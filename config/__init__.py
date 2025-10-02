# config/__init__.py

import os
import yaml
from dotenv import load_dotenv
import re
import streamlit as st

# Load .env file
load_dotenv()


class AppConfig:
    ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_dir, "config.yaml")
        self.config = self.load_config()

    def _replace_env_vars(self, data):
        """
        Recursively replace placeholders like ${VAR} in config with
        environment variables, Streamlit secrets, or leave as-is.
        """
        if isinstance(data, dict):
            return {k: self._replace_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_env_vars(v) for v in data]
        elif isinstance(data, str):
            matches = self.ENV_VAR_PATTERN.findall(data)
            for var in matches:
                # Try environment variable first
                value = os.getenv(var)

                # Then Streamlit secrets (if available)
                if not value and hasattr(st, "secrets"):
                    try:
                        value = st.secrets.get(var.lower()) or st.secrets.get(var)
                    except Exception:
                        value = None

                # Replace if value found
                if value:
                    data = data.replace(f"${{{var}}}", value)
            return data
        return data

    def load_config(self):
        """
        Load YAML config and replace placeholders.
        """
        try:
            with open(self.config_file, "r") as file:
                config = yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing YAML config: {e}")

        config = self._replace_env_vars(config)
        return config


# Global config object
app_config = AppConfig()
config = app_config.config


def get_api_key():
    """
    Safely get the API key from:
    1. Environment variable
    2. Resolved config.yaml
    3. Streamlit secrets (nested [api] or flat API_KEY)
    """
    # 1. Environment variable
    api_key = os.getenv("API_KEY")
    if api_key:
        return api_key

    # 2. Config.yaml
    if "api" in config and "key" in config["api"] and config["api"]["key"]:
        return config["api"]["key"]

    # 3. Streamlit nested secret
    if hasattr(st, "secrets"):
        try:
            if "api" in st.secrets and "key" in st.secrets["api"]:
                return st.secrets["api"]["key"]
            if "API_KEY" in st.secrets:
                return st.secrets["API_KEY"]
        except Exception:
            pass

    return None


API_KEY = get_api_key()

if not API_KEY:
    print("⚠️ Warning: API_KEY not found! Please check your .env, config.yaml, or Streamlit secrets.")
