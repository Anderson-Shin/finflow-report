# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Use GitHub's private
vulnerability reporting feature for this repository.

Include reproduction steps, affected versions, and potential impact. You can expect an
initial response within seven days.

## API key safety

FinFlow Report expands environment variables at runtime. Keep secrets in environment
variables or local secret stores and never commit them to configuration files.
