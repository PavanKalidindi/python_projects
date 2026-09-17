from typing import Any

import requests


def get_current_weather(city_name: str, lat: float, long: float) -> dict[str, Any]:

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": long,
        "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m", 'weather_code']
    }

    response = requests.get(url, params)

    response.raise_for_status()

    data = response.json()

    current = data["current"]
    units = data['current_units']

    return {
        "city": city_name,
        "weather": weather_interpretation_codes(current.get("weather_code")),
        "temperature": current.get("temperature_2m"),
        "feels like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "wind speed": current.get("wind_speed_10m"),
        "units": units
    }

def get_all_cities_weather(cities: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    city_names = list(cities.keys())
    lats = [coords['lat'] for coords in cities.values()]
    longs = [coords['long'] for coords in cities.values()]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lats,
        "longitude": longs,
        "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    payload = response.json()

    # If multiple locations are sent, Open-Meteo returns a list of result dicts
    results = payload if isinstance(payload, list) else [payload]
    
    weather_data = []
    for city, data in zip(city_names, results):
        current = data["current"]
        weather_data.append({
            "city": city,
            "weather": weather_interpretation_codes(current.get("weather_code")),
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
        })

    return weather_data

def weather_statistics(data: list[dict[str, Any]]) -> dict[str, Any]:
    """returns min, max and avg weather accross the cities"""

    if not data:
        raise ValueError("cannot calculate statistics for empty weather data")
    
    highest = max(data, key= lambda x: x['temperature'])
    lowest = min(data, key= lambda x: x['temperature'])

    temps = [d['temperature'] for d in data]
    avg_temp = round(sum(temps)/len(temps), 2)

    return {
        "highest_temp_city": highest['city'],
        "highest_temp": highest['temperature'],
        "lowest_temp_city": lowest['city'],
        "lowest_temp": lowest['temperature'],
        "avg_temp": avg_temp
    }

def weather_interpretation_codes(code: int) -> str | None:
    wmo_code_map = {
        0: 'clear sky',
        1: 'mainly clear',
        2: 'partly cloudy',
        3: 'overcast',
        45: 'fog',
        48: 'rime fog',
        51: 'light drizzle',
        53: 'moderate drizzle',
        55: 'heavy drizzle',
        56: 'light freezing drizzle',
        57: 'heavy freeqing drizzle',
        61: 'light rain',
        63: 'moderate rain',
        65: 'heavy rain',
        66: 'light freezing rain',
        67: 'heavy freezing rain',
        71: 'light snow fall',
        73: 'moderate snow fall',
        75: 'heavy snow fall',
        77: 'snow grains',
        80: 'light rain shower',
        81: 'moderate rain shower',
        82: 'heavy rain shower',
        85: 'light snow shower',
        86: 'heavy snow shower',
        95: 'light/moderate thunderstorm',
        96: 'light hail',
        99: 'heavy hail' 
    }

    return wmo_code_map.get(code)


cities = {
    "New York": {"lat": 40.7128, "long": -74.0060},
    "Los Angeles": {"lat": 34.0522, "long": -118.2437},
    "Chicago": {"lat": 41.8781, "long": -87.6298},
    "Houston": {"lat": 29.7604, "long": -95.3698},
    "Toronto": {"lat": 43.6532, "long": -79.3832},
    "Mexico City": {"lat": 19.4326, "long": -99.1332},
    "Vancouver": {"lat": 49.2827, "long": -123.1207},
    "Miami": {"lat": 25.7617, "long": -80.1918},
    "San Francisco": {"lat": 37.7749, "long": -122.4194},
    "Boston": {"lat": 42.3601, "long": -71.0589},
    "Washington, D.C.": {"lat": 38.9072, "long": -77.0369},
    "Seattle": {"lat": 47.6062, "long": -122.3321},
    "Las Vegas": {"lat": 36.1699, "long": -115.1398},
    "Atlanta": {"lat": 33.7490, "long": -84.3880},

    "São Paulo": {"lat": -23.5505, "long": -46.6333},
    "Rio de Janeiro": {"lat": -22.9068, "long": -43.1729},
    "Buenos Aires": {"lat": -34.6037, "long": -58.3816},
    "Lima": {"lat": -12.0464, "long": -77.0428},
    "Bogotá": {"lat": 4.7110, "long": -74.0721},
    "Santiago": {"lat": -33.4489, "long": -70.6693},
    "Caracas": {"lat": 10.4806, "long": -66.9036},
    "Quito": {"lat": -0.1807, "long": -78.4678},
    "Montevideo": {"lat": -34.9011, "long": -56.1645},

    "London": {"lat": 51.5074, "long": -0.1278},
    "Paris": {"lat": 48.8566, "long": 2.3522},
    "Berlin": {"lat": 52.5200, "long": 13.4050},
    "Rome": {"lat": 41.9028, "long": 12.4964},
    "Madrid": {"lat": 40.4168, "long": -3.7038},
    "Barcelona": {"lat": 41.3874, "long": 2.1686},
    "Amsterdam": {"lat": 52.3676, "long": 4.9041},
    "Brussels": {"lat": 50.8503, "long": 4.3517},
    "Vienna": {"lat": 48.2082, "long": 16.3738},
    "Prague": {"lat": 50.0755, "long": 14.4378},
    "Budapest": {"lat": 47.4979, "long": 19.0402},
    "Warsaw": {"lat": 52.2297, "long": 21.0122},
    "Copenhagen": {"lat": 55.6761, "long": 12.5683},
    "Stockholm": {"lat": 59.3293, "long": 18.0686},
    "Oslo": {"lat": 59.9139, "long": 10.7522},
    "Helsinki": {"lat": 60.1699, "long": 24.9384},
    "Dublin": {"lat": 53.3498, "long": -6.2603},
    "Lisbon": {"lat": 38.7223, "long": -9.1393},
    "Athens": {"lat": 37.9838, "long": 23.7275},
    "Zurich": {"lat": 47.3769, "long": 8.5417},
    "Geneva": {"lat": 46.2044, "long": 6.1432},
    "Moscow": {"lat": 55.7558, "long": 37.6173},
    "Istanbul": {"lat": 41.0082, "long": 28.9784},
    "Kyiv": {"lat": 50.4501, "long": 30.5234},

    "Tokyo": {"lat": 35.6762, "long": 139.6503},
    "Osaka": {"lat": 34.6937, "long": 135.5023},
    "Kyoto": {"lat": 35.0116, "long": 135.7681},
    "Seoul": {"lat": 37.5665, "long": 126.9780},
    "Beijing": {"lat": 39.9042, "long": 116.4074},
    "Shanghai": {"lat": 31.2304, "long": 121.4737},
    "Hong Kong": {"lat": 22.3193, "long": 114.1694},
    "Shenzhen": {"lat": 22.5431, "long": 114.0579},
    "Guangzhou": {"lat": 23.1291, "long": 113.2644},
    "Taipei": {"lat": 25.0330, "long": 121.5654},
    "Singapore": {"lat": 1.3521, "long": 103.8198},
    "Bangkok": {"lat": 13.7563, "long": 100.5018},
    "Jakarta": {"lat": -6.2088, "long": 106.8456},
    "Kuala Lumpur": {"lat": 3.1390, "long": 101.6869},
    "Manila": {"lat": 14.5995, "long": 120.9842},
    "Hanoi": {"lat": 21.0285, "long": 105.8542},
    "Ho Chi Minh City": {"lat": 10.8231, "long": 106.6297},

    "Mumbai": {"lat": 19.0760, "long": 72.8777},
    "Delhi": {"lat": 28.6139, "long": 77.2090},
    "Bengaluru": {"lat": 12.9716, "long": 77.5946},
    "Chennai": {"lat": 13.0827, "long": 80.2707},
    "Hyderabad": {"lat": 17.3850, "long": 78.4867},
    "Kolkata": {"lat": 22.5726, "long": 88.3639},
    "Pune": {"lat": 18.5204, "long": 73.8567},
    "Ahmedabad": {"lat": 23.0225, "long": 72.5714},
    "Jaipur": {"lat": 26.9124, "long": 75.7873},
    "Dhaka": {"lat": 23.8103, "long": 90.4125},
    "Kathmandu": {"lat": 27.7172, "long": 85.3240},
    "Colombo": {"lat": 6.9271, "long": 79.8612},
    "Karachi": {"lat": 24.8607, "long": 67.0011},
    "Lahore": {"lat": 31.5497, "long": 74.3436},
    "Islamabad": {"lat": 33.6844, "long": 73.0479},

    "Dubai": {"lat": 25.2048, "long": 55.2708},
    "Abu Dhabi": {"lat": 24.4539, "long": 54.3773},
    "Doha": {"lat": 25.2854, "long": 51.5310},
    "Riyadh": {"lat": 24.7136, "long": 46.6753},
    "Jeddah": {"lat": 21.4858, "long": 39.1925},
    "Kuwait City": {"lat": 29.3759, "long": 47.9774},
    "Muscat": {"lat": 23.5880, "long": 58.3829},
    "Amman": {"lat": 31.9454, "long": 35.9284},
    "Beirut": {"lat": 33.8938, "long": 35.5018},
    "Jerusalem": {"lat": 31.7683, "long": 35.2137},
    "Tel Aviv": {"lat": 32.0853, "long": 34.7818},
    "Cairo": {"lat": 30.0444, "long": 31.2357},

    "Johannesburg": {"lat": -26.2041, "long": 28.0473},
    "Cape Town": {"lat": -33.9249, "long": 18.4241},
    "Lagos": {"lat": 6.5244, "long": 3.3792},
    "Nairobi": {"lat": -1.2921, "long": 36.8219},
    "Addis Ababa": {"lat": 9.0320, "long": 38.7469},
    "Accra": {"lat": 5.6037, "long": -0.1870},
    "Casablanca": {"lat": 33.5731, "long": -7.5898},
    "Marrakesh": {"lat": 31.6295, "long": -7.9811},
    "Tunis": {"lat": 36.8065, "long": 10.1815},
    "Algiers": {"lat": 36.7538, "long": 3.0588},
    "Dakar": {"lat": 14.7167, "long": -17.4677},
    "Dar es Salaam": {"lat": -6.7924, "long": 39.2083},

    "Sydney": {"lat": -33.8688, "long": 151.2093},
    "Melbourne": {"lat": -37.8136, "long": 144.9631},
    "Brisbane": {"lat": -27.4698, "long": 153.0251},
    "Perth": {"lat": -31.9505, "long": 115.8605},
    "Adelaide": {"lat": -34.9285, "long": 138.6007},
    "Auckland": {"lat": -36.8509, "long": 174.7633},
    "Wellington": {"lat": -41.2866, "long": 174.7756},
}

country_city = {
    "United States": {
        "New York": {"lat": 40.7128, "long": -74.0060},
        "Los Angeles": {"lat": 34.0522, "long": -118.2437},
        "Chicago": {"lat": 41.8781, "long": -87.6298},
        "Houston": {"lat": 29.7604, "long": -95.3698},
        "Miami": {"lat": 25.7617, "long": -80.1918},
        "San Francisco": {"lat": 37.7749, "long": -122.4194},
        "Washington, D.C.": {"lat": 38.9072, "long": -77.0369},
        "Boston": {"lat": 42.3601, "long": -71.0589},
        "Seattle": {"lat": 47.6062, "long": -122.3321},
        "Las Vegas": {"lat": 36.1699, "long": -115.1398},
        "Atlanta": {"lat": 33.7490, "long": -84.3880},
        "Denver": {"lat": 39.7392, "long": -104.9903},
        "Dallas": {"lat": 32.7767, "long": -96.7970},
        "Philadelphia": {"lat": 39.9526, "long": -75.1652},
        "Phoenix": {"lat": 33.4484, "long": -112.0740},
    },

    "Canada": {
        "Toronto": {"lat": 43.6532, "long": -79.3832},
        "Vancouver": {"lat": 49.2827, "long": -123.1207},
        "Montreal": {"lat": 45.5017, "long": -73.5673},
        "Calgary": {"lat": 51.0447, "long": -114.0719},
        "Ottawa": {"lat": 45.4215, "long": -75.6972},
        "Edmonton": {"lat": 53.5461, "long": -113.4938},
        "Quebec City": {"lat": 46.8139, "long": -71.2080},
    },

    "Mexico": {
        "Mexico City": {"lat": 19.4326, "long": -99.1332},
        "Guadalajara": {"lat": 20.6597, "long": -103.3496},
        "Monterrey": {"lat": 25.6866, "long": -100.3161},
        "Cancún": {"lat": 21.1619, "long": -86.8515},
        "Tijuana": {"lat": 32.5149, "long": -117.0382},
    },

    "Brazil": {
        "São Paulo": {"lat": -23.5505, "long": -46.6333},
        "Rio de Janeiro": {"lat": -22.9068, "long": -43.1729},
        "Brasília": {"lat": -15.7975, "long": -47.8919},
        "Salvador": {"lat": -12.9777, "long": -38.5016},
        "Belo Horizonte": {"lat": -19.9167, "long": -43.9345},
        "Recife": {"lat": -8.0476, "long": -34.8770},
        "Curitiba": {"lat": -25.4284, "long": -49.2733},
        "Fortaleza": {"lat": -3.7319, "long": -38.5267},
    },

    "Argentina": {
        "Buenos Aires": {"lat": -34.6037, "long": -58.3816},
        "Córdoba": {"lat": -31.4201, "long": -64.1888},
        "Rosario": {"lat": -32.9442, "long": -60.6505},
        "Mendoza": {"lat": -32.8895, "long": -68.8458},
    },

    "Chile": {
        "Santiago": {"lat": -33.4489, "long": -70.6693},
        "Valparaíso": {"lat": -33.0472, "long": -71.6127},
        "Concepción": {"lat": -36.8201, "long": -73.0444},
    },

    "Colombia": {
        "Bogotá": {"lat": 4.7110, "long": -74.0721},
        "Medellín": {"lat": 6.2476, "long": -75.5658},
        "Cartagena": {"lat": 10.3910, "long": -75.4794},
        "Cali": {"lat": 3.4516, "long": -76.5320},
    },

    "Peru": {
        "Lima": {"lat": -12.0464, "long": -77.0428},
        "Cusco": {"lat": -13.5319, "long": -71.9675},
        "Arequipa": {"lat": -16.4090, "long": -71.5375},
    },

    "United Kingdom": {
        "London": {"lat": 51.5074, "long": -0.1278},
        "Manchester": {"lat": 53.4808, "long": -2.2426},
        "Birmingham": {"lat": 52.4862, "long": -1.8904},
        "Edinburgh": {"lat": 55.9533, "long": -3.1883},
        "Glasgow": {"lat": 55.8642, "long": -4.2518},
        "Liverpool": {"lat": 53.4084, "long": -2.9916},
        "Bristol": {"lat": 51.4545, "long": -2.5879},
        "Oxford": {"lat": 51.7520, "long": -1.2577},
        "Cambridge": {"lat": 52.2053, "long": 0.1218},
    },

    "France": {
        "Paris": {"lat": 48.8566, "long": 2.3522},
        "Marseille": {"lat": 43.2965, "long": 5.3698},
        "Lyon": {"lat": 45.7640, "long": 4.8357},
        "Nice": {"lat": 43.7102, "long": 7.2620},
        "Bordeaux": {"lat": 44.8378, "long": -0.5792},
        "Toulouse": {"lat": 43.6047, "long": 1.4442},
        "Strasbourg": {"lat": 48.5734, "long": 7.7521},
    },

    "Germany": {
        "Berlin": {"lat": 52.5200, "long": 13.4050},
        "Munich": {"lat": 48.1351, "long": 11.5820},
        "Hamburg": {"lat": 53.5511, "long": 9.9937},
        "Frankfurt": {"lat": 50.1109, "long": 8.6821},
        "Cologne": {"lat": 50.9375, "long": 6.9603},
        "Düsseldorf": {"lat": 51.2277, "long": 6.7735},
        "Stuttgart": {"lat": 48.7758, "long": 9.1829},
    },

    "Italy": {
        "Rome": {"lat": 41.9028, "long": 12.4964},
        "Milan": {"lat": 45.4642, "long": 9.1900},
        "Venice": {"lat": 45.4408, "long": 12.3155},
        "Florence": {"lat": 43.7696, "long": 11.2558},
        "Naples": {"lat": 40.8518, "long": 14.2681},
        "Turin": {"lat": 45.0703, "long": 7.6869},
        "Bologna": {"lat": 44.4949, "long": 11.3426},
    },

    "Spain": {
        "Madrid": {"lat": 40.4168, "long": -3.7038},
        "Barcelona": {"lat": 41.3874, "long": 2.1686},
        "Seville": {"lat": 37.3891, "long": -5.9845},
        "Valencia": {"lat": 39.4699, "long": -0.3763},
        "Málaga": {"lat": 36.7213, "long": -4.4214},
        "Bilbao": {"lat": 43.2630, "long": -2.9350},
    },

    "Netherlands": {
        "Amsterdam": {"lat": 52.3676, "long": 4.9041},
        "Rotterdam": {"lat": 51.9244, "long": 4.4777},
        "The Hague": {"lat": 52.0705, "long": 4.3007},
        "Utrecht": {"lat": 52.0907, "long": 5.1214},
    },

    "Belgium": {
        "Brussels": {"lat": 50.8503, "long": 4.3517},
        "Antwerp": {"lat": 51.2194, "long": 4.4025},
        "Bruges": {"lat": 51.2093, "long": 3.2247},
    },

    "Switzerland": {
        "Zurich": {"lat": 47.3769, "long": 8.5417},
        "Geneva": {"lat": 46.2044, "long": 6.1432},
        "Bern": {"lat": 46.9480, "long": 7.4474},
        "Basel": {"lat": 47.5596, "long": 7.5886},
        "Lucerne": {"lat": 47.0502, "long": 8.3093},
    },

    "Austria": {
        "Vienna": {"lat": 48.2082, "long": 16.3738},
        "Salzburg": {"lat": 47.8095, "long": 13.0550},
        "Innsbruck": {"lat": 47.2692, "long": 11.4041},
    },

    "Greece": {
        "Athens": {"lat": 37.9838, "long": 23.7275},
        "Thessaloniki": {"lat": 40.6401, "long": 22.9444},
        "Heraklion": {"lat": 35.3387, "long": 25.1442},
    },

    "Portugal": {
        "Lisbon": {"lat": 38.7223, "long": -9.1393},
        "Porto": {"lat": 41.1579, "long": -8.6291},
        "Faro": {"lat": 37.0194, "long": -7.9304},
    },

    "Ireland": {
        "Dublin": {"lat": 53.3498, "long": -6.2603},
        "Cork": {"lat": 51.8985, "long": -8.4756},
        "Galway": {"lat": 53.2707, "long": -9.0568},
    },

    "Czech Republic": {
        "Prague": {"lat": 50.0755, "long": 14.4378},
        "Brno": {"lat": 49.1951, "long": 16.6068},
        "Ostrava": {"lat": 49.8209, "long": 18.2625},
    },

    "Poland": {
        "Warsaw": {"lat": 52.2297, "long": 21.0122},
        "Kraków": {"lat": 50.0647, "long": 19.9450},
        "Wrocław": {"lat": 51.1079, "long": 17.0385},
        "Gdańsk": {"lat": 54.3520, "long": 18.6466},
        "Poznań": {"lat": 52.4064, "long": 16.9252},
    },

    "Hungary": {
        "Budapest": {"lat": 47.4979, "long": 19.0402},
        "Debrecen": {"lat": 47.5316, "long": 21.6273},
    },

    "Sweden": {
        "Stockholm": {"lat": 59.3293, "long": 18.0686},
        "Gothenburg": {"lat": 57.7089, "long": 11.9746},
        "Malmö": {"lat": 55.6050, "long": 13.0038},
    },

    "Norway": {
        "Oslo": {"lat": 59.9139, "long": 10.7522},
        "Bergen": {"lat": 60.3913, "long": 5.3221},
        "Trondheim": {"lat": 63.4305, "long": 10.3951},
    },

    "Denmark": {
        "Copenhagen": {"lat": 55.6761, "long": 12.5683},
        "Aarhus": {"lat": 56.1629, "long": 10.2039},
    },

    "Finland": {
        "Helsinki": {"lat": 60.1699, "long": 24.9384},
        "Tampere": {"lat": 61.4978, "long": 23.7610},
        "Turku": {"lat": 60.4518, "long": 22.2666},
    },

    "Russia": {
        "Moscow": {"lat": 55.7558, "long": 37.6173},
        "Saint Petersburg": {"lat": 59.9311, "long": 30.3609},
        "Kazan": {"lat": 55.8304, "long": 49.0661},
        "Sochi": {"lat": 43.6028, "long": 39.7342},
        "Novosibirsk": {"lat": 55.0084, "long": 82.9357},
    },

    "Turkey": {
        "Istanbul": {"lat": 41.0082, "long": 28.9784},
        "Ankara": {"lat": 39.9334, "long": 32.8597},
        "Izmir": {"lat": 38.4237, "long": 27.1428},
        "Antalya": {"lat": 36.8969, "long": 30.7133},
        "Bursa": {"lat": 40.1950, "long": 29.0600},
    },

    "Ukraine": {
        "Kyiv": {"lat": 50.4501, "long": 30.5234},
        "Lviv": {"lat": 49.8397, "long": 24.0297},
        "Odesa": {"lat": 46.4825, "long": 30.7233},
    },

    "United Arab Emirates": {
        "Dubai": {"lat": 25.2048, "long": 55.2708},
        "Abu Dhabi": {"lat": 24.4539, "long": 54.3773},
        "Sharjah": {"lat": 25.3463, "long": 55.4209},
    },

    "Saudi Arabia": {
        "Riyadh": {"lat": 24.7136, "long": 46.6753},
        "Jeddah": {"lat": 21.4858, "long": 39.1925},
        "Mecca": {"lat": 21.3891, "long": 39.8579},
        "Medina": {"lat": 24.5247, "long": 39.5692},
        "Dammam": {"lat": 26.4207, "long": 50.0888},
    },

    "Qatar": {
        "Doha": {"lat": 25.2854, "long": 51.5310},
    },

    "Israel": {
        "Tel Aviv": {"lat": 32.0853, "long": 34.7818},
        "Jerusalem": {"lat": 31.7683, "long": 35.2137},
        "Haifa": {"lat": 32.7940, "long": 34.9896},
    },

    "Egypt": {
        "Cairo": {"lat": 30.0444, "long": 31.2357},
        "Alexandria": {"lat": 31.2001, "long": 29.9187},
        "Giza": {"lat": 30.0131, "long": 31.2089},
        "Luxor": {"lat": 25.6872, "long": 32.6396},
    },

    "South Africa": {
        "Johannesburg": {"lat": -26.2041, "long": 28.0473},
        "Cape Town": {"lat": -33.9249, "long": 18.4241},
        "Durban": {"lat": -29.8587, "long": 31.0218},
        "Pretoria": {"lat": -25.7479, "long": 28.2293},
        "Port Elizabeth": {"lat": -33.9608, "long": 25.6022},
    },

    "Morocco": {
        "Casablanca": {"lat": 33.5731, "long": -7.5898},
        "Marrakesh": {"lat": 31.6295, "long": -7.9811},
        "Rabat": {"lat": 34.0209, "long": -6.8416},
        "Tangier": {"lat": 35.7595, "long": -5.8340},
        "Fes": {"lat": 34.0181, "long": -5.0078},
    },

    "Nigeria": {
        "Lagos": {"lat": 6.5244, "long": 3.3792},
        "Abuja": {"lat": 9.0765, "long": 7.3986},
        "Kano": {"lat": 12.0022, "long": 8.5920},
        "Ibadan": {"lat": 7.3775, "long": 3.9470},
    },

    "Kenya": {
        "Nairobi": {"lat": -1.2921, "long": 36.8219},
        "Mombasa": {"lat": -4.0435, "long": 39.6682},
        "Kisumu": {"lat": -0.0917, "long": 34.7680},
    },

    "Ethiopia": {
        "Addis Ababa": {"lat": 9.0320, "long": 38.7469},
        "Gondar": {"lat": 12.6030, "long": 37.4521},
    },

    "Ghana": {
        "Accra": {"lat": 5.6037, "long": -0.1870},
        "Kumasi": {"lat": 6.6885, "long": -1.6244},
    },

    "India": {
        "Mumbai": {"lat": 19.0760, "long": 72.8777},
        "Delhi": {"lat": 28.6139, "long": 77.2090},
        "Bengaluru": {"lat": 12.9716, "long": 77.5946},
        "Hyderabad": {"lat": 17.3850, "long": 78.4867},
        "Chennai": {"lat": 13.0827, "long": 80.2707},
        "Kolkata": {"lat": 22.5726, "long": 88.3639},
        "Pune": {"lat": 18.5204, "long": 73.8567},
        "Ahmedabad": {"lat": 23.0225, "long": 72.5714},
        "Jaipur": {"lat": 26.9124, "long": 75.7873},
        "Lucknow": {"lat": 26.8467, "long": 80.9462},
        "Kochi": {"lat": 9.9312, "long": 76.2673},
        "Goa": {"lat": 15.2993, "long": 74.1240},
        "Varanasi": {"lat": 25.3176, "long": 82.9739},
        "Chandigarh": {"lat": 30.7333, "long": 76.7794},
    },

    "China": {
        "Beijing": {"lat": 39.9042, "long": 116.4074},
        "Shanghai": {"lat": 31.2304, "long": 121.4737},
        "Guangzhou": {"lat": 23.1291, "long": 113.2644},
        "Shenzhen": {"lat": 22.5431, "long": 114.0579},
        "Chengdu": {"lat": 30.5728, "long": 104.0668},
        "Chongqing": {"lat": 29.5630, "long": 106.5516},
        "Xi'an": {"lat": 34.3416, "long": 108.9398},
        "Hangzhou": {"lat": 30.2741, "long": 120.1551},
        "Nanjing": {"lat": 32.0603, "long": 118.7969},
        "Wuhan": {"lat": 30.5928, "long": 114.3055},
    },

    "Japan": {
        "Tokyo": {"lat": 35.6762, "long": 139.6503},
        "Osaka": {"lat": 34.6937, "long": 135.5023},
        "Kyoto": {"lat": 35.0116, "long": 135.7681},
        "Yokohama": {"lat": 35.4437, "long": 139.6380},
        "Nagoya": {"lat": 35.1815, "long": 136.9066},
        "Sapporo": {"lat": 43.0618, "long": 141.3545},
        "Fukuoka": {"lat": 33.5904, "long": 130.4017},
    },

    "South Korea": {
        "Seoul": {"lat": 37.5665, "long": 126.9780},
        "Busan": {"lat": 35.1796, "long": 129.0756},
        "Incheon": {"lat": 37.4563, "long": 126.7052},
        "Daegu": {"lat": 35.8714, "long": 128.6014},
        "Jeju City": {"lat": 33.4996, "long": 126.5312},
    },

    "Singapore": {
        "Singapore": {"lat": 1.3521, "long": 103.8198},
    },

    "Thailand": {
        "Bangkok": {"lat": 13.7563, "long": 100.5018},
        "Chiang Mai": {"lat": 18.7883, "long": 98.9853},
        "Phuket": {"lat": 7.8804, "long": 98.3923},
        "Pattaya": {"lat": 12.9236, "long": 100.8825},
    },

    "Indonesia": {
        "Jakarta": {"lat": -6.2088, "long": 106.8456},
        "Bali": {"lat": -8.3405, "long": 115.0920},
        "Surabaya": {"lat": -7.2575, "long": 112.7521},
        "Bandung": {"lat": -6.9175, "long": 107.6191},
        "Yogyakarta": {"lat": -7.7956, "long": 110.3695},
    },

    "Malaysia": {
        "Kuala Lumpur": {"lat": 3.1390, "long": 101.6869},
        "George Town": {"lat": 5.4141, "long": 100.3288},
        "Johor Bahru": {"lat": 1.4927, "long": 103.7414},
        "Kota Kinabalu": {"lat": 5.9804, "long": 116.0735},
    },

    "Philippines": {
        "Manila": {"lat": 14.5995, "long": 120.9842},
        "Cebu City": {"lat": 10.3157, "long": 123.8854},
        "Davao City": {"lat": 7.1907, "long": 125.4553},
    },

    "Vietnam": {
        "Hanoi": {"lat": 21.0285, "long": 105.8542},
        "Ho Chi Minh City": {"lat": 10.8231, "long": 106.6297},
        "Da Nang": {"lat": 16.0544, "long": 108.2022},
        "Hoi An": {"lat": 15.8801, "long": 108.3380},
    },

    "Bangladesh": {
        "Dhaka": {"lat": 23.8103, "long": 90.4125},
        "Chittagong": {"lat": 22.3569, "long": 91.7832},
    },

    "Pakistan": {
        "Karachi": {"lat": 24.8607, "long": 67.0011},
        "Lahore": {"lat": 31.5497, "long": 74.3436},
        "Islamabad": {"lat": 33.6844, "long": 73.0479},
        "Rawalpindi": {"lat": 33.5651, "long": 73.0169},
    },

    "Nepal": {
        "Kathmandu": {"lat": 27.7172, "long": 85.3240},
        "Pokhara": {"lat": 28.2096, "long": 83.9856},
    },

    "Sri Lanka": {
        "Colombo": {"lat": 6.9271, "long": 79.8612},
        "Kandy": {"lat": 7.2906, "long": 80.6337},
        "Galle": {"lat": 6.0329, "long": 80.2168},
    },

    "Australia": {
        "Sydney": {"lat": -33.8688, "long": 151.2093},
        "Melbourne": {"lat": -37.8136, "long": 144.9631},
        "Brisbane": {"lat": -27.4698, "long": 153.0251},
        "Perth": {"lat": -31.9505, "long": 115.8605},
        "Adelaide": {"lat": -34.9285, "long": 138.6007},
        "Canberra": {"lat": -35.2809, "long": 149.1300},
        "Gold Coast": {"lat": -28.0167, "long": 153.4000},
    },

    "New Zealand": {
        "Auckland": {"lat": -36.8509, "long": 174.7633},
        "Wellington": {"lat": -41.2866, "long": 174.7756},
        "Christchurch": {"lat": -43.5321, "long": 172.6362},
        "Queenstown": {"lat": -45.0312, "long": 168.6626},
    }
}


# ----------- Testing
def main():
    city = "Hyderabad"
    lat = cities[city].get("lat")
    long = cities[city].get("long")
    print(get_current_weather(city, lat, long))

if __name__ == "__main__":
    main()