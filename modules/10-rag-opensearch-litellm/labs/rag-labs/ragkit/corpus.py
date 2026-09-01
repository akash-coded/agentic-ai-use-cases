"""The fictional corpus and the mini multi-hop benchmark.

All companies, people and figures are invented so that no real fact is misstated.
Every benchmark question carries gold spans that are exact substrings of a document,
so recall can be measured at chunk level under any chunking strategy.
"""
from dataclasses import dataclass, field
from .store import Doc

# ----------------------------------------------------------------------------
# Documents. Paragraphs are separated by a blank line so structural chunking has
# something to split on. Dates are ISO so metadata filters are trivial.
# ----------------------------------------------------------------------------
DOCS = [
    # --- storyline: Nord Aerospace, Elena Ruiz, Vega Dynamics (the worked question) ---
    Doc("a1", "Nord Aerospace names Elena Ruiz chief executive", "TechCrunch", "2026-03-12",
        "Nord Aerospace, the Bergen-based launch-vehicle maker, named Elena Ruiz as chief executive on Thursday, ending a nine-month search. Ruiz joins from Vega Dynamics, the propulsion firm she led for six years.\n\n"
        "She succeeds interim chief executive Lars Holm, who returns to his role as chief operating officer. The board said Ruiz would lead Nord's push into reusable first stages and a planned expansion of its Bergen test site.\n\n"
        "Ruiz said the appointment was a chance to build the next generation of European launch capability. Nord Aerospace employs about 1,400 people and reported revenue of 210 million euros in 2025."),
    Doc("b7", "Vega Dynamics shares jump in Nasdaq debut", "Reuters", "2023-06-08",
        "Shares of Vega Dynamics rose 28 percent in their Nasdaq debut on Thursday, June 8, 2023, valuing the propulsion company at about 2.1 billion dollars. The initial public offering raised 310 million dollars and the stock trades under the ticker VGDN.\n\n"
        "Chief executive Elena Ruiz, who has run the company since 2020, said the proceeds would fund a second engine plant in Oslo. Ruiz took the company public after three years as chief executive and had earlier served as its head of engineering.\n\n"
        "The listing was the largest by a European space company on a United States exchange this year. Vega Dynamics builds the VD-7 Kestrel engine used by two small-launch providers."),
    Doc("d3", "Vela Systems appoints Marcus Hale as chief executive", "Bloomberg", "2026-04-02",
        "Vela Systems, the Turin-based maker of satellite antennas, appointed Marcus Hale as chief executive on Wednesday, the company said in a statement. Hale previously ran the ground-segment division at Orbis Networks.\n\n"
        "The appointment follows the departure of founder Chiara Bassi, who will remain on the board. Vela said Hale would focus on winning contracts for the European Union's secure-connectivity constellation.\n\n"
        "Vela Systems employs about 600 people. The company did not disclose revenue figures."),
    Doc("e2", "Vega Dynamics posts record quarterly revenue", "Financial Times", "2025-11-20",
        "Vega Dynamics reported third-quarter revenue of 84 million dollars, a record for the propulsion company, driven by deliveries of its VD-7 Kestrel engine to two launch customers.\n\n"
        "Chief executive Elena Ruiz said demand for the engine had outstripped capacity at the Oslo plant. The company raised its full-year guidance."),
    Doc("g1", "European launch startups compete for institutional payloads", "Reuters", "2025-06-30",
        "A group of European launch startups, including Nord Aerospace and two French firms, submitted bids for institutional payload contracts, the European Space Agency said.\n\n"
        "Nord Aerospace's interim chief executive Lars Holm said the company expected a first orbital attempt in 2027."),
    Doc("g2", "Nord Aerospace expands Bergen test site", "Bloomberg", "2026-05-14",
        "Nord Aerospace began construction of a second test stand at its Bergen site, chief executive Elena Ruiz said on a call with reporters.\n\n"
        "The stand will support engines of up to 400 kilonewtons. Ruiz said the company was on schedule for a first orbital attempt in 2027."),
    Doc("g3", "VD-7 Kestrel engine data sheet", "Vega Dynamics engineering", "2024-02-01",
        "The VD-7 Kestrel is a 90 kilonewton methane-oxygen engine built by Vega Dynamics. Chamber pressure is 110 bar and the nozzle expansion ratio is 45.\n\n"
        "The engine designation VD-7 replaced the earlier VD-5. Qualification firing accumulated 2,400 seconds across 31 starts.",
        tenant="vega-internal", acl=["vega-engineering"]),

    # --- storyline: Halden Robotics and Brisk Automation ---
    Doc("h1", "Halden Robotics to buy Brisk Automation for 120 million dollars", "Reuters", "2024-09-17",
        "Halden Robotics agreed to acquire Brisk Automation, a maker of warehouse picking arms, for 120 million dollars in cash, the companies said on Tuesday, September 17, 2024.\n\n"
        "Halden chief executive Priya Natarajan said the deal would add picking capability to Halden's mobile-robot fleet. Brisk, based in Eindhoven, will keep its brand for two years.\n\n"
        "The transaction is expected to close by the end of the year."),
    Doc("h2", "Brisk Automation raises 40 million dollar Series B", "TechCrunch", "2022-02-03",
        "Brisk Automation has raised a 40 million dollar Series B led by Northlight Ventures, with participation from existing investors, the Eindhoven startup said on February 3, 2022.\n\n"
        "The company builds robotic arms that pick individual items in e-commerce warehouses. Chief executive Wouter de Vries said the funds would double the engineering team."),
    Doc("h3", "Halden Robotics founder Natarajan steps down as chief executive", "Bloomberg", "2025-05-06",
        "Priya Natarajan, who founded Halden Robotics in 2016, stepped down as chief executive on May 6, 2025, and was succeeded by chief financial officer Tomas Weber, the company said.\n\n"
        "Natarajan will become executive chair. Weber joined Halden in 2021 from Orbis Networks."),
    Doc("h4", "Halden Robotics revenue climbs to 212 million dollars", "Financial Times", "2026-02-11",
        "Halden Robotics reported revenue of 212 million dollars for 2025, up 31 percent, as warehouse operators expanded automation budgets.\n\n"
        "Chief executive Tomas Weber said the Brisk picking arms now account for a fifth of sales."),
    Doc("h5", "Fleet manager release notes 4.2", "Halden Robotics engineering", "2025-08-01",
        "Version 4.2 of the Halden fleet manager fixes error code ERR-4471, which caused idle robots to report a false low-battery state. The fix changes the polling interval from 30 seconds to 5 seconds.\n\n"
        "Known issue: ERR-4472 may appear on mixed fleets that include Brisk picking arms running firmware below 2.9.",
        tenant="halden-internal", acl=["halden-engineering"]),

    # --- storyline: Orbis Networks ---
    Doc("o1", "Orbis Networks raises 500 million dollars in NYSE listing", "Reuters", "2021-10-14",
        "Orbis Networks raised 500 million dollars in its initial public offering on the New York Stock Exchange on October 14, 2021, pricing shares at 22 dollars. The stock trades under the ticker ORBN.\n\n"
        "Chief executive Dana Kowalski said the proceeds would fund the rollout of the company's private 5G networks for ports and mines."),
    Doc("o2", "Orbis Networks revenue reaches 1.4 billion dollars", "Financial Times", "2026-01-22",
        "Orbis Networks reported revenue of 1.4 billion dollars for 2025, up 18 percent, helped by the acquisition of Mistral Spectrum.\n\n"
        "Chief executive Dana Kowalski said private-network contracts with three European ports drove growth."),
    Doc("o3", "Orbis Networks completes Mistral Spectrum acquisition", "Bloomberg", "2025-08-19",
        "Orbis Networks completed its acquisition of Mistral Spectrum, a spectrum-management software firm, for 95 million dollars on August 19, 2025.\n\n"
        "The deal gives Orbis software to manage shared spectrum across its private networks."),

    # --- storyline: Lumen Bio and Amir Sadeghi ---
    Doc("l1", "Lumen Bio raises 200 million dollars in Nasdaq IPO", "Reuters", "2024-05-16",
        "Lumen Bio raised 200 million dollars in its initial public offering on the Nasdaq on May 16, 2024, and its shares trade under the ticker LMBO.\n\n"
        "Chief executive Amir Sadeghi said the funds would carry the company's lead liver-disease drug through phase 3 trials."),
    Doc("l2", "Profile: Amir Sadeghi, the founder who sold Helix Diagnostics and started again", "TechCrunch", "2024-06-02",
        "Before founding Lumen Bio, Amir Sadeghi founded Helix Diagnostics, a blood-test company that he sold to Corvin Pharma in 2019 for 140 million dollars.\n\n"
        "Sadeghi started Lumen Bio in 2020 with two former Helix colleagues. He said the Helix sale taught him to run trials with a smaller team."),
    Doc("l3", "Lumen Bio phase 3 trial meets primary endpoint", "Financial Times", "2025-09-30",
        "Lumen Bio said its phase 3 trial of LB-201 met its primary endpoint, with results announced on September 30, 2025. Shares rose 40 percent.\n\n"
        "Chief executive Amir Sadeghi said the company would file for approval in the first half of 2026."),

    # --- storyline: Sable Energy and Mei Lin ---
    Doc("s1", "Sable Energy raises 150 million dollar Series C", "TechCrunch", "2025-03-11",
        "Sable Energy, a sodium-ion battery maker, raised a 150 million dollar Series C led by Northlight Ventures on March 11, 2025.\n\n"
        "Chief executive Mei Lin said the round would fund a pilot line in Gdansk."),
    Doc("s2", "Sable Energy plans Gdansk gigafactory", "Reuters", "2025-10-08",
        "Sable Energy will build a 4 gigawatt-hour battery plant in Gdansk, Poland, with production expected in 2027.\n\n"
        "The company said the plant would employ 900 people."),
    Doc("s3", "Profile: Mei Lin, from rocket engines to sodium batteries", "Bloomberg", "2025-04-01",
        "Mei Lin, chief executive of Sable Energy, spent four years as chief operating officer at Vega Dynamics before founding Sable in 2022.\n\n"
        "Lin said the discipline of engine testing shaped how Sable qualifies battery cells."),

    # --- storyline: Kestrel Foods (lexical trap with the VD-7 Kestrel engine) ---
    Doc("k1", "Kestrel Foods recalls frozen meals over labelling error", "Reuters", "2024-03-05",
        "Kestrel Foods recalled 12,000 cases of frozen meals across Germany after an allergen labelling error, the company said on March 5, 2024.\n\n"
        "The recall affects three product lines sold under the Kestrel brand."),
    Doc("k2", "Kestrel Foods appoints Ingrid Solberg as chief financial officer", "Bloomberg", "2025-01-15",
        "Kestrel Foods appointed Ingrid Solberg as chief financial officer, effective February 1, 2025. Solberg joins from a Nordic grocery retailer.\n\n"
        "She succeeds Henrik Dahl, who retires after eleven years."),
    Doc("k3", "Kestrel Foods revenue flat at 3.1 billion euros", "Financial Times", "2026-02-03",
        "Kestrel Foods reported 2025 revenue of 3.1 billion euros, flat on the previous year, as price rises offset lower volumes.\n\n"
        "The company said it expected modest growth in 2026."),

    # --- investors, roundups, and noise ---
    Doc("n1", "Northlight Ventures closes 800 million dollar fund", "Reuters", "2024-11-12",
        "Northlight Ventures closed its fifth fund at 800 million dollars on November 12, 2024, to back industrial and climate startups in Europe.\n\n"
        "The firm's earlier investments include Brisk Automation and Sable Energy."),
    Doc("r1", "The year in European listings", "Financial Times", "2024-12-20",
        "European companies raised less on public markets in 2024 than in 2023. The largest technology listing of the year was Lumen Bio's 200 million dollar Nasdaq IPO in May.\n\n"
        "Bankers expect a stronger 2025 if interest rates fall."),
    Doc("f1", "European Central Bank holds rates", "Reuters", "2025-02-14",
        "The European Central Bank left its deposit rate unchanged on Thursday, citing sticky services inflation.\n\n"
        "Markets had expected a cut by June."),
    Doc("f2", "Startup funding in Europe rises 12 percent in second quarter", "TechCrunch", "2025-07-22",
        "Venture funding for European startups rose 12 percent in the second quarter, with climate and robotics companies taking the largest share.\n\n"
        "Late-stage rounds recovered faster than seed rounds."),
    Doc("f3", "Nasdaq to tighten listing rules for small companies", "Bloomberg", "2024-08-09",
        "Nasdaq proposed stricter minimum-float requirements for new listings, a move aimed at thinly traded small companies.\n\n"
        "The exchange said the rules would apply to initial public offerings from 2025."),
    Doc("f4", "Chief executive turnover hits a five-year high", "Financial Times", "2026-03-30",
        "Chief executive departures at European listed companies reached a five-year high in the first quarter, as boards moved faster to replace leaders after weak results.\n\n"
        "Interim appointments now last nine months on average before a permanent chief executive is named."),
]


