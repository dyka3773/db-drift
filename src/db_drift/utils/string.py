import hashlib


def hash_body(body: str) -> str:
    """
    Generate a SHA-256 hash of the given body string.

    Args:
        body (str): The body string to hash.

    Returns:
        str: The SHA-256 hash of the body.
    """
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
