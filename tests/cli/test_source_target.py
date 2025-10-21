import argparse
from unittest.mock import Mock, patch

import pytest

from db_drift.cli.cli import cli_arg_parse
from db_drift.utils.exceptions.cli import CliArgumentError, CliUsageError


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_source_and_target_same_value_error(mock_parse_args: Mock) -> None:
    """Test that source and target cannot be the same."""
    mock_args = argparse.Namespace(
        dbms="sqlite",
        output="drift_report.html",
        source="sqlite:///same.db",
        target="sqlite:///same.db",  # Same as source
        verbose=False,
    )
    mock_parse_args.return_value = mock_args

    with pytest.raises(CliUsageError, match="Source and target connection strings must be different"):
        cli_arg_parse()


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
def test_source_and_target_different_dbms_error(mock_parse_args: Mock) -> None:
    """Test that source and target must be of the same DBMS type."""
    test_cases = [
        ("sqlite:///source.db", "postgresql://user:pass@localhost/target"),
        ("postgresql://user:pass@localhost/source", "mysql://user:pass@localhost/target"),
        ("mysql://user:pass@localhost/source", "sqlite:///target.db"),
    ]

    for source, target in test_cases:
        mock_args = argparse.Namespace(
            dbms="sqlite",
            output="drift_report.html",
            source=source,
            target=target,
            verbose=False,
        )
        mock_parse_args.return_value = mock_args

        with pytest.raises(CliArgumentError, match="Source and target databases must be of the same DBMS type"):
            cli_arg_parse()
