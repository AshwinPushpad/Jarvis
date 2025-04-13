from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Returns fake weather info for a given city.
    """
    # In a real use-case, this would call a weather API.
    weather_data = {
        "Delhi": "Hot and sunny, 40°C",
        "Mumbai": "Humid with scattered showers, 30°C",
        "Bangalore": "Pleasant and cloudy, 25°C",
        "Kolkata": "Warm and partly cloudy, 33°C"
    }
    return weather_data.get(city, f"No weather data available for {city}")
