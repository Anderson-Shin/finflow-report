from typing import Any

import pandas as pd

from finflow_report.config import FieldConfig


def _nested_value(record: dict[str, Any], path: str) -> Any:
    current: Any = record
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def normalize_records(
    records: list[dict[str, Any]], fields: dict[str, FieldConfig]
) -> pd.DataFrame:
    rows = [
        {target: _nested_value(record, field.source) for target, field in fields.items()}
        for record in records
    ]
    frame = pd.DataFrame(rows, columns=list(fields))

    errors: list[str] = []
    for column, field in fields.items():
        if field.required and frame[column].isna().any():
            missing = int(frame[column].isna().sum())
            errors.append(f"'{column}' has {missing} missing required value(s)")
        if field.type == "number":
            converted = pd.to_numeric(frame[column], errors="coerce")
            invalid = converted.isna() & frame[column].notna()
            if invalid.any():
                errors.append(f"'{column}' has {int(invalid.sum())} invalid number value(s)")
            frame[column] = converted
        elif field.type == "date":
            converted = pd.to_datetime(frame[column], errors="coerce")
            invalid = converted.isna() & frame[column].notna()
            if invalid.any():
                errors.append(f"'{column}' has {int(invalid.sum())} invalid date value(s)")
            frame[column] = converted

    if errors:
        raise ValueError("Data validation failed: " + "; ".join(errors))
    return frame
