import argparse
import contextlib
from unittest.mock import Mock, patch

from db_drift.cli.cli import cli
from db_drift.utils.constants import SUPPORTED_DBMS_REGISTRY


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_dbms_argument_valid_choices(mock_parse_args: Mock) -> None:
    """Test that --dbms accepts valid DBMS choices."""
    for dbms in SUPPORTED_DBMS_REGISTRY:
        mock_args = argparse.Namespace(
            dbms=dbms,
            output="drift_report.html",
            source="sqlite:///source.db",
            target="sqlite:///target.db",
            verbose=False,
        )
        mock_parse_args.return_value = mock_args

        # Should not raise any exception
        with contextlib.suppress(SystemExit):
            cli()


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_dbms_argument_default_value(mock_parse_args: Mock) -> None:
    """Test that --dbms defaults to 'sqlite'."""
    mock_args = argparse.Namespace(
        dbms="sqlite",  # Default value
        output="drift_report.html",
        source="sqlite:///source.db",
        target="sqlite:///target.db",
        verbose=False,
    )
    mock_parse_args.return_value = mock_args

    with contextlib.suppress(SystemExit):
        cli()
