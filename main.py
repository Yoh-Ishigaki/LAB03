from weathersummary import WeatherSource, build_summary, write_summary
from weathersummary.config import OUTPUT_PATH


def main():
    try:
        records = WeatherSource().fetch_records()
    except ValueError as exc:
        print(f"Download failed: {exc}")
        return

    if records is None:
        return

    try:
        summary = build_summary(records)
    except ValueError as exc:
        print(f"Download failed: {exc}")
        return

    try:
        write_summary(summary)
    except OSError as exc:
        print(f"Could not write output file: {exc}")
        return

    print(
        f"Success: processed {summary['records_processed']} valid "
        f"records and wrote {OUTPUT_PATH}."
    )


if __name__ == "__main__":
    main()
