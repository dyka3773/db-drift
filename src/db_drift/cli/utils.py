from importlib import metadata


def get_version() -> str:
    """Get the current version of the package."""
    try:
        return metadata.version("db-drift")
    except metadata.PackageNotFoundError:
        return "unknown"
