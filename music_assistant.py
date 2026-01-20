import os
import argparse
from tools.play_on_youtube import open_youtube_video
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


class MusicAssistant:
    """
    AI Agent that can take your input and play song on YouTube music.
    start chrome in debugger mode: "c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory=Default --user-data-dir="C:\ChromeDebug"
    """
    OLLAMA_MODEL = "llama3.2:latest"
    OLLAMA_HOST = "http://localhost:11434"

    # os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

    system_prompt = """
                    You are a music assistant.
                    
                    Your job:
                    1. Understand what the user wants.
                    2. If they want to play or open a song on YouTube music, call the appropriate tool.
                    3. The user wants title that includes only music videos
                    
                    When calling the tool, you MUST provide ONLY the allowed argument fields.
                    The tool open_youtube_video accepts exactly one argument:
                    
                    {"title": "<song title>"}
                    
                    Do NOT include any other fields such as "movie", "actor", "id", or anything else.
                    If you include extra fields, the tool call will fail.
                    
                    
                    """

    def __init__(self, query):
        self.human_prompt = query

    def search_music_with_ollama(self) -> str:
        try:
            # llm = Ollama(model=self.OLLAMA_MODEL)
            llm = ChatOllama(
                model=self.OLLAMA_MODEL,
                base_url=self.OLLAMA_HOST,
                temperature=0.7
            )

            # tools is just a list of tool objects created via @tool
            tools = [open_youtube_video]

            # Build an agent that knows how to call tools
            agent = create_agent(model=llm, tools=tools,
                                 system_prompt=self.system_prompt,
                                 )

            # Wrap in an executor to run it
            result = agent.invoke({"messages": [HumanMessage(content=self.human_prompt)]})
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
