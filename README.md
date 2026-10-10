# Weather Summary

This package refactors the AIGC 5005 Lab 02 weather-summary program into an installable Python package. It downloads seven days of hourly weather observations from Open-Meteo, validates them, and writes the same summary structure as Lab 02.

## Data source

The source is the Open-Meteo forecast API for latitude 43.65 and longitude 79.38, requesting hourly temperature and precipitation for the previous seven days in the America/Toronto timezone.

One record represents one hourly observation containing:
- time
- temperature
- precipitation

The normal response contains approximately 168 hourly records.

## Setup

```bash
conda env create -f environment.yml
conda activate weathersummary
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

The result is written to `data/processed/summary.json`.

## Test

```bash
python -m unittest discover -s tests
```

The tests use hand-made records and do not access the network.

## Layout

| Module | Responsibility |
|---|---|
| `src/weathersummary/config.py` | Central URL, timeout, and output-path settings. |
| `src/weathersummary/models.py` | Defines and cleans one `WeatherRecord`. |
| `src/weathersummary/sources.py` | Downloads data from Open-Meteo and converts it to records. This is the only module that imports `requests`. |
| `src/weathersummary/aggregations.py` | Defines the aggregation base class and concrete aggregation subclasses. |
| `src/weathersummary/report.py` | Combines aggregation results and writes JSON output. |
| `src/weathersummary/__init__.py` | Re-exports public classes and functions. |
| `main.py` | Thin entry point and user-facing error messages. |
| `tests/test_models.py` | Offline tests for record cleaning and aggregation behavior. |

## What moved where

| Lab 02 code | Lab 03 location |
|---|---|
| `SOURCE_URL` | `config.py` → `SOURCE_URL` |
| `OUTPUT_FILE` | `config.py` → `OUTPUT_PATH` |
| `download_data()` | `sources.py` → `WeatherSource.download()` |
| `WeatherRecord` namedtuple | `models.py` → `WeatherRecord` class |
| record validation in `process_data()` | `models.py` → `WeatherRecord.__init__()` |
| daily grouping and summary | `aggregations.py` → `DailySummaryAggregation.compute()` |
| temperature categories | `aggregations.py` → `TemperatureCategoryAggregation.compute()` |
| recent 24 temperatures | `aggregations.py` → `RecentTemperaturesAggregation.compute()` |
| overall statistics | `aggregations.py` → `OverallAggregation.compute()` |
| summary construction | `report.py` → `build_summary()` |
| JSON writing | `report.py` → `write_summary()` |
| `main()` | `main.py` → `main()` |

## Design choices

`WeatherRecord` represents one clean weather observation. Its constructor validates the time, temperature, and precipitation values, converts numeric values to `float`, and raises `ValueError` for malformed records. This keeps data cleaning in one place.

`WeatherSource` is responsible only for downloading and converting API data into `WeatherRecord` objects. `requests` is intentionally imported only in `sources.py`.

`Aggregation` is the base class for computations over a list of records. Four subclasses override `compute()`:

- `DailySummaryAggregation`
- `TemperatureCategoryAggregation`
- `RecentTemperaturesAggregation`
- `OverallAggregation`

The report code stores these objects in a list and calls `compute()` on each object without checking which subclass it is. Adding another aggregation requires creating another subclass and adding it to the aggregation list.

The refactored program preserves the Lab 02 summary keys and calculations.

## Known limitations

The Open-Meteo feed is live, so weather values can change between runs. The structure and calculations remain the same, but a newly generated `summary.json` can contain different values from an earlier run.

If the network request fails, the program prints a clear message and exits without a traceback.
