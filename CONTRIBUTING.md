<!-- omit in toc -->
# Contributing to db-drift

First of all, thank you for considering contributing to db-drift! It's people like you that make open source so great.

<!-- omit in toc -->
## Table of Contents
- [Where do I go from here?](#where-do-i-go-from-here)
  - [1. Fork \& create a branch](#1-fork--create-a-branch)
  - [2. Get the code](#2-get-the-code)
  - [3. Set up the development environment](#3-set-up-the-development-environment)
  - [4. Make your changes](#4-make-your-changes)
  - [5. Run the tests](#5-run-the-tests)
  - [6. Commit and push your changes](#6-commit-and-push-your-changes)
  - [7. Create a Pull Request](#7-create-a-pull-request)
- [Style guide](#style-guide)
- [Code of Conduct](#code-of-conduct)


## Where do I go from here?

If you've noticed a bug or have a feature request, [make one](https://github.com/dyka3773/db-drift/issues/new)! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

### 1. Fork & create a branch

If this is something you think you can fix, then [fork `db-drift`](https://github.com/dyka3773/db-drift/fork) and create a branch with a descriptive name.

A good branch name would be (where issue #123 is the ticket you're working on):

```bash
git checkout -b 123-add-a-feature
```

### 2. Get the code

```bash
git clone https://github.com/your-username/db-drift.git
cd db-drift
```

### 3. Set up the development environment

We use `uv` for dependency management. To set up the development environment, run:

```bash
uv sync --dev
```

This will install all the necessary dependencies for development, including the ones for running tests and linting.

### 4. Make your changes

Make your changes in the codebase. Make sure to add tests for your changes if applicable. Follow the existing code style and conventions.

### 5. Run the tests

To run the tests, run:

```bash
pytest
```

### 6. Commit and push your changes

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages to enable automatic versioning and changelog generation.

**Commit Message Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature (triggers minor version bump)
- `fix`: A bug fix (triggers patch version bump)
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance (triggers patch version bump)
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools
- `ci`: Changes to CI configuration files and scripts

**Examples:**
```bash
feat: add theme support with --theme option
fix: resolve dependency parsing error with special characters
docs: update README with new theme examples
chore: update dependencies to latest versions
```

**BREAKING CHANGES:**
For breaking changes, add `!` after the type or include `BREAKING CHANGE:` in the footer:
```bash
feat!: change CLI interface for better usability
# or
feat: change CLI interface

BREAKING CHANGE: --output-format flag renamed to --format
```

```bash
git commit -m "feat: add your new feature description"
git push origin 123-add-a-feature
```

### 7. Create a Pull Request

Go to the GitHub repository and create a pull request.

## Style guide

We use `ruff` for linting and formatting. Please make sure your code conforms to the style guide by running:

```bash
ruff check .
ruff format .
```

## Code of Conduct

We have a [Code of Conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.