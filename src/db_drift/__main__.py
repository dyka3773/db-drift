from db_drift.cli.cli import cli_arg_parse
from db_drift.db.factory import get_connector
from db_drift.report.generate import generate_drift_report
from db_drift.utils import custom_logging
from db_drift.utils.constants import ExitCode
from db_drift.utils.exceptions import CliError, ConfigError, DatabaseError, DbDriftError, DbDriftInterruptError
from db_drift.utils.exceptions.base import DbDriftSystemError
from db_drift.utils.exceptions.formatting import handle_error_and_exit

logger = custom_logging.setup_logger("db-drift")


def main() -> None:
    """Entry point for the db-drift package."""
    try:
        logger.debug("Starting db-drift CLI")
        args = cli_arg_parse()

        connector = get_connector(args.dbms)

        db_structure_source = connector(args.source).fetch_schema_structure()
        logger.info("Fetched source database schema structure.")

        db_structure_target = connector(args.target).fetch_schema_structure()
        logger.info("Fetched target database schema structure.")

        logger.info("Generating drift report...")
        generate_drift_report(
            db_structure_source,
            db_structure_target,
            args.output,
        )

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        error = DbDriftInterruptError()
        logger.info("Operation cancelled by user")
        handle_error_and_exit(
            error,
            logger=logger,
            show_traceback=True,
            show_suggestions=False,
        )

    except CliError as e:
        # Handle CLI-specific errors (argument parsing, usage errors, etc.)
        logger.error("CLI Error occurred")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except ConfigError as e:
        # Handle configuration errors
        logger.error("Configuration Error occurred")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except DatabaseError as e:
        # Handle database connection and query errors
        logger.error("Database Error occurred")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except DbDriftError as e:
        # Handle other custom application errors
        logger.error("Application Error occurred")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        handle_error_and_exit(
            e,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except FileNotFoundError as e:
        # Handle file not found errors
        logger.error("File not found")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        system_error = DbDriftSystemError(f"Required file not found: {e}", exit_code=ExitCode.NO_INPUT)
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except PermissionError as e:
        # Handle permission errors
        logger.error("Permission denied")  # noqa: TRY400 # The stacktrace is logged in handle_error_and_exit
        system_error = DbDriftSystemError(f"Permission denied: {e}", exit_code=ExitCode.NO_PERMISSION)
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=True,
            show_suggestions=True,
        )

    except Exception as e:
        # Handle any unexpected errors
        logger.exception("Unexpected error occurred")
        system_error = DbDriftSystemError(f"An unexpected error occurred: {e}", exit_code=ExitCode.GENERAL_ERROR)
        handle_error_and_exit(
            system_error,
            logger=logger,
            show_traceback=True,
            show_suggestions=False,
        )


if __name__ == "__main__":
    main()
