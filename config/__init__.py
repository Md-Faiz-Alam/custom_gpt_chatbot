# config/__init__.py

import os
import yaml
from dotenv import load_dotenv
import re
import streamlit as st  

# Load .env file if it exists
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
        Streamlit secrets, environment variables, or leave as-is.
        """
        if isinstance(data, dict):
            return {k: self._replace_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_env_vars(v) for v in data]
        elif isinstance(data, str):
            matches = self.ENV_VAR_PATTERN.findall(data)
            for var in matches:
                # Try Streamlit secrets (lowercase fallback)
                value = None
                if hasattr(st, "secrets"):
                    value = st.secrets.get(var.lower()) or st.secrets.get(var)
                # Try environment variable
                if not value:
                    value = os.getenv(var)
                # Replace if value found, else leave placeholder
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
    1. Resolved config.yaml
    2. Streamlit secrets (nested or flat)
    3. Environment variable
    """
    # 1. From config.yaml
    if "api" in config and "key" in config["api"] and config["api"]["key"]:
        return config["api"]["key"]

    # 2. Nested Streamlit secret
    if hasattr(st, "secrets") and "api" in st.secrets and "key" in st.secrets["api"]:
        return st.secrets["api"]["key"]

    # 3. Flat Streamlit secret
    if hasattr(st, "secrets") and "API_KEY" in st.secrets:
        return st.secrets["API_KEY"]

    # 4. Environment variable fallback
    return os.getenv("API_KEY")


API_KEY = get_api_key()

if not API_KEY:
    print("⚠️ Warning: API_KEY not found! Please check secrets/config/environment.")