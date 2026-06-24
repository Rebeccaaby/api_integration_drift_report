from src.config.configloader import load_config
from src.providers.provider_factory import get_provider
from src.comparator.comparator import WeatherCompareEngine
from src.reporting.reporter import DriftReportClass


def run():
    print("Weather Drift Report\n")

    # 1.Load config + secrets
    config      = load_config()
    locations   = config["locations"]
    sources     = config["weather_sources"]
    api_keys    = config["api_keys"]
    target_date = config["target_date"]

    print(f"Date      : {target_date}")
    print(f"Locations : {[l['code'] for l in locations]}")
    print(f"Sources   : {sources}\n")

    # 2.Fetch weather from all providers for all locations
    comparator  = WeatherCompareEngine()
    reporter    = DriftReportClass(output_dir="reports")
    all_reports = []

    for location in locations:
        code = location["code"]
        lat  = location["latitude"]
        lon  = location["longitude"]

        print(f"Fetching data for {code}")

        records = {}
        for source in sources:
            try:
                provider = get_provider(source, api_keys[source])
                record   = provider.get_weather(code, lat, lon, target_date)
                records[source] = record
                print(f"  {source:<10} -> avg={record.avg_temp_f}F  "
                      f"max={record.max_temp_f}F  min={record.min_temp_f}F  "
                      f"humidity={record.humidity}%  "
                      f"precip={record.precipitation_in}in  "
                      f"wind={record.wind_mph}mph")
            except Exception as e:
                print(f"  {source:<10} -> ERROR: {e}")
                records[source] = None

        # 3.Compare two sources
        source_a, source_b = sources[0], sources[1]
        rec_a = records.get(source_a)
        rec_b = records.get(source_b)

        if rec_a and rec_b:
            drift_report = comparator.compare(rec_a, rec_b)
            all_reports.append(drift_report)
        else:
            print(f" Skipping comparison for {code} — missing data from one source\n")

        print()

    # 4.Generate all reports
    if all_reports:
        reporter.print_console_report(all_reports)
        reporter.save_json_report(all_reports)
        reporter.save_csv_report(all_reports)
        print("\nDONE. Reports saved under reports/")
    else:
        print("No reports generated — check API errors above.")


if __name__ == "__main__":
    run()
