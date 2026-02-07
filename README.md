# music_assistant

Agentic AI that uses a local `ollama` instance and user-defined tools to search YouTube music and play songs based on search criteria.

## Features
- Query and search music by title, artist, genre, year, mood, and other criteria.
- Integrates with a local `ollama` model server for natural language understanding.
- Supports user-defined tools for searching and playing music (e.g., YouTube search + player) based on mcp server.
- Extensible tool interface so you can add custom data sources or playback backends.
- connect to home assistant and make your smart lights dance to music
- Optional LangSmith tracing for monitoring and debugging agent interactions.

## Prerequisites
- Python 3.8+  
- `pip` available on your PATH  
- A local `ollama` server accessible from the machine (see `OLLAMA_HOST` and `OLLAMA_MODEL` configuration below)
- Optional: YouTube extraction/downloading tool (e.g., `yt-dlp`) or a player expected by your tools

## Installation
1. Clone the repository:
   - `git clone <repo-url>`
2. Create and activate a virtual environment:
   - Windows (PowerShell): `python -m venv venv` then `.\venv\Scripts\Activate.ps1`
   - Windows (cmd): `python -m venv venv` then `.\venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Configuration
- Environment variables:
  - `OLLAMA_HOST` — host/port of your local ollama server (e.g., `http://localhost:11434`)
  - `OLLAMA_MODEL` — model name to use on the ollama server
  - `HA_URL` — URL for Home Assistant API to control devices (if using HA tools)
  - `HA_TOKEN` — long-lived access token for Home Assistant API
  - `LANGSMITH_TRACING` — set to `true` to enable LangSmith tracing
  - `LANGSMITH_ENDPOINT` — LangSmith API endpoint (e.g., `https://api.smith.langchain.com`)
  - `LANGSMITH_API_KEY` — API key for LangSmith
  - `LANGSMITH_PROJECT` — project name for LangSmith tracing
- Tool configuration:
  - Setup your tool under the mcp_server configuration. Put any helper files under mcp_server/tools_helpers
- Create an env file (e.g., `.env`) in the project root with the necessary environment variables:
  ```
  OLLAMA_HOST=http://localhost:11434
  OLLAMA_MODEL=your-ollama-model-name
  HA_URL = http://homeassistant.local:8123/api/services/light/turn_on
  HA_TOKEN = xxxxx
  LANGSMITH_TRACING=true
  LANGSMITH_ENDPOINT=https://api.smith.langchain.com
  LANGSMITH_API_KEY=xxxxxxx
  LANGSMITH_PROJECT=music_assistant
  ```

## Usage
- For now we need to run chrome with remote debugging enabled. example for windows run:
  - `"c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory=Default --user-data-dir="C:\ChromeDebug"`
- Run the assistant via the project's entrypoint (example):
  - `python music_assistant.py --song "<query for the AI assistant>"`
- Provide natural language queries like:
  - "Play the latest song by Radiohead"
  - "Find an upbeat lo-fi track from 2019"
- The assistant will use `ollama` to interpret the query and call the configured tools to search and play results.
- to run using streamlit interface:
  - `streamlit run streamlit_app.py`
- Streamlit interface allows you to input queries and see the assistant's reasoning and tool calls in real time plus toggle the music syncing with home assistant

## Troubleshooting
- If the assistant cannot reach `ollama`, verify `OLLAMA_HOST` and that the ollama server is running locally.
- If playback fails, check your tool configuration and ensure the LLM sends proper arguments to the tool.
- make sure that Chrome is running with remote debugging enabled on the expected port if using the YouTube tool.
- Check the console output for any error messages or stack traces to identify issues.
- If using LangSmith tracing, verify that your API key and endpoint are correct and check the LangSmith dashboard for logged interactions.
- If using Home Assistant integration, verify that your `HA_URL` and `HA_TOKEN` are correct and that the Home Assistant API is accessible from the machine running the assistant.
- If you encounter issues with the assistant's reasoning or tool usage, consider enabling more verbose logging in the code to see the LLM's thought process and tool calls in more detail.
- 

