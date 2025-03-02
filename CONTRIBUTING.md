# Contributing to NAOMI API

This guide explains how to contribute to the NAOMI API project.

## Setting up your development environment

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Git

### Fork and clone the repository

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone git@github.com:YOUR_USERNAME/naomi_api.git
   cd naomi_api
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/reubenjohn/naomi_api
   ```

### Install dependencies

```bash
make install
```

This will create a virtual environment using Poetry and install all development dependencies.

## Environment Variables

Set up the required environment variables:

```
SERVICE_ACCOUNT_KEY_PATH=path/to/firebase-service-account.json
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_MODEL=gpt-4
```

## Development workflow

### Create a new branch

```bash
git checkout -b feature/your-feature-name
```

### Run the API server locally

```bash
poetry run api_server
# or with custom host/port
poetry run api_server --host 127.0.0.1 --port 8000
```

### Code formatting and linting

```bash
# Format code
make fmt

# Run linters
make lint
```

The project uses:
- Black for code formatting (line length: 100)
- isort for import sorting
- flake8 for linting
- mypy for type checking

### Running tests

```bash
# Run all tests
make test

# Run a specific test
poetry run pytest tests/test_api.py::test_receive_webhook -v

# Watch tests (rerun on file changes)
make watch
```

### Building documentation

```bash
make docs
```

## Pull Request Process

1. Ensure your code passes all tests and linting
2. Update documentation if necessary
3. Make your commits with clear, descriptive messages following [conventional commits](https://www.conventionalcommits.org/)
4. Push your changes to your fork
5. Submit a pull request to the main repository

## Code Style Guidelines

- Use type annotations for all function parameters and return values
- Follow PEP 8 style guidelines (enforced by flake8)
- Organize imports into three groups: standard library, third-party, local
- Write docstrings for all public functions, classes, and methods
- Include meaningful test cases for new functionality

## Creating a new release

This project uses semantic versioning (MAJOR.MINOR.PATCH).

To create a new release:

1. Ensure all tests pass
2. Run `make release`
3. Enter the new version number when prompted

## Makefile utilities

```bash
make help             # Show available commands
make install          # Install the project in dev mode
make fmt              # Format code using black & isort
make lint             # Run pep8, black, mypy linters
make test             # Run tests and generate coverage report
make watch            # Run tests on every change
make clean            # Clean unused files
make release          # Create a new tag for release
make docs             # Build the documentation
```