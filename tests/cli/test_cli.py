"""Tests for CLI argument parsing and validation."""

import argparse
from unittest.mock import Mock, patch

import pytest
from db_drift.cli.cli import cli_arg_parse
from db_drift.utils.exceptions import CliArgumentError, CliUsageError


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_invalid_argument_error_handling(mock_parse_args: Mock) -> None:
    """Test handling of argparse.ArgumentError."""
    mock_parse_args.side_effect = argparse.ArgumentError(None, "Invalid value for argument")

    with pytest.raises(CliArgumentError, match="Invalid argument: Invalid value for argument"):
        cli_arg_parse()


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_system_exit_error_handling(mock_parse_args: Mock) -> None:
    """Test handling of SystemExit from argparse."""
    # Test non-zero exit code (error case)
    mock_parse_args.side_effect = SystemExit(2)

    with pytest.raises(CliUsageError, match="Invalid command line arguments"):
        cli_arg_parse()


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_system_exit_success_re_raised(mock_parse_args: Mock) -> None:
    """Test that successful SystemExit (like --help) is re-raised."""
    mock_parse_args.side_effect = SystemExit(0)  # Success exit code

    with pytest.raises(SystemExit) as exc_info:
        cli_arg_parse()

    assert exc_info.value.code == 0


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_malformed_connection_string_handling(mock_parse_args: Mock) -> None:
    """Test handling of malformed connection strings."""
    # Connection strings without proper scheme
    malformed_strings = [
        # TODO @dyka3773: Add more possible malformed cases as needed
        "",
    ]

    for malformed_string in malformed_strings:
        mock_args = argparse.Namespace(
            dbms="sqlite",
            output="drift_report.html",
            source=malformed_string,
            target="sqlite:///target.db",
            verbose=False,
        )
        mock_parse_args.return_value = mock_args

        # Should raise an IndexError when trying to split on "://" and access [0]
        with pytest.raises((IndexError, CliArgumentError)):
            cli_arg_parse()
