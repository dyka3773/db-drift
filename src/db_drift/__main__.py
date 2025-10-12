import os

from db_drift.cli.cli import cli
from db_drift.utils import custom_logging
from db_drift.utils.exceptions import CliError, ConfigError, DatabaseError, DbDriftError, DbDriftInterruptError, ExitCode
from db_drift.utils.exceptions.base import DbDriftSystemError
from db_drift.utils.exceptions.formatting import handle_error_and_exit, handle_unexpected_error

logger = custom_logging.setup_logger("db-drift")


DEBUG_MODE: int = os.getenv("DB_DRIFT_DEBUG", "").lower() in ("1", "true", "yes", "on")


def main() -> None:
    """Entry point for the db-drift package."""
    try:
        logger.debug("Starting db-drift CLI")
        cli()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        error = DbDriftInterruptError()
        logger.info("Operation cancelled by user")
        handle_error_and_exit(
            error,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=False,
        )

    except CliError as e:
        # Handle CLI-specific errors (argument parsing, usage errors, etc.)
        logger.exception("CLI Error occurred")
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except ConfigError as e:
        # Handle configuration errors
        logger.exception("Configuration Error occurred")
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except DatabaseError as e:
        # Handle database connection and query errors
        logger.exception("Database Error occurred")
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except DbDriftError as e:
        # Handle other custom application errors
        logger.exception("Application Error occurred")
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except FileNotFoundError as e:
        # Handle file not found errors
        logger.exception("File not found")
        system_error = DbDriftSystemError(f"Required file not found: {e}", exit_code=ExitCode.NO_INPUT)
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except PermissionError as e:
        # Handle permission errors
        logger.exception("Permission denied")
        system_error = DbDriftSystemError(f"Permission denied: {e}", exit_code=ExitCode.NO_PERMISSION)
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=DEBUG_MODE,
            show_suggestions=True,
        )

    except Exception:
        # Handle any unexpected errors
        logger.exception("Unexpected error occurred")

        # In debug mode, show full traceback; otherwise, show generic message
        handle_unexpected_error(DEBUG_MODE, logger)


if __name__ == "__main__":
    main()
