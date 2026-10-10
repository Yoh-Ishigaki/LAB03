import json

from .aggregations import (
    DailySummaryAggregation,
    OverallAggregation,
    RecentTemperaturesAggregation,
    TemperatureCategoryAggregation,
)
from .config import OUTPUT_PATH, SOURCE_URL


def build_summary(records, invalid_records_skipped=0):
    """Build the same summary structure produced by Lab 02."""
    if not records:
        raise ValueError("no valid weather records were found")

    aggregations = [
        DailySummaryAggregation(records),
        TemperatureCategoryAggregation(records),
        RecentTemperaturesAggregation(records),
        OverallAggregation(records),
    ]

    results = [aggregation.compute() for aggregation in aggregations]

    daily_summary, temperature_categories, recent_temperatures, overall = results

    unique_dates = list(
        dict.fromkeys(record.time.split("T")[0] for record in records)
    )

    return {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
        "invalid_records_skipped": invalid_records_skipped,
        "days_processed": len(unique_dates),
        "daily_summary": daily_summary,
        "temperature_categories": temperature_categories,
        "overall": overall,
        "most_recent_24_temperatures": recent_temperatures,
    }


def write_summary(summary, output_path=OUTPUT_PATH):
    """Write a summary dictionary to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
