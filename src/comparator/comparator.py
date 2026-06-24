from dataclasses import dataclass, field
from typing import Optional, List
from src.models.weatherInfo import WeatherInfo


@dataclass
class MetricDifference:
    metric:         str
    source_a_value: Optional[float]
    source_b_value: Optional[float]
    difference:     Optional[float]
    drift_detected: bool


@dataclass
class LocationDriftReport:
    # Drift report for one location comparing two sources
    location: str
    date:     str
    source_a: str
    source_b: str
    diffs:    List[MetricDifference] = field(default_factory=list)
    has_drift: bool = False


class WeatherCompareEngine:
    # Compare two WeatherInfo objects field by field

    # Thresholds per metric
    THRESHOLDS = {
        "avg_temp_f":       2.0,   # degrees F
        "max_temp_f":       2.0,
        "min_temp_f":       2.0,
        "humidity":         5.0,   # percent
        "precipitation_in": 0.1,   # inches
        "wind_mph":         2.0,   # mph
    }

    METRIC_LABELS = {
        "avg_temp_f":       "Avg Temp (F)",
        "max_temp_f":       "Max Temp (F)",
        "min_temp_f":       "Min Temp (F)",
        "humidity":         "Humidity (%)",
        "precipitation_in": "Precipitation (in)",
        "wind_mph":         "Wind (mph)",
    }

    def compare(self, record_a: WeatherInfo, record_b: WeatherInfo) -> LocationDriftReport:
        # Compare two WeatherInfo objects
        if record_a.location != record_b.location:
            raise ValueError(
                f"Location mismatch: {record_a.location} vs {record_b.location}. "
                "Can only compare records for the same location."
            )

        report = LocationDriftReport(
            location=record_a.location,
            date=record_a.date,
            source_a=record_a.source,
            source_b=record_b.source,
        )

        for field_name, label in self.METRIC_LABELS.items():
            val_a = getattr(record_a, field_name)
            val_b = getattr(record_b, field_name)

            if val_a is None or val_b is None:
                diff = MetricDifference(
                    metric=label,
                    source_a_value=val_a,
                    source_b_value=val_b,
                    difference=None,
                    drift_detected=False,
                )
            else:
                difference = round(abs(val_a - val_b), 4)
                threshold  = self.THRESHOLDS.get(field_name, 0)
                is_drift   = difference > threshold

                diff = MetricDifference(
                    metric=label,
                    source_a_value=val_a,
                    source_b_value=val_b,
                    difference=difference,
                    drift_detected=is_drift,
                )

                if is_drift:
                    report.has_drift = True

            report.diffs.append(diff)

        return report
