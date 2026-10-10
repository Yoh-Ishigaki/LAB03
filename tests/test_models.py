import unittest

from weathersummary import (
    DailySummaryAggregation,
    OverallAggregation,
    TemperatureCategoryAggregation,
    WeatherRecord,
)


class WeatherRecordTests(unittest.TestCase):
    def test_record_converts_numbers_and_has_string_representation(self):
        record = WeatherRecord(
            "2026-10-01T12:00",
            12,
            0.5,
        )

        self.assertEqual(record.temperature, 12.0)
        self.assertEqual(record.precipitation, 0.5)
        self.assertIn("2026-10-01T12:00", str(record))

    def test_record_rejects_malformed_temperature(self):
        with self.assertRaises(ValueError):
            WeatherRecord("2026-10-01T12:00", "bad", 0.5)


class AggregationTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            WeatherRecord("2026-10-01T00:00", -2, 1),
            WeatherRecord("2026-10-01T01:00", 8, 0),
            WeatherRecord("2026-10-01T02:00", 15, 2),
            WeatherRecord("2026-10-01T03:00", 22, 0),
        ]

    def test_temperature_categories(self):
        result = TemperatureCategoryAggregation(self.records).compute()

        self.assertEqual(
            result,
            {
                "below_freezing": 1,
                "cool": 1,
                "mild": 1,
                "warm": 1,
            },
        )

    def test_overall_statistics(self):
        result = OverallAggregation(self.records).compute()

        self.assertEqual(result["average_temperature"], 10.75)
        self.assertEqual(result["total_precipitation"], 3)
        self.assertEqual(result["maximum_temperature"], 22.0)
        self.assertEqual(result["minimum_temperature"], -2.0)

    def test_daily_summary(self):
        result = DailySummaryAggregation(self.records).compute()

        self.assertEqual(result["2026-10-01"]["record_count"], 4)
        self.assertEqual(result["2026-10-01"]["average_temperature"], 10.75)
        self.assertEqual(result["2026-10-01"]["total_precipitation"], 3.0)


if __name__ == "__main__":
    unittest.main()
