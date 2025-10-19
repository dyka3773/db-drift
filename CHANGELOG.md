# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v1.2.0](https://github.com/dyka3773/db-drift/releases/tag/v1.2.0) - 2025-10-19

<small>[Compare with v1.1.0](https://github.com/dyka3773/db-drift/compare/v1.1.0...v1.2.0)</small>

### Features

- Using argparse add arguments for Verbosity/log level Fixes #5 ([35a15d1](https://github.com/dyka3773/db-drift/commit/35a15d1d346fd5a27583e083389d6c8269c0bb7d) by Hercules Konsoulas).
- add source, target & output file options in the cli and add some validation that the  source and target dbs are of the same type ([ecc61a3](https://github.com/dyka3773/db-drift/commit/ecc61a36666d2c42b92e6350a250e26ef209834e) by Hercules Konsoulas).
- add arguments for DBMS type ([35cf63b](https://github.com/dyka3773/db-drift/commit/35cf63b774580155897dc03a94608be8fd16eb50) by Hercules Konsoulas).
- add CLI version info ([1f77939](https://github.com/dyka3773/db-drift/commit/1f77939e7880aeda4c1c6cf41a7e3cb326c09914) by Hercules Konsoulas).
- add basic cli parsing ([c6ae7cd](https://github.com/dyka3773/db-drift/commit/c6ae7cd3f766e500f9ee355985df10e0d38a2be3) by Hercules Konsoulas).
- add app entrypoint ([98bd1ed](https://github.com/dyka3773/db-drift/commit/98bd1ed30193dedb4b574951e4cf0a4bde9e4261) by Hercules Konsoulas).

### Bug Fixes

- add copilot suggestions for custom exceptions' constructors ([1b07656](https://github.com/dyka3773/db-drift/commit/1b0765650de4116c9b385a3d3bc984ac37ea7b2b) by Hercules Konsoulas).
- Correct how logs are presented to the user by keeping only INFO (and above) logs on the console and log everything including stacktraces only in the logfile ([8861855](https://github.com/dyka3773/db-drift/commit/8861855d9d751da82be6a6c6b7285457638e6cf7) by Hercules Konsoulas).
- make `--dbms` option mandatory ([ca0f94e](https://github.com/dyka3773/db-drift/commit/ca0f94ea3b44e2f67eb66189562d331e52ebc34e) by Hercules Konsoulas).
- Fix bug where args is treated as dictionary instead of Namespace object ([f1505b7](https://github.com/dyka3773/db-drift/commit/f1505b7ce83d3fefbef5a46a7f8bd7774744a190) by Hercules Konsoulas).

### Code Refactoring

- add suggestions by copilot ([c8c8cb2](https://github.com/dyka3773/db-drift/commit/c8c8cb2ffc9b9a20ab095dc674bd4e27e9e98297) by Hercules Konsoulas).
- move constants to the utils package ([737f7d2](https://github.com/dyka3773/db-drift/commit/737f7d24cce97f817db0df368b256e4471ec48dd) by Hercules Konsoulas).
- move `ExitCode` to the `constants` module ([f9edeb0](https://github.com/dyka3773/db-drift/commit/f9edeb089b5487b5e64bac4fb8dd4004cd1e88cd) by Hercules Konsoulas).
- rename unused (for now) variable to pass ruff checks ([e26a86e](https://github.com/dyka3773/db-drift/commit/e26a86e62995bec0b040e69662dcb19bfd212e2d) by Hercules Konsoulas).

## [v1.1.0](https://github.com/dyka3773/db-drift/releases/tag/v1.1.0) - 2025-10-12

<small>[Compare with v1.0.0](https://github.com/dyka3773/db-drift/compare/v1.0.0...v1.1.0)</small>

### Features

- add global exception handling for CLI errors and possible future issues ([4ecb81b](https://github.com/dyka3773/db-drift/commit/4ecb81b35aa0efc5eeffa9f5c2a0bc7fd0c752c4) by Hercules Konsoulas).
- add logging configuration ([49137a9](https://github.com/dyka3773/db-drift/commit/49137a99df34b326c52818bc9ab880987bac75fb) by Hercules Konsoulas).
- add CLI version info ([50ea4c3](https://github.com/dyka3773/db-drift/commit/50ea4c39a69c75085dedcc20f8d1a3b6ddb95f2c) by Hercules Konsoulas).
- add basic cli parsing ([5af123a](https://github.com/dyka3773/db-drift/commit/5af123ae7cf1eebe8409473e0294d7c4b28b729f) by Hercules Konsoulas).
- add app entrypoint ([2892a15](https://github.com/dyka3773/db-drift/commit/2892a15b1842cda803370d28841e5fbd9c194a39) by Hercules Konsoulas).

### Code Refactoring

- add suggestions by copilot ([7cb4914](https://github.com/dyka3773/db-drift/commit/7cb49148fd084b617d875e9134dc40f5712659d8) by Hercules Konsoulas).
- rename unused (for now) variable to pass ruff checks ([7cac9d5](https://github.com/dyka3773/db-drift/commit/7cac9d5ffaa634d55cfe470caaf80b06bbc3e11b) by Hercules Konsoulas).

## [v1.0.0](https://github.com/dyka3773/db-drift/releases/tag/v1.0.0) - 2025-08-04

<small>[Compare with first commit](https://github.com/dyka3773/db-drift/compare/4741274c923649ec7b499260bc11141a04b5d000...v1.0.0)</small>

