import pandas as pd
import pytest

from finflow_report.config import FieldConfig
from finflow_report.normalize import normalize_records

FIELDS = {
    "date": FieldConfig(source="period.date", type="date"),
    "value": FieldConfig(source="metrics.value", type="number"),
}


def test_normalizes_nested_records() -> None:
    frame = normalize_records(
        [{"period": {"date": "2025-01-01"}, "metrics": {"value": "42.5"}}], FIELDS
    )

    assert frame.loc[0, "value"] == 42.5
    assert pd.api.types.is_datetime64_any_dtype(frame["date"])


def test_reports_missing_required_values() -> None:
    with pytest.raises(ValueError, match="'value' has 1 missing required"):
        normalize_records([{"period": {"date": "2025-01-01"}}], FIELDS)
