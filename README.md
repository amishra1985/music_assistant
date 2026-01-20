# music_assistant

Agentic AI that uses a local `ollama` instance and user-defined tools to search YouTube music and play songs based on search criteria.

## Features
- Query and search music by title, artist, genre, year, mood, and other criteria.
- Integrates with a local `ollama` model server for natural language understanding.
- Supports user-defined tools for searching and playing music (e.g., YouTube search + player).
- Extensible tool interface so you can add custom data sources or playback backends.

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
- Tool configuration:
  - Define your user tools (search, playback) in the project's tool configuration file or folder (commonly a `tools/` directory or a `tools.yaml`/`tools.json` file). The assistant expects each tool to expose a simple interface for search and play operations.
- Example env export (Windows cmd):
  - `set OLLAMA_HOST=http://localhost:11434`
  - `set OLLAMA_MODEL=your-model-name`

## Usage
- For now we need to run chrome with remote debugging enabled:
  - `"c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory=Default --user-data-dir="C:\ChromeDebug"`
- Run the assistant via the project's entrypoint (example):
  - `python music_assistant.py --song "<query for the AI assistant>"`
- Provide natural language queries like:
  - "Play the latest song by Radiohead"
  - "Find an upbeat lo-fi track from 2019"
- The assistant will use `ollama` to interpret the query and call the configured tools to search and play results.
- to run using streamlit interface:
  - `streamlit run streamlit_app.py`

## Troubleshooting
- If the assistant cannot reach `ollama`, verify `OLLAMA_HOST` and that the ollama server is running locally.
- If playback fails, check your tool configuration and ensure the LLM sends proper arguments to the tool

