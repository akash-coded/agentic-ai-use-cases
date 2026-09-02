from harness import check, expect, expect_eq
C = {"answerable": 58, "ambiguous": 14, "out_of_scope": 9, "unretrievable": 11, "adversarial": 8}
@check("the target is (ambiguous + out_of_scope + unretrievable) / total",
       teaches="34 of 100 inputs have 'I don't know' as the correct answer. An agent abstaining on 3% of these is answering 31% it should not.")
def t_target(m): expect_eq(m.abstention_target(C)["target"], 0.34)
@check("answerable inputs are NOT in the numerator")
def t_not_answerable(m):
    r = m.abstention_target({"answerable": 90, "ambiguous": 5, "out_of_scope": 3, "unretrievable": 2, "adversarial": 0})
    expect_eq(r["target"], 0.1)
@check("adversarial inputs are NOT in the numerator",
       teaches="Adversarial cases should be resisted, which is a different behaviour from abstaining — they get their own slice.")
def t_not_adversarial(m):
    r = m.abstention_target({"answerable": 50, "ambiguous": 0, "out_of_scope": 0, "unretrievable": 0, "adversarial": 50})
    expect_eq(r["target"], 0.0)
@check("the denominator is every classified input")
def t_total(m): expect_eq(m.abstention_target(C)["n"], 100)
@check("the band is ±5 points around the target")
def t_band(m): expect_eq(m.abstention_target(C)["band"], (0.29, 0.39))
