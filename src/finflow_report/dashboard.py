import os

import plotly.express as px
import streamlit as st

from finflow_report.config import load_config
from finflow_report.normalize import normalize_records
from finflow_report.source import fetch_records


def main() -> None:
    st.set_page_config(page_title="FinFlow Report", page_icon="📈", layout="wide")
    st.title("FinFlow Report")
    config_path = st.sidebar.text_input(
        "Configuration path", os.getenv("FINFLOW_CONFIG", "configs/sample.yml")
    )

    try:
        config = load_config(config_path)
        frame = normalize_records(fetch_records(config.source), config.fields)
        frame = frame.sort_values(config.report.date_column)
    except Exception as exc:
        st.error(f"Pipeline validation failed: {exc}")
        st.stop()

    metrics = config.report.metric_columns
    columns = st.columns(len(metrics))
    for column, metric in zip(columns, metrics, strict=True):
        latest = frame[metric].dropna().iloc[-1]
        column.metric(metric.replace("_", " ").title(), f"{latest:,.2f}")

    selected = st.multiselect("Metrics", metrics, default=metrics)
    if selected:
        long_frame = frame.melt(
            id_vars=config.report.date_column,
            value_vars=selected,
            var_name="metric",
            value_name="value",
        )
        figure = px.line(
            long_frame,
            x=config.report.date_column,
            y="value",
            color="metric",
            title=config.report.title,
        )
        st.plotly_chart(figure, width="stretch")
    st.dataframe(frame, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
