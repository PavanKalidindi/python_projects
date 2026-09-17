from typing import Any

from weather_api import get_all_cities_weather, weather_statistics, cities, country_city
import json, csv
from pathlib import Path
from datetime import datetime, timedelta

def export_json(data) -> None:
    file = Path(__file__).parent.resolve() / 'cache.json'
    ts = datetime.now().isoformat()

    data = {
        "timestamp": ts,
        "weather_data": data
    }

    with file.open('w', encoding='utf-8') as f:
        try:
            json.dump(data, f, indent=2)
            print("weather data cached")

        except json.JSONDecodeError as e:
            print(f"error caching weather: {e}")

def export_csv(data: dict[str, Any]) -> None:
    file = Path(__file__).parent.resolve() / 'weather_report.csv'
    ts = datetime.now().isoformat()

    file_exists = file.is_file()

    data['timestamp'] = ts
    fields = ["time", 'highest_temp_city', 'highest_temp', 'lowest_temp_city', 'lowest_temp', 'avg_temp']

    with file.open('a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields, extrasaction= 'ignore')

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

    print("weather report exported")

def main():
    cached_file = Path(__file__).parent.resolve() / 'cache.json'
    now = datetime.now()
    cache = False

    if cached_file.is_file():
        with cached_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
            ct = datetime.fromisoformat(data['timestamp'])

            cache = (now - ct) < timedelta(minutes=10)

            if cache:
                print("pulling data from cache.")
                weather_data = data["weather_data"]

    if not cache:
        weather_data = get_all_cities_weather(cities)
        export_json(weather_data)

    stats = weather_statistics(weather_data)

    print(f"{" Weather Statistics ".center(70, "_")}")
    print(f"{"highest temperature city".ljust(30)}: {stats["highest_temp_city"]}")
    print(f"{"highest temperature".ljust(30)}: {stats["highest_temp"]}°C")
    print(f"{"lowest temperature city".ljust(30)}: {stats["lowest_temp_city"]}")
    print(f"{"lowest temperature".ljust(30)}: {stats["lowest_temp"]}°C")
    print(f"{"average temperature".ljust(30)}: {stats["avg_temp"]}°C")
    print(f"{" End ".center(70, "-")}")

    export_csv(stats)

if __name__ == "__main__":
    start = datetime.now()
    try:
        main()
    except:
        print("error occured.")
    end = datetime.now()
    time = end - start
    print(f"took -> {time}")