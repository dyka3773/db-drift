import argparse
from unittest.mock import Mock, patch

import pytest
from db_drift.cli.cli import cli_arg_parse
from db_drift.utils.exceptions.cli import CliUsageError


@patch("db_drift.cli.cli.argparse.ArgumentParser.parse_args")
@pytest.mark.skip(reason="We have disabled strict connection string validation for now for testing purposes.")
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
