Set up a new Python project in the current directory with the following requirements:

## Project initialization

* Initialize a Python project using `uv init --python 3.12` (assume uv is installed)
* Add development dependencies using `uv add --dev`:
  * `pytest` for testing
  * `pytest-cov` for code coverage
  * `black` for code formatting
  * `ruff` for linting

## Source structure

* Confirm the project source folder name with the user. Default: convert $ARGUMENTS from kebab-case to snake_case (e.g., `link-checker` becomes `link_checker`)
* Create the source folder `{project_name}/` with an `__init__.py` file containing:
  ```python
  """Project description."""

  __version__ = "0.1.0"
  ```
* Create `tests/` folder with a dummy test file `test_ci.py`:
  ```python
  """Dummy test to verify CI setup."""


  def test_ci():
      """Dummy test that always passes."""
      assert True
  ```
* Create a new folder `docker/` in the root of the repository. Ensure it's committed to git later.

## Git setup

* Initialize git repository with `git init`
* Create `.git/hooks/pre-commit` (must be executable with `chmod +x`):
  ```bash
  #!/bin/bash
  set -e

  echo "Running pre-commit checks..."

  # Run black on project source and tests only
  echo "Running black..."
  uv run black --check {project_name}/ tests/

  # Run ruff on project source and tests only
  echo "Running ruff..."
  uv run ruff check {project_name}/ tests/

  # Run tests
  echo "Running tests..."
  uv run pytest

  echo "All pre-commit checks passed!"
  ```
  Replace `{project_name}` with the actual confirmed project folder name.

## Standard files

* Create `LICENSE` file with MIT licence template using [year] and [fullname] as placeholders
* Create `README.md` with sections: Project Title (use $ARGUMENTS as title), Description (placeholder), Installation (with git clone and uv sync commands), Usage (placeholder), Testing (show pytest, black, ruff commands), License (reference to MIT). Ensure that the README.md file shows badges for test status, coverage etc.

## CI setup

* Create `.github/workflows/test.yml` that:
  * Triggers on pull_request and push to main branch
  * Uses ubuntu-latest runner
  * Checks out code
  * Installs uv using `astral-sh/setup-uv@v5` with cache enabled
  * Installs Python 3.12 with `uv python install 3.12`
  * Installs dependencies with `uv sync`
  * Runs tests with `uv run pytest`

## Finalisation

* Check for untracked files with `git status`
* Add files individually to git (not with `git add .`):
  * `.github/workflows/test.yml`
  * `LICENSE`
  * `README.md`
  * `{project_name}/__init__.py`
  * `tests/test_ci.py`
  * `pyproject.toml`
  * `.python-version`
  * Any other files created by `uv init` (except `hello.py`, which should be removed)
  * Any other untracked files found in the working directory (except those in .gitignore)
  * Do NOT add `uv.lock` if it's gitignored
  * Do NOT add `.venv/` or other ignored directories
* Commit with message 'initial commit' (exactly, no variations)
* If commit fails due to pre-commit hook issues (formatting/linting), fix them and retry
* Create GitHub repository: `gh repo create $ARGUMENTS --public --source=. --remote=origin`
* Create a label 'epic'
* Push to remote: `git push -u origin main`
* Verify CI runs and passes: `sleep 5 && gh run list --limit 1` then `gh run view {run_id}` to confirm success

Execute these tasks in order. Use appropriate commands and create necessary configuration files. The project should be ready for development after completion.

For the MIT license, use the standard template with [year] and [fullname] as placeholders.

For the README, include placeholder text that can be filled in later.