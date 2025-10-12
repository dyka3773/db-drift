"""Tests for CLI --version/-v flag functionality."""

import re
import subprocess
import sys
from unittest.mock import Mock, patch

import pytest
from db_drift.cli.utils import get_version

EXPECTED_VERSION_OUTPUT_PARTS = 2


def is_valid_version_string(version: str) -> bool:
    """Check if the version string is valid (PEP 440 or 'unknown')."""
    if version == "unknown":
        return True
    # PEP 440 version regex (simplified, covers most cases)
    pep440_regex = (
        r"^(?:[1-9]\d*|0)(?:\.(?:[1-9]\d*|0))*"
        r"(?:a\d+|b\d+|rc\d+|\.post\d+|\.dev\d+)?(?:\+\w+)?$"
    )
    return re.match(pep440_regex, version) is not None


def test_get_version_function_returns_string() -> None:
    """Test that get_version() returns a valid version string."""
    version = get_version()
    assert isinstance(version, str)
    assert len(version) > 0
    # Should either be a proper version (like "1.6.0") or "unknown"

    assert is_valid_version_string(version)


@patch("db_drift.cli.utils.metadata.version")
def test_get_version_handles_package_not_found(mock_version: Mock) -> None:
    """
    Test that get_version() handles PackageNotFoundError gracefully.

    Args:
        mock_version: Mocked version function that raises PackageNotFoundError.
    """
    from importlib.metadata import PackageNotFoundError  # noqa: PLC0415

    mock_version.side_effect = PackageNotFoundError("Package not found")

    version = get_version()
    assert version == "unknown"


@patch("db_drift.cli.utils.metadata.version")
def test_get_version_returns_correct_version(mock_version: Mock) -> None:
    """
    Test that get_version() returns the mocked version.

    Args:
        mock_version: Mocked version function.
    """
    mock_version.return_value = "1.0.0"

    version = get_version()
    assert version == "1.0.0"
    mock_version.assert_called_once_with("db-drift")


def test_version_flag_via_cmd() -> None:
    """Test --version flag via subprocess."""
    try:
        result = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "db_drift",
                "--version",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
            cwd=".",
        )

        # Should exit with code 0 (success)
        assert result.returncode == 0

        # Should output version information
        assert "db-drift" in result.stdout

        output = result.stdout.strip()
        parts = output.split()
        assert len(parts) == EXPECTED_VERSION_OUTPUT_PARTS  # Should be two parts: "db-drift" and version number
        # Second part should be version number
        version_part = parts[1]
        assert len(version_part) > 0

        # Should not have stderr output for normal version display
        # Accept RuntimeWarning about 'db_drift.__main__' in sys.modules
        if result.stderr:
            assert "RuntimeWarning" in result.stderr
            assert "'db_drift.__main__' found in sys.modules" in result.stderr

    except subprocess.TimeoutExpired:
        pytest.fail("--version command timed out")
    except FileNotFoundError:
        pytest.skip("db_drift module not available for subprocess testing")
