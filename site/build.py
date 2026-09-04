#!/usr/bin/env python3
"""Build the GitHub Pages site around the pristine SkyWays Architect tool.

The tool, ``site/app/SkyWays-Architect.html``, is never edited. This script copies it to ``_site/index.html``
and injects two things at the document boundaries: attribution and SEO metadata just before ``</head>``, and
the site frame (attribution, licence notice, invitation, contact form) just before ``</body>``. Everything
between those two points is byte-for-byte the tool.

    python site/build.py            # writes site/_site/
    python -m http.server -d site/_site 8000

Updating the tool is a file copy: replace ``site/app/SkyWays-Architect.html`` with the new export.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent
SRC = SITE / "app" / "SkyWays-Architect.html"
BASE_URL = "https://akash-coded.github.io/aws-bedrock-agentcore-strands/"
REPO_URL = "https://github.com/akash-coded/aws-bedrock-agentcore-strands"
AUTHOR = "Akash Das"
TITLE = "SkyWays Architect · the agentic PDLC in one simulation"
DESCRIPTION = ("One agentic feature, six architect decisions, thirty-eight scenarios. An interactive walk-through "
               "of the agentic PDLC by role, built by Akash Das.")

JSON_LD = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "SkyWays Architect",
    "alternateName": "SkyWays · Architect's Demo",
    "url": BASE_URL,
    "description": DESCRIPTION,
    "image": BASE_URL + "assets/og.png",
    "applicationCategory": "EducationalApplication",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "isAccessibleForFree": True,
    "author": {"@type": "Person", "name": AUTHOR, "url": "https://github.com/akash-coded"},
    "copyrightHolder": {"@type": "Person", "name": AUTHOR},
    "copyrightYear": 2026,
    "license": REPO_URL + "/blob/main/LICENSE",
    "isPartOf": {"@type": "CreativeWork", "name": "Agentic AI on AWS", "url": REPO_URL},
}

HEAD = f"""
<!-- site frame: injected at build time by site/build.py. The tool itself is untouched. -->
<meta name="description" content="{DESCRIPTION}">
<meta name="author" content="{AUTHOR}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE_URL}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F7F6F2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SkyWays Architect">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{BASE_URL}">
<meta property="og:image" content="{BASE_URL}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{BASE_URL}assets/og.png">
<script type="application/ld+json">{json.dumps(JSON_LD, ensure_ascii=False)}</script>
<link rel="stylesheet" href="frame/frame.css">
"""

BODY = """
<!-- site frame: attribution, licence, invitation and contact form. See site/frame/. -->
<script src="frame/config.js"></script>
<script src="frame/frame.js"></script>
"""

ROBOTS = f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n"


def sitemap(today: str) -> str:
    urls = [BASE_URL, BASE_URL + "app/SkyWays-Architect.html"]
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


def inject(html: str) -> str:
    for marker in ("</head>", "</body>"):
        if html.count(marker) != 1:
            sys.exit(f"expected exactly one {marker} in {SRC.name}, found {html.count(marker)}")
    html = html.replace("</head>", HEAD + "</head>", 1)
    return html.replace("</body>", BODY + "</body>", 1)


def build(out: Path) -> None:
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    original = SRC.read_text(encoding="utf-8")
    (out / "index.html").write_text(inject(original), encoding="utf-8")
    for folder in ("frame", "assets", "app"):
        shutil.copytree(SITE / folder, out / folder)
    shutil.copy2(SITE / "404.html", out / "404.html")
    (out / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (out / "sitemap.xml").write_text(sitemap(date.today().isoformat()), encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    built = (out / "index.html").read_text(encoding="utf-8")
    # The tool must survive the build untouched: strip the two injections and compare.
    if built.replace(HEAD, "", 1).replace(BODY, "", 1) != original:
        sys.exit("the build changed the tool itself; refusing to continue")
    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    print(f"built {out.relative_to(SITE.parent)} ({len(files)} files, index.html {len(built):,} bytes)")
    for f in files:
        print("  " + f)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(SITE / "_site"), help="output directory (default: site/_site)")
    build(Path(ap.parse_args().out).resolve())
