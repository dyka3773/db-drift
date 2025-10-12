from db_drift.cli.cli import cli
from db_drift.utils import custom_logging

logger = custom_logging.setup_logger("db-drift")


def main() -> None:
    """Entry point for the db-drift package."""
    logger.debug("Starting db-drift CLI")
    cli()


if __name__ == "__main__":
    main()
