## Custom GPT Chatbot

A custom AI chatbot built with Streamlit and Groq API, designed to respond to user queries, explain code, define terms, and provide concise answers. Perfect for showcasing AI capabilities in a professional or interview setting.

### Table of Contents

1. Features
2. Demo
3. Installation
4. Configuration
5. Usage
6. Project Structure
7. Requirements
8. Deployment
9. Notes

### Features

 - Interactive AI chatbot interface with conversation history.

 - Quick prompts for:
   - Explaining code
   - Defining terms
   - Providing concise answers

 - Clean conversation formatting: clear distinction between user and assistant messages.

- Configurable Groq API model.

- Logging of all interactions for debugging and monitoring.

### Demo

After running the app locally:

 - Type messages in the chat input.

 - Use Quick Prompt buttons on the sidebar to interact with AI automatically.

 - Conversation history is displayed on the sidebar.


### Installation

1. Clone the repository:
```
[Clone the repository](https://github.com/Md-Faiz-Alam/custom_gpt_chatbot.git)
cd custom_bot
```

2. Create and activate a virtual environment:
```
python -m venv venv
vevn\scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

### Configuration 

***.env*** File
Create a .env fiel in the root directory and add your Groq API key:

```
API_KEY=your_groq_api_key_here
```

*** config/config.yaml *** 
Configure the app, API, and model settings:

```
app:
  name: "Custom_Bot"
  version: "0.1.0"
  description: "A custom Bot application"

api:
  key: "${API_KEY}"
  base_url: "https://api.groq.com/v1"
  timeout: 30
  retries: 3

models:
  default: "llama-3.3-70b-versatile"
  available:
    - "llama-3.3-70b-versatile"
    - "llama3-70b-8192"
    - "mixtral-8x7b-32768"
    - "gemma2-9b-it"
  settings:
    temperature: 0.7
    max_tokens: 1024

logging:
  level: "INFO"
  log_directory: "logs"
  log_file_format: "[%(asctime)s] %(name)s -%(levelname)s -%(message)s"
  max_bytes: 10485760
  backup_count: 5
  rotate: true

```

### Usage

1. Run teh Streamlit app:

```
streamlit run app.py
```

2. Interact with the chatbot:
 - Enter messages in the chat input.
 - use Quick Prompt buttons to:
  - Explain code
  - Define terms
  -  Get concise answers

3. Conversation history will appear in the sidebar

### Project Structure

```
custom_bot/
│
├── app/
│   ├── __init__.py
│   ├── api_client.py          # Groq API client
│   ├── chat.py                # Chat manager
│   ├── utils.py               # Formatting and logging helpers
│   └── app.py                 # Streamlit app entrypoint
│
├── config/
│   ├── __init__.py            # Loads YAML + environment variables
│   └── config.yaml            # Main configuration file
│
├── logs/                      # Auto-generated logs folder
├── .env                       # Groq API key (not committed)
├── requirements.txt           # Project dependencies
└── README.md

```

### Requirements

- [Python 3.13](https://www.python.org/downloads/release/python-3130/)  
- [Streamlit](https://streamlit.io/)  
- [Groq API Python client](https://pypi.org/project/groq/)  
 - Other dependencies as per requirements.txt:


### Notes

- Make sure Groq API key is set in ***.env*** or Streamlit environment variables.

- Conversation history is stored in-memory using ***st.session_state***.

- Quick Prompt buttons work dynamically without requiring extra input.

- Logging is configured to store messages and errors in ***logs/***.

- Model selection can be changed in ***config.yaml***. Ensure the model exists in your Groq account.