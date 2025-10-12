<!-- omit in toc -->
# Exception Handling and Error Codes

This document describes the exception handling system and error codes used in db-drift.

<!-- omit in toc -->
## Table of Contents
- [Error Code Standards](#error-code-standards)
  - [Standard Exit Codes](#standard-exit-codes)
- [Exception Hierarchy](#exception-hierarchy)
  - [Base Exceptions](#base-exceptions)
  - [CLI Exceptions](#cli-exceptions)
  - [Database Exceptions](#database-exceptions)
  - [Configuration Exceptions](#configuration-exceptions)
- [Debug Mode](#debug-mode)
- [Error Handling Best Practices](#error-handling-best-practices)
  - [For Developers](#for-developers)
  - [For Users](#for-users)


## Error Code Standards

db-drift follows Unix-style exit codes and BSD sysexits.h standards for consistency. All exit codes are defined in the `ExitCode` enum located in `src/db_drift/utils/exceptions/status_codes.py`.

### Standard Exit Codes

| Exit Code | Constant | Description | Exception Type |
|-----------|----------|-------------|----------------|
| 0 | `ExitCode.SUCCESS` | Success | - |
| 1 | `ExitCode.GENERAL_ERROR` | General error | `DbDriftSystemError`, unexpected errors |
| 2 | `ExitCode.USAGE_ERROR` | CLI usage error | `CliError`, `CliArgumentError`, `CliUsageError` |
| 65 | `ExitCode.DATA_ERROR` | Data format error | `DatabaseSchemaError` |
| 66 | `ExitCode.NO_INPUT` | Cannot open input file | File not found errors |
| 69 | `ExitCode.UNAVAILABLE` | Service unavailable | Database connection failures |
| 70 | `ExitCode.SOFTWARE_ERROR` | Internal software error | `DatabaseQueryError` |
| 77 | `ExitCode.NO_PERMISSION` | Permission denied | File/directory permission errors |
| 78 | `ExitCode.CONFIG_ERROR` | Configuration error | `ConfigError`, `MissingConfigError` |
| 130 | `ExitCode.SIGINT` | User interruption | Ctrl+C (SIGINT) |

## Exception Hierarchy

### Base Exceptions

- `DbDriftError`: Base class for all application exceptions
  - `DbDriftUserError`: User-caused errors (exit code 2)
  - `DbDriftSystemError`: System-level errors (exit code 1)
  - `DbDriftInterruptError`: User interruption (exit code 130)

### CLI Exceptions

- `CliError`: Base CLI exception (exit code 2)
  - `CliArgumentError`: Invalid command-line arguments
  - `CliUsageError`: Incorrect usage patterns
  - `CliConfigError`: CLI configuration issues

### Database Exceptions

- `DatabaseError`: Base database exception (exit code 1)
  - `DatabaseConnectionError`: Connection failures
  - `DatabaseQueryError`: Query execution errors
  - `DatabaseSchemaError`: Schema-related errors
  - `DatabaseAuthenticationError`: Authentication failures
  - `DatabaseTimeoutError`: Operation timeouts

### Configuration Exceptions

- `ConfigError`: Base configuration exception (exit code 2)
  - `MissingConfigError`: Missing required configuration
  - `ConfigValidationError`: Invalid configuration values
  - `ConfigFormatError`: Configuration file format errors

## Debug Mode

Set the environment variable `DB_DRIFT_DEBUG=1` to enable debug mode:

- Shows full Python tracebacks
- Provides detailed error information
- Useful for development and troubleshooting

Example:
```bash
DB_DRIFT_DEBUG=1 db-drift --source db1 --target db2
```

## Error Handling Best Practices

### For Developers

1. **Use specific exceptions**: Choose the most specific exception type
2. **Provide helpful messages**: Include context and suggestions
3. **Set appropriate exit codes**: Follow the standard codes above
4. **Log errors properly**: Use `logger.exception()` for caught exceptions

Example:
```python
try:
    connect_to_database(connection_string)
except ConnectionError as e:
    raise DatabaseConnectionError(
        f"Failed to connect to {host}:{port}",
        host=host,
        port=port,
        database=database_name
    ) from e
```

### For Users

1. **Check exit codes**: Use `echo $?` (Unix) or `echo %ERRORLEVEL%` (Windows)
2. **Enable debug mode**: Set `DB_DRIFT_DEBUG=1` for detailed errors
3. **Read suggestions**: Error messages often include helpful suggestions
4. **Check logs**: Detailed logs are written to `.logs/db-drift.log`
