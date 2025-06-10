import requests

API_KEY = "c4c5b248e978b4c6a8c1f6f4c9f538d8"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    if not city:
        print("[DEBUG] No city provided")
        return None

    try:
        print(f"[DEBUG] Fetching weather for city: {city}")
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pl"
        })
        data = response.json()
        print("[DEBUG] API response:", data)

        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}: {data}")
            return None

        if "weather" not in data or "main" not in data:
            print("[ERROR] Missing weather/main in response")
            return None

        weather_main = data["weather"][0].get("main", "").lower()
        weather_desc = data["weather"][0].get("description", "")
        humidity = data["main"].get("humidity", 0)
        temp = data["main"].get("temp", 0)

        return {
            "is_rainy": "rain" in weather_main or "drizzle" in weather_main,
            "humidity": humidity,
            "temp": temp,
            "desc": weather_desc,
            "raw": weather_main
        }

    except Exception as e:
        print(f"[EXCEPTION] Błąd pobierania pogody: {e}")
        return None
