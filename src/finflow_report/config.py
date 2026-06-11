from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator


class SourceConfig(BaseModel):
    type: Literal["json_file", "http_json"]
    path: str | None = None
    url: str | None = None
    records_path: str = ""
    headers: dict[str, str] = Field(default_factory=dict)
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_location(self) -> "SourceConfig":
        if self.type == "json_file" and not self.path:
            raise ValueError("json_file sources require 'path'")
        if self.type == "http_json" and not self.url:
            raise ValueError("http_json sources require 'url'")
        return self


class FieldConfig(BaseModel):
    source: str
    type: Literal["string", "number", "date"] = "string"
    required: bool = True


class ReportConfig(BaseModel):
    title: str = "FinFlow Report"
    output: str = "output/finflow_report.xlsx"
    sheet_name: str = "Data"
    date_column: str
    metric_columns: list[str]


class PipelineConfig(BaseModel):
    source: SourceConfig
    fields: dict[str, FieldConfig]
    report: ReportConfig


def load_config(path: str | Path) -> PipelineConfig:
    config_path = Path(path).resolve()
    with config_path.open(encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    config = PipelineConfig.model_validate(raw)
    if config.source.path:
        source_path = Path(config.source.path)
        if not source_path.is_absolute():
            config.source.path = str((config_path.parent / source_path).resolve())
    return config
