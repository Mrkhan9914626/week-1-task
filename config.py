import os
from dotenv import load_dotenv

load_dotenv()


def get_env_or_raise(key: str) -> str:
    # Try streamlit secrets first (for Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, AttributeError):
        pass

    # Fall back to environment variables (for local development)
    value = os.getenv(key)
    if not value:
        raise ValueError(
            f"{key} is not set. For local development, add it to your .env file. "
            f"For Streamlit Cloud, add it to your app's secrets in the Streamlit Cloud dashboard."
        )
    return value


OPENAI_API_KEY = get_env_or_raise("OPENAI_API_KEY")
WEATHER_API_KEY = get_env_or_raise("WEATHER_API_KEY")
TAVILY_API_KEY = get_env_or_raise("TAVILY_API_KEY")
