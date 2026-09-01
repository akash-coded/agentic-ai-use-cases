class Throttled(Exception):
    pass


class BadRequest(Exception):
    pass


def classify_error(exc):
    if isinstance(exc, Throttled):
        return "retryable"
    return "fatal"


def working(name, answer="ok"):
    return {"id": name, "call": lambda req: f"{answer} from {name}"}


def failing(name, exc):
    def call(req):
        raise exc
    return {"id": name, "call": call}


PRIMARY = working("claude-primary")
FALLBACK = working("claude-fallback")
THROTTLED = failing("claude-primary", Throttled("rate limit"))
BROKEN = failing("claude-primary", BadRequest("malformed input"))
