import httpx
from agents import function_tool
from config import WEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@function_tool
def get_weather(location: str) -> str:
    """Get the current weather for a given city using OpenWeatherMap.

    Args:
        location: The city name (e.g., "London", "Karachi", "New York").
            Optionally include the country code (e.g., "London,UK").
    """
    try:
        response = httpx.get(
            BASE_URL,
            params={
                "q": location,
                "appid": WEATHER_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Weather in {city}, {country}: {condition.capitalize()}, "
            f"{temp:.1f}°C (feels like {feels_like:.1f}°C), "
            f"humidity {humidity}%, wind {wind_speed} m/s"
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: City '{location}' not found. Please check the spelling."
        return f"Error: Weather API returned status {e.response.status_code}."
    except httpx.RequestError:
        return "Error: Could not connect to the weather service. Please check your internet connection."
    except (KeyError, IndexError) as e:
        return f"Error: Unexpected response format from weather API: {e}"
