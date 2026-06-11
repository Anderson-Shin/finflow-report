from pathlib import Path

from finflow_report.pipeline import run_pipeline


def test_sample_pipeline_creates_excel(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    config = Path(__file__).parents[1] / "configs" / "sample.yml"

    frame, output = run_pipeline(config)

    assert len(frame) == 6
    assert output.exists()
    assert output.stat().st_size > 0
