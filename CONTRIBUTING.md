# Contributing to RWA

Welcome! We're excited that you're interested in contributing to the Rural Water Association Digital Transformation Platform. Every contribution helps rural water systems operate more effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Development Setup](#development-setup)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@visionblox.io.

---

## How to Contribute

There are many ways to contribute:

- **Report bugs** — Found something broken? Let us know
- **Suggest features** — Ideas for improvements are always welcome
- **Improve documentation** — Clearer docs help everyone
- **Write code** — Fix bugs, add features, improve performance
- **Review pull requests** — Fresh eyes catch issues
- **Share expertise** — Water industry knowledge is invaluable

---

## Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

**To report a bug:**

1. Go to [Issues](https://github.com/khaaliswooden-max/rwa/issues)
2. Click "New Issue"
3. Select "Bug Report" template
4. Fill out all sections completely
5. Add appropriate labels (domain: nrw/energy/compliance)

**A good bug report includes:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, browser)
- Screenshots if applicable
- Relevant log output

---

## Suggesting Features

We prioritize features that benefit small rural water systems within their operational constraints.

**To suggest a feature:**

1. Go to [Issues](https://github.com/khaaliswooden-max/rwa/issues)
2. Click "New Issue"
3. Select "Feature Request" template
4. Explain the problem you're trying to solve
5. Describe your proposed solution
6. Note MVRI compatibility (can it work with minimal infrastructure?)

**Strong feature requests:**
- Solve a real operational problem
- Work within typical rural system constraints
- Have clear acceptance criteria
- Consider data requirements realistically

---

## Development Setup

### Prerequisites

- Python 3.11 or 3.12
- Node.js 20+
- PostgreSQL 15+ with TimescaleDB
- Git

### Local Environment Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/rwa.git
cd rwa

# 2. Add upstream remote
git remote add upstream https://github.com/khaaliswooden-max/rwa.git

# 3. Create Python virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Install Python dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Install frontend dependencies
cd frontend
npm install
cd ..

# 6. Set up environment variables
cp .env.example .env
# Edit .env with your local database credentials

# 7. Initialize database
createdb rwa_dev
python scripts/init_db.py

# 8. Run tests to verify setup
pytest

# 9. Start development servers
python -m uvicorn api.main:app --reload &
cd frontend && npm run dev
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## Branch Naming Convention

Use descriptive branch names with the following prefixes:

| Prefix | Use Case | Example |
|--------|----------|---------|
| `feature/` | New functionality | `feature/mnf-analysis-dashboard` |
| `bugfix/` | Bug fixes | `bugfix/water-balance-calculation-error` |
| `hotfix/` | Critical production fixes | `hotfix/compliance-deadline-crash` |
| `docs/` | Documentation only | `docs/api-examples-update` |
| `refactor/` | Code improvement, no behavior change | `refactor/pump-optimizer-cleanup` |
| `test/` | Test additions/improvements | `test/energy-module-coverage` |

**Format:** `prefix/short-descriptive-name`

---

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Build process, auxiliary tools |
| `ci` | CI configuration |

### Scopes

- `nrw` — Non-Revenue Water module
- `energy` — Energy management module
- `compliance` — Compliance module
- `api` — API gateway
- `frontend` — React frontend
- `db` — Database schemas/migrations
- `infra` — Infrastructure, deployment

### Examples

```bash
# Feature
feat(nrw): add minimum night flow detection algorithm

# Bug fix
fix(energy): correct pump power calculation for variable speed drives

# Documentation
docs(api): add water balance endpoint examples

# Breaking change (note the !)
feat(api)!: change authentication from API key to JWT
```

---

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest `main`
2. **Run the full test suite** — `pytest`
3. **Run linters** — `black . && isort . && flake8`
4. **Update documentation** if needed
5. **Update CHANGELOG.md** under `[Unreleased]`

### Submitting

1. Push your branch to your fork
2. Open a Pull Request against `main`
3. Fill out the PR template completely
4. Request review from maintainers
5. Address review feedback

### Review Criteria

PRs are evaluated on:

- **Correctness** — Does it work as intended?
- **Tests** — Are there adequate tests?
- **Documentation** — Is usage clear?
- **Style** — Does it follow project conventions?
- **MVRI Compatibility** — Can it work with minimal infrastructure?
- **Performance** — Any unnecessary overhead?

### Merge Requirements

- At least 1 approving review
- All CI checks passing
- No merge conflicts
- CHANGELOG updated

---

## Code Style

### Python

We use automated formatting tools. Run before committing:

```bash
# Format code
black .

# Sort imports
isort .

# Check for issues
flake8

# Type checking (optional but encouraged)
mypy src/
```

**Configuration files:** `pyproject.toml`, `.flake8`

**Key conventions:**
- Line length: 88 characters (Black default)
- Imports: standard library → third-party → local (isort handles this)
- Type hints: encouraged for public APIs
- Docstrings: Google style

### JavaScript/TypeScript

```bash
cd frontend

# Format
npm run format

# Lint
npm run lint

# Type check
npm run typecheck
```

**Configuration files:** `.prettierrc`, `.eslintrc.js`, `tsconfig.json`

**Key conventions:**
- Prettier for formatting
- ESLint for code quality
- TypeScript strict mode

---

## Testing Requirements

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific module
pytest tests/test_nrw/

# Specific test
pytest tests/test_nrw/test_water_balance.py::test_calculate_real_losses
```

### Coverage Requirements

- **Minimum coverage: 80%** — PRs below this will fail CI
- New features must include tests
- Bug fixes should include regression tests

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── test_nrw/             # NRW module tests
├── test_energy/          # Energy module tests
├── test_compliance/      # Compliance module tests
├── test_api/             # API endpoint tests
└── integration/          # Cross-module tests
```

### Writing Good Tests

```python
def test_water_balance_calculates_real_losses():
    """Real losses should equal system input minus authorized consumption minus apparent losses."""
    # Arrange
    system_input = 1000  # cubic meters
    authorized_consumption = 800
    apparent_losses = 50
    
    # Act
    result = calculate_water_balance(system_input, authorized_consumption, apparent_losses)
    
    # Assert
    assert result.real_losses == 150
    assert result.nrw_percentage == 20.0
```

---

## Questions?

- **General questions:** Open a [Discussion](https://github.com/khaaliswooden-max/rwa/discussions)
- **Bug or feature:** Open an [Issue](https://github.com/khaaliswooden-max/rwa/issues)
- **Security concerns:** Email security@visionblox.io (see [SECURITY.md](SECURITY.md))

Thank you for contributing to better water infrastructure for rural communities! 💧

