import argparse

from finflow_report.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize financial API data and generate a polished Excel report."
    )
    parser.add_argument("config", help="Path to a FinFlow YAML configuration file")
    args = parser.parse_args()

    frame, output = run_pipeline(args.config)
    print(f"Validated {len(frame):,} records")
    print(f"Excel report created: {output}")


if __name__ == "__main__":
    main()
