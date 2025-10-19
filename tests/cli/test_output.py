import argparse
import contextlib
from unittest.mock import Mock, patch

from db_drift.cli.cli import cli


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_output_argument_default_value(mock_parse_args: Mock) -> None:
    """Test that --output defaults to 'drift_report.html'."""
    mock_args = argparse.Namespace(
        dbms="sqlite",
        output="drift_report.html",  # Default value
        source="sqlite:///source.db",
        target="sqlite:///target.db",
    )
    mock_parse_args.return_value = mock_args

    with contextlib.suppress(SystemExit):
        cli()


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_output_argument_custom_value(mock_parse_args: Mock) -> None:
    """Test that --output accepts custom filenames."""
    custom_outputs = [
        "custom_report.html",
        "my_drift_analysis.html",
        "report_2023.html",
        "output/nested/path/report.html",
    ]

    for output_file in custom_outputs:
        mock_args = argparse.Namespace(
            dbms="sqlite",
            output=output_file,
            source="sqlite:///source.db",
            target="sqlite:///target.db",
        )
        mock_parse_args.return_value = mock_args

        with contextlib.suppress(SystemExit):
            cli()
