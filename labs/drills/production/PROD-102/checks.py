from harness import check, expect_eq
def exc(name): return type(name, (Exception,), {})("boom")
@check("throttling is retryable")
def t_throttle(m): expect_eq(m.classify_error(exc("ThrottlingException")), "retryable")
@check("a malformed request is fatal", teaches="It will be malformed on the fallback too.")
def t_validation(m): expect_eq(m.classify_error(exc("ValidationException")), "fatal")
@check("a timeout is retryable")
def t_timeout(m): expect_eq(m.classify_error(TimeoutError("slow")), "retryable")
@check("access denied is fatal", teaches="Permissions do not come back on the next model.")
def t_denied(m): expect_eq(m.classify_error(exc("AccessDeniedException")), "fatal")
@check("an UNKNOWN error is fatal",
       teaches="Defaulting to retryable walks a five-model chain on something you do not understand, at five times the cost, to learn nothing. Fail fast and put it in the log where someone will add a rule.")
def t_unknown(m): expect_eq(m.classify_error(exc("SomethingNobodyHasSeen")), "fatal")
