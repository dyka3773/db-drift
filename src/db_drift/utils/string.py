import hashlib


def hash_body(body: str) -> str:
    """
    Generate an MD5 hash of the given body string.

    Args:
        body (str): The body string to hash.

    Returns:
        str: The MD5 hash of the body.
    """
    return hashlib.md5(body.encode("utf-8")).hexdigest()  # noqa: S324
