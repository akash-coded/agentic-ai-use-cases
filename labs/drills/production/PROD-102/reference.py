RETRYABLE = {"ThrottlingException", "ServiceUnavailableException", "TimeoutError", "ModelTimeoutException", "ConnectionError"}
FATAL = {"ValidationException", "AccessDeniedException", "ResourceNotFoundException"}

def classify_error(exc):
    name = type(exc).__name__
    if name in RETRYABLE:
        return "retryable"
    if name in FATAL:
        return "fatal"
    return "fatal"      # unknown: an error you do not understand is not one to retry five times
