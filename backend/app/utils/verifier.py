import os

def verify(step_action: str, result: dict, rule: str) -> bool:
    """
    Simple post-condition verifier.
    """

    if rule == "documents_loaded":
        return result.get("count", 0) > 0

    if rule == "file_exists":
        return os.path.exists(result.get("file", ""))

    if rule == "email_sent":
        return result.get("status") == "sent"

    if rule == "user_confirmed":
        return True

    return False
