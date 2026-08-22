# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->

## v1.5.0 (2026-03-07)

### Documentation

- **oracle**: Added Document Oracle support
  ([`c6dd9f1`](https://github.com/dyka3773/db-drift/commit/c6dd9f14b3e0d8e5103480e51790bfbe28489399))

- **sqlite**: Remove objects that cannot be supported
  ([`3a04e31`](https://github.com/dyka3773/db-drift/commit/3a04e31d198abe13c1a92d8eb225475975dd3c72))

### Features

- **sqlite**: Add support for index extraction
  ([`072f1e0`](https://github.com/dyka3773/db-drift/commit/072f1e0ed4808d26b5dc75e69c8d9ef77e7e87d6))

- **sqlite**: Add support for trigger exporting
  ([`a75f89a`](https://github.com/dyka3773/db-drift/commit/a75f89a12b60385fc6ce338cc7ef5a8346469056))

- **sqlite**: Add support for Views and Tables extraction
  ([`b046986`](https://github.com/dyka3773/db-drift/commit/b046986b4e6d83b36ec267ee4a99a0ace4e3b189))

### Refactoring

- **sqlite**: Changed the way some models are imported and added pydoc in teh generic function that
  returns table or view structure
  ([`abb75e4`](https://github.com/dyka3773/db-drift/commit/abb75e42446009ce7107a8a4c0e17a6f749048fa))

### Testing

- **sqlite**: Add some minor sqlite tests and begin testing in general
  ([`30fc2d8`](https://github.com/dyka3773/db-drift/commit/30fc2d8d87d4fac6202b32496e5e08fa5a84427e))

- **sqlite**: Add testing for index extraction
  ([`a4799c6`](https://github.com/dyka3773/db-drift/commit/a4799c66b53cc4fca8d593903dc9be66359e43f6))

- **sqlite**: Add tests for tables and views
  ([`aa7f724`](https://github.com/dyka3773/db-drift/commit/aa7f7243138b0c59956bd48e5425ac27d7fad0d4))


## v1.4.1 (2026-03-06)

### Bug Fixes

- **oracle**: Correct a query to match the right records on join, avoid sql injection in another
  query and minor typo on a variable
  ([`ed42cb2`](https://github.com/dyka3773/db-drift/commit/ed42cb25c66c430c4845636a72074d90b9a85716))

- **oracle**: Fix how constraints are fetched so that COLUMN_NAME is always fetched
  ([`7f93bbd`](https://github.com/dyka3773/db-drift/commit/7f93bbd90d53a212cb407ed437b3f1d7314f4ef2))

- **oracle**: Fix minor typo in a variable name and add some docs regarding the supported objects
  ([`ddba4b5`](https://github.com/dyka3773/db-drift/commit/ddba4b55597323c8bf35069cedbbd36ebd1d7f76))

- **oracle**: Fix various type inconsistencies
  ([`178540f`](https://github.com/dyka3773/db-drift/commit/178540f1aaebf4ed70e3b3e9d1a92ede22793102))

### Documentation

- **oracle**: Document the logic behind empty string bodies
  ([`75d5a61`](https://github.com/dyka3773/db-drift/commit/75d5a61155e6bdaf437964e317f34c0a27da3f68))

### Performance Improvements

- **oracle**: Add a more robust algorithm for hashing code text
  ([`275d7f5`](https://github.com/dyka3773/db-drift/commit/275d7f5fd63a55236e05483aa9edd35eb653c9c7))

### Refactoring

- Change the DBConstraintTypeEnum to be forward compatible for when the report is going to be
  generated
  ([`df86e73`](https://github.com/dyka3773/db-drift/commit/df86e73cef85f570019bd83334945e1b960a96ee))


## v1.4.0 (2026-03-04)

### Bug Fixes

- **oracle**: Correct the Constraint mapping to show the Enum values
  ([`f13478d`](https://github.com/dyka3773/db-drift/commit/f13478dbb1f0f4cd43995b8985f98f830c3027f3))

### Features

- Add support for database constraints, constraint type mapping between different DBMSs and created
  a new abstract model to distinguish between objects that need column details and objects with just
  column references
  ([`54b4e32`](https://github.com/dyka3773/db-drift/commit/54b4e329bd541f1a61610d79b62c198da9b82852))

- **oracle**: Add support for custom directory export
  ([`014639f`](https://github.com/dyka3773/db-drift/commit/014639fedc85f5f84d73a3dafa76c2fb8a9666d6))

- **oracle**: Add support for custom type extraction
  ([`fc599ec`](https://github.com/dyka3773/db-drift/commit/fc599ec93907ba4c613738e6e3c5bf9271b8497b))

- **oracle**: Add support for oracle sequence exporting
  ([`ee0b57e`](https://github.com/dyka3773/db-drift/commit/ee0b57ec432ff8638e6e9584a6084275dd51c65d))

- **oracle**: Add support for packages
  ([`61a5ab5`](https://github.com/dyka3773/db-drift/commit/61a5ab5ca9a95cc56d9a45142130088d2e43513b))

- **oracle**: Add support for stored functions extraction
  ([`0593635`](https://github.com/dyka3773/db-drift/commit/0593635413e055fc4d321b7a24fbccf6ecbbd8d4))

- **oracle**: Add support for stored procedure extraction
  ([`c186b72`](https://github.com/dyka3773/db-drift/commit/c186b72580b31bf859e9d6eb13c765326678cbb7))

- **oracle**: Add support for synonym extraction
  ([`0bca1ad`](https://github.com/dyka3773/db-drift/commit/0bca1ada6a19d2f725d7d6353d0d90cff562fb30))

### Refactoring

- **oracle**: Use partial function instead of lambda for constraint fetching
  ([`7bee375`](https://github.com/dyka3773/db-drift/commit/7bee3759e43d516a39549ede49a9b55c8267163f))

### Testing

- Fix test import
  ([`fa9e2bf`](https://github.com/dyka3773/db-drift/commit/fa9e2bf2e5b16d4fcf83eb2c2dd45ae4dbd558f6))


## v1.3.8 (2026-03-04)

### Chores

- **ci**: Remove pip group of dependency checks and only keep the uv automation
  ([`9d78f5f`](https://github.com/dyka3773/db-drift/commit/9d78f5f7555aa950f670f0d1f2fc00acec10246e))

### Continuous Integration

- Simplify how project is released
  ([`762fc93`](https://github.com/dyka3773/db-drift/commit/762fc93375f3af57be109c6ca18b38fbcaebcc1f))

### Deps

- Update lockfile
  ([`96788ab`](https://github.com/dyka3773/db-drift/commit/96788abd5155f68b0687b37920c4107f31af9c9b))

### Documentation

- Update changelog for v1.3.7
  ([`00e66ae`](https://github.com/dyka3773/db-drift/commit/00e66ae9fefd2fc35902ee158fa34283b1d673db))


## [v1.3.7](https://github.com/dyka3773/db-drift/releases/tag/v1.3.7) - 2026-03-04

<small>[Compare with v1.3.6](https://github.com/dyka3773/db-drift/compare/v1.3.6...v1.3.7)</small>

## [v1.3.6](https://github.com/dyka3773/db-drift/releases/tag/v1.3.6) - 2026-01-19

<small>[Compare with v1.3.5](https://github.com/dyka3773/db-drift/compare/v1.3.5...v1.3.6)</small>

## [v1.3.5](https://github.com/dyka3773/db-drift/releases/tag/v1.3.5) - 2026-01-12

<small>[Compare with v1.3.4](https://github.com/dyka3773/db-drift/compare/v1.3.4...v1.3.5)</small>

## [v1.3.4](https://github.com/dyka3773/db-drift/releases/tag/v1.3.4) - 2026-01-07

<small>[Compare with v1.3.3](https://github.com/dyka3773/db-drift/compare/v1.3.3...v1.3.4)</small>

## [v1.3.3](https://github.com/dyka3773/db-drift/releases/tag/v1.3.3) - 2025-12-15

<small>[Compare with v1.3.2](https://github.com/dyka3773/db-drift/compare/v1.3.2...v1.3.3)</small>

## [v1.3.2](https://github.com/dyka3773/db-drift/releases/tag/v1.3.2) - 2025-12-02

<small>[Compare with v1.3.1](https://github.com/dyka3773/db-drift/compare/v1.3.1...v1.3.2)</small>

## [v1.3.1](https://github.com/dyka3773/db-drift/releases/tag/v1.3.1) - 2025-11-19

<small>[Compare with v1.3.0](https://github.com/dyka3773/db-drift/compare/v1.3.0...v1.3.1)</small>

## [v1.3.0](https://github.com/dyka3773/db-drift/releases/tag/v1.3.0) - 2025-10-21

<small>[Compare with v1.2.0](https://github.com/dyka3773/db-drift/compare/v1.2.0...v1.3.0)</small>

### Features

- add support for table & view columns extraction and remove DatabaseObject name attribute from all classes in order to use dictionaries for faster lookup ([ececb0b](https://github.com/dyka3773/db-drift/commit/ececb0b610cf77207d2666e5a7c4c10df0edd38f) by Hercules Konsoulas).
- Implement OracleConnector & SQLiteConnector design to fetch db structure and moved stuff around for better clarity and decoupling ([17cf72a](https://github.com/dyka3773/db-drift/commit/17cf72a0b3419432153e67e1b1cf45d3926c1262) by Hercules Konsoulas).
- create placeholder DB Connectors, a factory method to get the appropriate Connector, a placeholder report generator and a simple-lookup registry to register supported DBMSs ([c4d690e](https://github.com/dyka3773/db-drift/commit/c4d690e6deea474c59ff81888a60216b6185b077) by Hercules Konsoulas).
- Create generic DVOs for every Structure that can be found in a database Fixes #11 ([44e0e78](https://github.com/dyka3773/db-drift/commit/44e0e7865660420554cf008eee02454d83a07747) by Hercules Konsoulas).

### Code Refactoring

- add copilot suggestions ([dc37514](https://github.com/dyka3773/db-drift/commit/dc37514eb74e42da4777c7239cd41544db4c9ab0) by Hercules Konsoulas).

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
