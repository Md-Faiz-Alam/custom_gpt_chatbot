# app/api_client.py

import os
from groq import Groq
from logger import CustomLogger
from config import config
import streamlit as st

class GroqClient:
    """Class to interact with the Groq API."""

    def __init__(self):
        # Load API key from environment, Streamlit secrets, or config
        self.api_key = (
            os.getenv("API_KEY") or 
            st.secrets.get("API_KEY") or 
            config.get("api", {}).get("key")
        )
        if not self.api_key:
            raise ValueError(
                "API_KEY is missing! Set it in Streamlit secrets or config.yaml."
            )

        
        self.model = config.get("models", {}).get(
            "default", "llama-3.3-70b-versatile"
        )

        
        self.client = Groq(api_key=self.api_key)
        self.logger = CustomLogger().get_logger()

    def get_response(self, messages):
        """
        Send messages to the Groq API and return the response.

        :param messages: List of messages for the conversation.
        :return: AI response as a string.
        """
        try:
            self.logger.info(f"Sending messages to Groq API using model {self.model}...")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            response = chat_completion.choices[0].message.content
            self.logger.info("Received response from Groq API.")
            return response
        except Exception as e:
            self.logger.error(f"Error communicating with Groq API: {e}")
            return "Sorry, I couldn't get a response at this time."
