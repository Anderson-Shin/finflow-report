from pathlib import Path

import pandas as pd

from finflow_report.config import ReportConfig


def write_excel(frame: pd.DataFrame, config: ReportConfig) -> Path:
    output = Path(config.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output, engine="xlsxwriter", datetime_format="yyyy-mm-dd") as writer:
        workbook = writer.book
        sheet = workbook.add_worksheet(config.sheet_name)
        writer.sheets[config.sheet_name] = sheet

        title_format = workbook.add_format(
            {"bold": True, "font_size": 18, "font_color": "#FFFFFF", "bg_color": "#17365D"}
        )
        note_format = workbook.add_format({"font_color": "#666666", "italic": True})
        sheet.merge_range(0, 0, 0, max(len(frame.columns) - 1, 3), config.title, title_format)
        sheet.write(1, 0, f"Generated from {len(frame):,} normalized records", note_format)

        frame.to_excel(writer, sheet_name=config.sheet_name, startrow=3, index=False)
        rows, columns = frame.shape
        sheet.add_table(
            3,
            0,
            3 + rows,
            columns - 1,
            {
                "name": "FinFlowData",
                "style": "Table Style Medium 2",
                "columns": [{"header": column} for column in frame.columns],
            },
        )
        sheet.freeze_panes(4, 1)

        for index, column in enumerate(frame.columns):
            width = min(max(len(column) + 2, frame[column].astype(str).map(len).max() + 2), 28)
            cell_format = None
            if pd.api.types.is_numeric_dtype(frame[column]):
                cell_format = workbook.add_format({"num_format": "#,##0.00"})
            sheet.set_column(index, index, width, cell_format)

        chart = workbook.add_chart({"type": "line"})
        date_index = frame.columns.get_loc(config.date_column)
        for metric in config.metric_columns:
            metric_index = frame.columns.get_loc(metric)
            chart.add_series(
                {
                    "name": [config.sheet_name, 3, metric_index],
                    "categories": [config.sheet_name, 4, date_index, 3 + rows, date_index],
                    "values": [config.sheet_name, 4, metric_index, 3 + rows, metric_index],
                }
            )
        chart.set_title({"name": config.title})
        chart.set_legend({"position": "bottom"})
        chart.set_style(10)
        sheet.insert_chart(3, columns + 1, chart, {"x_scale": 1.5, "y_scale": 1.4})
    return output
