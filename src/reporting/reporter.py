import json
import csv
import os
from datetime import datetime
from typing import List
from src.comparator.comparator import LocationDriftReport, MetricDifference


class DriftReportClass:

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def print_console_report(self, reports: List[LocationDriftReport]) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("=" * 55)
        print("               WEATHER DRIFT REPORT   ")
        print("=" * 55)

        for report in reports:
            self._print_location_summary(report)  
            self._print_location_table(report) 

        # total   = len(reports)
        # drifted = sum(1 for r in reports if r.has_drift)
        # clean   = total - drifted
        # print("=" * 55)
        # print("  SUMMARY")
        # print(f"  Locations checked : {total}")
        # print(f"  Drift detected    : {drifted}")
        # print(f"  Clean             : {clean}")
        # print("=" * 55)

    def _print_location_summary(self, report: LocationDriftReport) -> None:
        # Part 1: Summary
        print()
        print(f"  Location = {report.location}")

        for d in report.diffs:
            if d.difference is None:
                if "Humidity" in d.metric:
                    # Meteostat free tier does not return humidity for all locations
                    print(f"  Humidity Difference = N/A (Meteostat did not return humidity)")
                continue

            if "Avg" in d.metric:
                print(f"  Temperature Difference = {d.difference}°F")
            elif "Humidity" in d.metric:
                print(f"  Humidity Difference = {d.difference}%")
            elif "Wind" in d.metric:
                print(f"  Wind Difference = {d.difference} mph")
            elif "Precipitation" in d.metric:
                print(f"  Precipitation Difference = {d.difference} in")

        print()

    def _print_location_table(self, report: LocationDriftReport) -> None:
        # Part 2: full metrics drift table
        print("=" * 55)
        print(f"Location: {report.location}")
        print(f"Date: {report.date}")
        print()
        print(f"{'Metric':<22} {'Source A':>10} {'Source B':>10} {'Diff':>8}")
        print("-" * 55)

        for d in report.diffs:
            val_a = f"{d.source_a_value}" if d.source_a_value is not None else "N/A"
            val_b = f"{d.source_b_value}" if d.source_b_value is not None else "N/A"
            diff  = f"{d.difference}"     if d.difference     is not None else "N/A"
            print(f"{d.metric:<22} {val_a:>10} {val_b:>10} {diff:>8}")

        print()
        status = "DRIFT DETECTED" if report.has_drift else "NO DRIFT"
        print(f"Status: {status}")
        print("=" * 55)
        print()

    def save_json_report(self, reports: List[LocationDriftReport]) -> str:
        output = {
            "generated_at":         datetime.now().isoformat(),
            "total_locations":      len(reports),
            "drift_detected_count": sum(1 for r in reports if r.has_drift),
            "reports":              []
        }
        for report in reports:
            report_dict = {
                "location": report.location,
                "date":     report.date,
                "source_a": report.source_a,
                "source_b": report.source_b,
                "status":   "DRIFT DETECTED" if report.has_drift else "NO DRIFT",
                "metrics":  []
            }
            for d in report.diffs:
                report_dict["metrics"].append({
                    "metric":          d.metric,
                    "source_a_value":  d.source_a_value,
                    "source_b_value":  d.source_b_value,
                    "difference":      d.difference,
                    "drift_detected":  d.drift_detected,
                })
            output["reports"].append(report_dict)

        filepath = os.path.join(self.output_dir, "drift_report.json")
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        print(f"JSON report saved:  {filepath}")
        return filepath

    def save_csv_report(self, reports: List[LocationDriftReport]) -> str:
        filepath = os.path.join(self.output_dir, "drift_report.csv")
        fieldnames = [
            "location", "date", "source_a", "source_b",
            "metric", "source_a_value", "source_b_value",
            "difference", "drift_detected", "location_status"
        ]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for report in reports:
                location_status = "DRIFT DETECTED" if report.has_drift else "NO DRIFT"
                for d in report.diffs:
                    writer.writerow({
                        "location":        report.location,
                        "date":            report.date,
                        "source_a":        report.source_a,
                        "source_b":        report.source_b,
                        "metric":          d.metric,
                        "source_a_value":  d.source_a_value,
                        "source_b_value":  d.source_b_value,
                        "difference":      d.difference,
                        "drift_detected":  d.drift_detected,
                        "location_status": location_status,
                    })
        print(f"CSV report saved:  {filepath}")
        return filepath
