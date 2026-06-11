# FinFlow Report

[![CI](https://github.com/Anderson-Shin/finflow-report/actions/workflows/ci.yml/badge.svg)](https://github.com/Anderson-Shin/finflow-report/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Turn inconsistent financial API responses into polished Excel reports and interactive
Streamlit dashboards.

## Why FinFlow Report?

Financial analysts often repeat the same fragile workflow: fetch JSON from several APIs,
rewrite field mappings, clean values, format an Excel workbook, and repair chart ranges.
FinFlow Report moves those decisions into a readable YAML file so the pipeline can be
validated, reproduced, and shared.

## Features

- Map nested JSON responses into one consistent table without rewriting Python.
- Load local JSON for reproducible demos or authenticated HTTP JSON APIs.
- Validate required fields, dates, and numeric values with actionable errors.
- Generate a polished Excel workbook with an auto-expanding table and chart.
- Explore the same normalized data in an interactive Streamlit dashboard.
- Add new financial data sources through configuration instead of provider-specific code.

## Quick Start

```bash
git clone https://github.com/Anderson-Shin/finflow-report.git
cd finflow-report
python -m venv .venv
source .venv/bin/activate
pip install -e .
finflow configs/sample.yml
```

The command validates six bundled sample records and creates
`output/sample_report.xlsx`.

Launch the dashboard:

```bash
streamlit run src/finflow_report/dashboard.py
```

## Configuration

Each normalized field points to a nested value in the source response:

```yaml
source:
  type: json_file
  path: ../examples/data/sample_market.json
  records_path: observations

fields:
  date: {source: period.date, type: date}
  close_price: {source: market.close, type: number}

report:
  title: Market Report
  output: output/market_report.xlsx
  sheet_name: Overview
  date_column: date
  metric_columns: [close_price]
```

For authenticated APIs, use environment variables rather than committing keys:

```yaml
source:
  type: http_json
  url: https://api.example.com/v1/observations
  headers:
    Authorization: Bearer ${FINFLOW_API_KEY}
```

See [`examples/http_api.yml`](examples/http_api.yml) for a complete template.

## Project Structure

```text
finflow-report/
├── configs/                 # Ready-to-run pipeline configurations
├── examples/                # Example API config and key-free sample data
├── src/finflow_report/      # Source, normalization, Excel, dashboard, and CLI modules
├── tests/                   # Unit and end-to-end tests
├── CONTRIBUTING.md          # Contribution workflow
└── pyproject.toml           # Package metadata and dependencies
```

## Roadmap

- Provider examples for FRED, Alpha Vantage, BEA, BLS, DART, and KIS
- Response schema-change detection and mapping suggestions
- Multi-sheet reports and reusable Excel themes
- Scheduled refreshes and report snapshots
- Community-maintained adapter and template catalog

See the [project review](docs/PROJECT_REVIEW.md), [growth plan](docs/GROWTH_PLAN.md),
and [Codex for OSS application draft](docs/CODEX_FOR_OSS_APPLICATION.md).

## Contributing

Financial APIs are diverse by nature. Contributions of provider examples, validation
rules, report templates, bug fixes, and documentation are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) to get started.

## Security

Never commit API keys. Please report vulnerabilities according to
[`SECURITY.md`](SECURITY.md).

## License

FinFlow Report is available under the [MIT License](LICENSE).
