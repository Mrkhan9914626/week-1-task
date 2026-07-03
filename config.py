import os
from dotenv import load_dotenv

load_dotenv()


def get_env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(
            f"{key} is not set. Add it to your .env file or set it as an environment variable."
        )
    return value


OPENAI_API_KEY = get_env_or_raise("OPENAI_API_KEY")
WEATHER_API_KEY = get_env_or_raise("WEATHER_API_KEY")
TAVILY_API_KEY = get_env_or_raise("TAVILY_API_KEY")
