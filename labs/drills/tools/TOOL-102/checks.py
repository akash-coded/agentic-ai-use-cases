from harness import check, expect, expect_eq, expect_in
S = {"required": ["booking_ref"], "properties": {"booking_ref": "string", "verbose": "boolean"}}
@check("valid arguments pass")
def t_ok(m): expect_eq(m.validate_args(S, {"booking_ref": "X", "verbose": True}), {"ok": True})
@check("a hallucinated key is reported by name",
       teaches="The model cannot fix what it cannot see. Name the key it invented.")
def t_unknown(m):
    r = m.validate_args(S, {"booking_reference": "X"}); expect_eq(r["ok"], False); expect_in("booking_reference", r["unknown"])
@check("a missing required key is reported")
def t_missing(m):
    r = m.validate_args(S, {"verbose": True}); expect_in("booking_ref", r["missing"])
@check("the advice names the VALID keys",
       teaches="'Invalid argument' leaves the model to guess again — usually the same guess. Listing the valid names ends the loop.")
def t_advice(m):
    r = m.validate_args(S, {"booking_reference": "X"})
    expect_in("booking_ref", r["advice"]); expect_in("verbose", r["advice"])
@check("None arguments do not raise",
       teaches="Zero-argument tools arrive with input missing entirely. Crashing on None is a self-inflicted bug.")
def t_none(m):
    r = m.validate_args({"required": [], "properties": {}}, None); expect_eq(r, {"ok": True})
