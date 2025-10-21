<!-- omit in toc -->
# DB Drift

[![PyPI version](https://badge.fury.io/py/db-drift.svg)](https://badge.fury.io/py/db-drift)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Downloads](https://pepy.tech/badge/db-drift)](https://pepy.tech/project/db-drift)
[![CI](https://github.com/dyka3773/db-drift/workflows/CI/badge.svg)](https://github.com/dyka3773/db-drift/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A command-line tool to visualize the differences between two DB states.

<!-- omit in toc -->
## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [How to Use](#how-to-use)
- [Examples](#examples)
- [Options](#options)
  - [Supported DBMS Types](#supported-dbms-types)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Getting Help](#getting-help)
- [Contributing](#contributing)
- [License](#license)


## Installation

Install the package from PyPI:

```bash
# Using pip
pip install db-drift

# Using pipx
pipx install db-drift

# Using poetry
poetry add db-drift

# Using pipenv
pipenv install db-drift

# Using uv
uv add db-drift
```

## Features
- Compare two database states and visualize the differences.

## How to Use

Basic usage:

```bash
db-drift --source "source.db" --target "target.db"
```

The tool will generate an HTML report showing the differences between the two database states.

## Examples

```bash
# Compare two SQLite databases
db-drift --source "old_version.db" --target "new_version.db"

# Specify custom output file
db-drift --source "db1.db" --target "db2.db" --output "my_report.html"

# Show version information
db-drift --version
```

## Options

| Option | Description | Default | Required |
|--------|-------------|---------|----------|
| `-v`, `--version` | Show version information and exit | - | No |
| `--dbms` | Specify the type of DBMS | `sqlite` | No |
| `-o`, `--output` | Output filename for the drift report | `drift_report.html` | No |
| `--source` | Connection string for the source database | - | **Yes** |
| `--target` | Connection string for the target database | - | **Yes** |
| `--verbose` | Enable verbose logging output | No | No |

### Supported DBMS Types

Currently supported database management systems:
- `sqlite` - SQLite databases
- `oracle` - Oracle databases

*Note: Support for PostgreSQL and MySQL is planned for future releases.*

## Troubleshooting

### Common Issues

### Getting Help

- Check the [examples](examples/) directory for working samples
- Review the [issues](https://github.com/dyka3773/db-drift/issues) page for known problems
- Create a new issue if you encounter a bug or have a feature request

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.