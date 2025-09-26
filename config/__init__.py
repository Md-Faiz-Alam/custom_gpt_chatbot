# config/__init__.py

import os
import yaml
from dotenv import load_dotenv
import re
import streamlit as st  

load_dotenv() 

class AppConfig:
    ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_dir, "config.yaml")
        self.config = self.load_config()

    def _replace_env_vars(self, data):
        if isinstance(data, dict):
            return {k: self._replace_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_env_vars(v) for v in data]
        elif isinstance(data, str):
            matches = self.ENV_VAR_PATTERN.findall(data)
            for var in matches:
                value = st.secrets.get(var.lower()) if hasattr(st, "secrets") else None
                if not value:
                    value = os.getenv(var, data)
                data = data.replace(f"${{{var}}}", value)
            return data
        return data

    def load_config(self):
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

API_KEY = st.secrets["api"]["key"] if hasattr(st, "secrets") else config.get("api", {}).get("key")