# ----------------------------------------------------------------------------
# Benchmark. Gold spans are exact substrings of the document body. A question is
# answerable only if every gold span survives into the packed context.
# ----------------------------------------------------------------------------
@dataclass
class Question:
    qid: str
    qtype: str                      # inference | comparison | temporal | null
    text: str
    answer: str | None              # None for null questions
    gold: list = field(default_factory=list)   # list of (doc_id, span)
    dependent: bool = False         # True when hop two needs hop one's answer
    distractor_answer: str = ""     # what an ungrounded model would say for a null question
    frozen: bool = False            # held out from tuning
    plan: list = field(default_factory=list)   # the decomposition a planner model would produce; used offline, replaced by the model when a provider is set

    @property
    def gold_docs(self) -> list:
        return sorted({d for d, _ in self.gold})


QUESTIONS = [
    Question("q01", "inference",
             "The person who became CEO of Nord Aerospace in 2026 had earlier taken which company public, and in what year?",
             "Vega Dynamics, 2023",
             [("a1", "named Elena Ruiz as chief executive on Thursday, ending a nine-month search. Ruiz joins from Vega Dynamics"),
              ("b7", "Shares of Vega Dynamics rose 28 percent in their Nasdaq debut on Thursday, June 8, 2023")],
             dependent=True),
    Question("q02", "inference",
             "Which venture firm led the Series B of the company that Halden Robotics acquired in 2024?",
             "Northlight Ventures",
             [("h1", "Halden Robotics agreed to acquire Brisk Automation, a maker of warehouse picking arms, for 120 million dollars in cash"),
              ("h2", "Brisk Automation has raised a 40 million dollar Series B led by Northlight Ventures")],
             dependent=True),
    Question("q03", "inference",
             "The founder of the diagnostics company that was sold to Corvin Pharma later took which company public?",
             "Lumen Bio",
             [("l2", "Amir Sadeghi founded Helix Diagnostics, a blood-test company that he sold to Corvin Pharma in 2019"),
              ("l1", "Lumen Bio raised 200 million dollars in its initial public offering on the Nasdaq on May 16, 2024")],
             dependent=True),
    Question("q04", "comparison",
             "Which raised more in its initial public offering, Orbis Networks or Vega Dynamics?",
             "Orbis Networks, 500 million dollars against 310 million dollars",
             [("o1", "Orbis Networks raised 500 million dollars in its initial public offering on the New York Stock Exchange on October 14, 2021"),
              ("b7", "The initial public offering raised 310 million dollars")]),
    Question("q05", "comparison",
             "Which company reported higher revenue for 2025, Halden Robotics or Orbis Networks?",
             "Orbis Networks, 1.4 billion dollars against 212 million dollars",
             [("h4", "Halden Robotics reported revenue of 212 million dollars for 2025"),
              ("o2", "Orbis Networks reported revenue of 1.4 billion dollars for 2025")]),
    Question("q06", "comparison",
             "Did Sable Energy's Series C raise more than Brisk Automation's Series B?",
             "Yes, 150 million dollars against 40 million dollars",
             [("s1", "Sable Energy, a sodium-ion battery maker, raised a 150 million dollar Series C led by Northlight Ventures"),
              ("h2", "Brisk Automation has raised a 40 million dollar Series B led by Northlight Ventures")]),
    Question("q07", "temporal",
             "Which happened first, the initial public offering of Vega Dynamics or that of Orbis Networks?",
             "Orbis Networks, in 2021, before Vega Dynamics in 2023",
             [("b7", "Shares of Vega Dynamics rose 28 percent in their Nasdaq debut on Thursday, June 8, 2023"),
              ("o1", "Orbis Networks raised 500 million dollars in its initial public offering on the New York Stock Exchange on October 14, 2021")]),
    Question("q08", "temporal",
             "Did Priya Natarajan step down as chief executive before or after Halden Robotics acquired Brisk Automation?",
             "After, in May 2025 against September 2024",
             [("h3", "Priya Natarajan, who founded Halden Robotics in 2016, stepped down as chief executive on May 6, 2025"),
              ("h1", "Halden Robotics agreed to acquire Brisk Automation, a maker of warehouse picking arms, for 120 million dollars in cash, the companies said on Tuesday, September 17, 2024")],
             frozen=True),
    Question("q09", "temporal",
             "Which came first for Lumen Bio, its initial public offering or its phase 3 trial results?",
             "The initial public offering, in May 2024, before the phase 3 results in September 2025",
             [("l1", "Lumen Bio raised 200 million dollars in its initial public offering on the Nasdaq on May 16, 2024"),
              ("l3", "Lumen Bio said its phase 3 trial of LB-201 met its primary endpoint, with results announced on September 30, 2025")],
             frozen=True),
    Question("q10", "null", "Who is the chief financial officer of Nord Aerospace?", None, [],
             distractor_answer="Ingrid Solberg"),
    Question("q11", "null", "What was Vela Systems' revenue in 2025?", None, [],
             distractor_answer="about 600 million euros"),
    Question("q12", "null", "Which bank underwrote the initial public offering of Vega Dynamics?", None, [],
             distractor_answer="Goldman Sachs", frozen=True),
]

