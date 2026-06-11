# Contributing to FinFlow Report

Thank you for helping make financial data workflows more reproducible.

## Development setup

```bash
git clone https://github.com/Anderson-Shin/finflow-report.git
cd finflow-report
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Good first contributions

- Add a key-free sample response and configuration for a public financial API.
- Improve validation messages for a real-world response shape.
- Add an Excel theme or dashboard visualization.
- Improve documentation and examples.

Do not commit API keys, account identifiers, proprietary data, or responses whose terms
do not permit redistribution.

## Pull requests

Keep changes focused, add tests for behavior changes, and explain the user problem being
solved. Run `pytest` and `ruff check .` before opening a pull request.
