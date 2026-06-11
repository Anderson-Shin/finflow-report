import json
import os
from pathlib import Path
from typing import Any

import requests

from finflow_report.config import SourceConfig


def _expand_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
        key: os.path.expandvars(str(value)) if isinstance(value, str) else value
        for key, value in values.items()
    }


def _select_path(payload: Any, records_path: str) -> Any:
    current = payload
    if records_path:
        for part in records_path.split("."):
            if not isinstance(current, dict) or part not in current:
                raise ValueError(f"records_path '{records_path}' was not found in the response")
            current = current[part]
    if not isinstance(current, list):
        raise ValueError("The selected response value must be a list of records")
    return current


def fetch_records(config: SourceConfig) -> list[dict[str, Any]]:
    if config.type == "json_file":
        with Path(config.path or "").open(encoding="utf-8") as file:
            payload = json.load(file)
    else:
        response = requests.get(
            config.url or "",
            params=_expand_values(config.params),
            headers=_expand_values(config.headers),
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
    return _select_path(payload, config.records_path)
