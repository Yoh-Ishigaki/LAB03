from collections import Counter, defaultdict, deque
from abc import ABC, abstractmethod


class Aggregation(ABC):
    """Base class for one calculation performed on weather records."""

    def __init__(self, records):
        """Store the records used by this aggregation."""
        self.records = list(records)

    @abstractmethod
    def compute(self):
        """Return this aggregation's result."""
        raise NotImplementedError


class DailySummaryAggregation(Aggregation):
    """Calculate record counts, average temperature and precipitation by day."""

    def compute(self):
        daily_records = defaultdict(list)

        for record in self.records:
            date = record.time.split("T")[0]
            daily_records[date].append(record)

        return {
            date: {
                "record_count": len(day_records),
                "average_temperature": round(
                    sum(r.temperature for r in day_records) / len(day_records), 2
                ),
                "total_precipitation": round(
                    sum(r.precipitation for r in day_records), 2
                ),
            }
            for date, day_records in daily_records.items()
        }


class TemperatureCategoryAggregation(Aggregation):
    """Count observations in the Lab 02 temperature categories."""

    def compute(self):
        categories = Counter()

        for record in self.records:
            if record.temperature < 0:
                category = "below_freezing"
            elif record.temperature < 10:
                category = "cool"
            elif record.temperature < 20:
                category = "mild"
            else:
                category = "warm"

            categories[category] += 1

        return dict(categories)


class RecentTemperaturesAggregation(Aggregation):
    """Return the most recent 24 temperatures."""

    def compute(self):
        recent = deque(
            (record.temperature for record in self.records),
            maxlen=24,
        )
        return list(recent)


class OverallAggregation(Aggregation):
    """Calculate overall temperature and precipitation statistics."""

    def compute(self):
        return {
            "average_temperature": round(
                sum(record.temperature for record in self.records)
                / len(self.records),
                2,
            ),
            "total_precipitation": round(
                sum(record.precipitation for record in self.records),
                2,
            ),
            "maximum_temperature": max(
                record.temperature for record in self.records
            ),
            "minimum_temperature": min(
                record.temperature for record in self.records
            ),
        }
