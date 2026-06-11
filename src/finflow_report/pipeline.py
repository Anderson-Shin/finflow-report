from pathlib import Path

import pandas as pd

from finflow_report.config import PipelineConfig, load_config
from finflow_report.excel import write_excel
from finflow_report.normalize import normalize_records
from finflow_report.source import fetch_records


def run_pipeline(config_path: str | Path) -> tuple[pd.DataFrame, Path]:
    config: PipelineConfig = load_config(config_path)
    records = fetch_records(config.source)
    frame = normalize_records(records, config.fields)
    frame = frame.sort_values(config.report.date_column).reset_index(drop=True)
    output = write_excel(frame, config.report)
    return frame, output