# Decomposition plans. Each hop is a dict: text (may contain {bridge}), depends_on (hop index or None),
# bridge_kind (person or company, when the hop needs an entity from an earlier hop), tool (the tool an expert would pick).
PLANS = {
    "q01": [{"text": "who became chief executive of Nord Aerospace in 2026", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "which company did {bridge} take public, and in what year", "depends_on": 0, "bridge_kind": "person", "tool": "hybrid"}],
    "q02": [{"text": "which company did Halden Robotics acquire in 2024", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "which venture firm led the Series B of {bridge}", "depends_on": 0, "bridge_kind": "company", "tool": "hybrid"}],
    "q03": [{"text": "which diagnostics company was sold to Corvin Pharma and who founded it", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "which company did {bridge} take public", "depends_on": 0, "bridge_kind": "person", "tool": "hybrid"}],
    "q04": [{"text": "how much did Orbis Networks raise in its initial public offering", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "how much did Vega Dynamics raise in its initial public offering", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
    "q05": [{"text": "Halden Robotics revenue for 2025", "depends_on": None, "bridge_kind": "", "tool": "lexical"},
            {"text": "Orbis Networks revenue for 2025", "depends_on": None, "bridge_kind": "", "tool": "lexical"}],
    "q06": [{"text": "how much was the Series C raised by Sable Energy", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "how much was the Series B raised by Brisk Automation", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
    "q07": [{"text": "when was the initial public offering of Vega Dynamics", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "when was the initial public offering of Orbis Networks", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
    "q08": [{"text": "when did Priya Natarajan step down as chief executive", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "when did Halden Robotics agree to acquire Brisk Automation", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
    "q09": [{"text": "when was the initial public offering of Lumen Bio", "depends_on": None, "bridge_kind": "", "tool": "hybrid"},
            {"text": "when did Lumen Bio announce its phase 3 trial results", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
    "q10": [{"text": "chief financial officer of Nord Aerospace", "depends_on": None, "bridge_kind": "", "tool": "lexical"}],
    "q11": [{"text": "Vela Systems revenue 2025", "depends_on": None, "bridge_kind": "", "tool": "lexical"}],
    "q12": [{"text": "bank that underwrote the initial public offering of Vega Dynamics", "depends_on": None, "bridge_kind": "", "tool": "hybrid"}],
}
for _q in QUESTIONS:
    _q.plan = PLANS.get(_q.qid, [])

# The worked question that the whole programme carries.
ANCHOR = QUESTIONS[0]


def load(store):
    """Load the corpus into a store and return the benchmark."""
    store.add_docs(DOCS)
    return list(QUESTIONS)


def check_spans():
    """Assert every gold span is an exact substring of its document body."""
    bodies = {d.doc_id: d.body for d in DOCS}
    bad = [(q.qid, doc, span[:40]) for q in QUESTIONS for doc, span in q.gold if span not in bodies[doc]]
    assert not bad, f"gold spans not found verbatim: {bad}"
    return True


# Test inputs and expected outcomes
# check_spans()              -> True
# len(DOCS)                  -> 30
# ANCHOR.gold_docs           -> ["a1", "b7"]
# [q.qid for q in QUESTIONS if q.qtype == "null"]  -> ["q10", "q11", "q12"]
