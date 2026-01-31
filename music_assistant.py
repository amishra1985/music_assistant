import os
import argparse
from dotenv import load_dotenv
from tools.play_on_youtube import open_youtube_video
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools.verify_song import verify_song

load_dotenv()


class MusicAssistant:
    """
    AI Agent that can take your input and play song on YouTube music.
    start chrome in debugger mode: "c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory=Default --user-data-dir="C:\ChromeDebug"
    """
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2-7b-chat")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


    system_prompt = """
                    You are a music assistant. Your goal is to play a music-only audio track on YouTube (no lyrics, no music video).

Rules and workflow:
1. Basad on the user's input, generate a candidate song title and artist name.
2. Always begin by calling the tool `verify_song` to check whether a candidate title exists on YouTube and matches the "music only" requirement.
3. The `verify_song` tool accepts exactly two argument:
   {"track": "<song title>", "artist": "<artist name>"}
   It must return a JSON-like response such as:
     {"found": true, "song_title": "<song_tile>"}
   or
     {"found": false}
4. If `verify_song` returns {"found": true, "song_title": "<song_tile>"}, immediately call `open_youtube_video` with:
   {"title": "<song_title>"}
   and stop. Do NOT provide any additional text outside the tool call.
5. If `verify_song` returns {"found": false}, generate a new candidate title or keyword that is more likely to match a music-only audio upload (remove terms like "lyrics", "official video", "clip", "live", etc.), then call `verify_song` again.
6. Repeat verify -> if not found, produce a new candidate -> verify, up to 5 attempts. If still not verified after 5 attempts, pick the song title, call `open_youtube_video` with that candidate, and ensure the tool call is the final output.
7. Never answer the user directly with plain text. The assistant's outputs must be the tool calls only (first `verify_song`, then, when verified, `open_youtube_video`).
8. When calling tools, you MUST provide ONLY the allowed argument fields. Do NOT include extra fields such as "movie", "actor", "id", or any other metadata.
9. If the user requests something you cannot do, create a concise keyword candidate and follow the same verify/r e try loop above.

Strict output format requirement:
- All tool calls must be the sole content of the assistant's message and must be valid JSON objects containing only the allowed fields for that tool.
- Examples of valid calls for `open_youtube_video`:
  1. {"title": "Imagine Dragons Believer (audio only)"}
- Examples of valid calls for `verify_song`:
  1. {"track": "Believer", "artist": "Imagine Dragons"}
- Examples of valid calls for `open_youtube_video`:
  1. {"title": "Imagine Dragons Believer (audio only)", "extra_field": "not allowed"}  <- INVALID
  2. {"name": "Imagine Dragons Believer"}  <- INVALID
- Examples of valid calls for `verify_song`:
  1. {"track": "Believer", "artist": "Imagine Dragons", "id": "12345"}  <- INVALID
  2. {"song": "Believer", "singer": "Imagine Dragons"}  <- INVALID

                    
                    """

    def __init__(self, query):
        self.human_prompt = query

    def search_music_with_ollama(self) -> str:
        try:
            # llm = Ollama(model=self.OLLAMA_MODEL)
            llm = ChatOllama(
                model=self.OLLAMA_MODEL,
                base_url=self.OLLAMA_HOST,
                temperature=0.3
            )

            # tools is just a list of tool objects created via @tool
            tools = [verify_song, open_youtube_video]

            # Build an agent that knows how to call tools
            agent = create_agent(model=llm, tools=tools,
                                 system_prompt=self.system_prompt,
                                 )

            # Wrap in an executor to run it
            result = agent.invoke({"messages": [HumanMessage(content=self.human_prompt)]},)
            print(result['messages'][-1].content)
            # result is a dict with "output" by default
            return result['messages'][-1].content
            # result.get("output", str(result))

        except Exception as e:
            return f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Music Assistant using Ollama + LangChain")
    parser.add_argument("--song", required=True, help="Song title or query")

    args = parser.parse_args()
    ma = MusicAssistant(args.song)

    output = ma.search_music_with_ollama()
    # print(output)


if __name__ == "__main__":
    main()
