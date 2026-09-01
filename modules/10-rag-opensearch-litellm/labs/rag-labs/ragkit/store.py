"""In-memory document and chunk store on SQLite.

Everything the notebooks retrieve from lives here, so any state can be inspected
with a SQL query. The store is created fresh on every run and is never written to disk.
"""
import hashlib
import json
import sqlite3
from dataclasses import dataclass, field
from typing import Iterable

SCHEMA = """
CREATE TABLE docs (
  doc_id TEXT PRIMARY KEY, title TEXT, source TEXT, date TEXT, tenant TEXT,
  acl TEXT, body TEXT, body_hash TEXT, version INTEGER DEFAULT 1
);
CREATE TABLE chunks (
  chunk_id TEXT, doc_id TEXT, ordinal INTEGER, text TEXT,
  n_words INTEGER, heading TEXT, index_version TEXT,
  PRIMARY KEY(chunk_id, index_version),
  FOREIGN KEY(doc_id) REFERENCES docs(doc_id)
);
CREATE INDEX chunks_doc ON chunks(doc_id);
CREATE INDEX chunks_ver ON chunks(index_version);
CREATE TABLE index_versions (
  version TEXT PRIMARY KEY, chunker TEXT, embedder TEXT, created_seq INTEGER, live INTEGER DEFAULT 0
);
CREATE TABLE traces (
  trace_id TEXT PRIMARY KEY, question TEXT, payload TEXT
);
"""


def content_hash(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]


@dataclass
class Doc:
    doc_id: str
    title: str
    source: str
    date: str
    body: str
    tenant: str = "public"
    acl: list = field(default_factory=lambda: ["everyone"])

    @property
    def text(self) -> str:
        return f"{self.title}\n\n{self.body}"


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    ordinal: int
    text: str
    heading: str = ""
    index_version: str = "v1"

    @property
    def n_words(self) -> int:
        return len(self.text.split())


class Store:
    """A SQLite in-memory store. One instance per notebook run."""

    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.con.row_factory = sqlite3.Row
        self.con.executescript(SCHEMA)
        self._seq = 0

    # ---- documents ----
    def add_docs(self, docs: Iterable[Doc]) -> int:
        rows = [(d.doc_id, d.title, d.source, d.date, d.tenant, json.dumps(d.acl), d.body, content_hash(d.body)) for d in docs]
        self.con.executemany("INSERT INTO docs(doc_id,title,source,date,tenant,acl,body,body_hash) VALUES (?,?,?,?,?,?,?,?)", rows)
        self.con.commit()
        return len(rows)

    def doc(self, doc_id: str) -> Doc:
        r = self.con.execute("SELECT * FROM docs WHERE doc_id=?", (doc_id,)).fetchone()
        if r is None:
            raise KeyError(doc_id)
        return Doc(r["doc_id"], r["title"], r["source"], r["date"], r["body"], r["tenant"], json.loads(r["acl"]))

    def docs(self) -> list:
        return [self.doc(r["doc_id"]) for r in self.con.execute("SELECT doc_id FROM docs ORDER BY doc_id")]

    def update_doc_body(self, doc_id: str, new_body: str) -> bool:
        """Edit a document. Returns True when the normalised body actually changed."""
        old = self.con.execute("SELECT body_hash FROM docs WHERE doc_id=?", (doc_id,)).fetchone()["body_hash"]
        new_hash = content_hash(new_body)
        if new_hash == old:
            return False
        self.con.execute("UPDATE docs SET body=?, body_hash=?, version=version+1 WHERE doc_id=?", (new_body, new_hash, doc_id))
        self.con.commit()
        return True

    # ---- chunks and index versions ----
    def add_chunks(self, chunks: Iterable[Chunk], version: str, chunker: str = "", embedder: str = "") -> int:
        chunks = list(chunks)
        self._seq += 1
        self.con.execute("INSERT OR REPLACE INTO index_versions(version,chunker,embedder,created_seq,live) VALUES (?,?,?,?,COALESCE((SELECT live FROM index_versions WHERE version=?),0))",
                         (version, chunker, embedder, self._seq, version))
        self.con.executemany("INSERT OR REPLACE INTO chunks(chunk_id,doc_id,ordinal,text,n_words,heading,index_version) VALUES (?,?,?,?,?,?,?)",
                             [(c.chunk_id, c.doc_id, c.ordinal, c.text, c.n_words, c.heading, version) for c in chunks])
        self.con.commit()
        return len(chunks)

    def chunks(self, version: str = None) -> list:
        version = version or self.live_version()
        rows = self.con.execute("SELECT * FROM chunks WHERE index_version=? ORDER BY doc_id, ordinal", (version,)).fetchall()
        return [Chunk(r["chunk_id"], r["doc_id"], r["ordinal"], r["text"], r["heading"], r["index_version"]) for r in rows]

    def chunk(self, chunk_id: str, version: str = None) -> Chunk:
        version = version or self.live_version()
        r = self.con.execute("SELECT * FROM chunks WHERE chunk_id=? AND index_version=?", (chunk_id, version)).fetchone()
        if r is None:
            raise KeyError(chunk_id)
        return Chunk(r["chunk_id"], r["doc_id"], r["ordinal"], r["text"], r["heading"], r["index_version"])

    def delete_chunks_for_doc(self, doc_id: str, version: str) -> int:
        cur = self.con.execute("DELETE FROM chunks WHERE doc_id=? AND index_version=?", (doc_id, version))
        self.con.commit()
        return cur.rowcount

    def set_live(self, version: str):
        """Atomic alias swap. Only one version is routed to at a time."""
        self.con.execute("UPDATE index_versions SET live=0")
        self.con.execute("UPDATE index_versions SET live=1 WHERE version=?", (version,))
        self.con.commit()

    def live_version(self) -> str:
        r = self.con.execute("SELECT version FROM index_versions WHERE live=1").fetchone()
        if r is None:
            r = self.con.execute("SELECT version FROM index_versions ORDER BY created_seq DESC LIMIT 1").fetchone()
        return r["version"] if r else "v1"

    def versions(self) -> list:
        return [dict(r) for r in self.con.execute("SELECT * FROM index_versions ORDER BY created_seq")]

    # ---- traces ----
    def save_trace(self, trace_id: str, question: str, payload: dict):
        self.con.execute("INSERT OR REPLACE INTO traces VALUES (?,?,?)", (trace_id, question, json.dumps(payload, default=str)))
        self.con.commit()

    def trace(self, trace_id: str) -> dict:
        r = self.con.execute("SELECT payload FROM traces WHERE trace_id=?", (trace_id,)).fetchone()
        return json.loads(r["payload"]) if r else None

    # ---- convenience ----
    def sql(self, query: str, params: tuple = ()):
        """Run any SELECT and get a pandas DataFrame back."""
        import pandas as pd
        rows = self.con.execute(query, params).fetchall()
        return pd.DataFrame([dict(r) for r in rows])


# Test inputs and expected outcomes
# s = Store(); s.add_docs([Doc("x","T","src","2026-01-01","hello world")])  -> returns 1
# s.doc("x").text                                                          -> "T\n\nhello world"
# s.update_doc_body("x", "hello world")                                    -> False (hash unchanged)
# s.update_doc_body("x", "hello there")                                    -> True, version becomes 2
# s.add_chunks([Chunk("x:0:abc","x",0,"hello there")], "v1"); s.set_live("v1"); s.live_version() -> "v1"
# the same chunk id may exist in several versions; (chunk_id, index_version) is the key
