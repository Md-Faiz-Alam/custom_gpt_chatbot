# app/utils.py

import re
import html
from logger import CustomLogger

logger = CustomLogger().get_logger()

def log_error(message: str):
    """Log an error message."""
    logger.error(message)


def format_response(response):
    """Format AI response for Streamlit display with code blocks and markdown."""

    if not isinstance(response, str):
        response = str(response)

    response = response.replace("[object Object]", "")

    if "```" in response:
        parts = response.split("```")
        formatted_response = ""
        for i, part in enumerate(parts):
            if i % 2 == 1:
                formatted_response += f"<pre style='background:#f4f4f4; padding:8px; border-radius:5px;'><code>{part}</code></pre>"
            else:
                formatted_response += part
        response = formatted_response
    else:
        response = response.replace("\n", "<br>")

    response = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", response)
    response = re.sub(r"\*(.*?)\*", r"<em>\1</em>", response)

    return response

