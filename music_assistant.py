# python
import os
import sys
import argparse
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import tracemalloc
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
tracemalloc.start()


class MusicAssistant:
    """
    AI Agent that can take your input and play song on YouTube music.
    start chrome in debugger mode: "c:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --profile-directory=Default --user-data-dir="C:\ChromeDebug"
    """
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2-7b-chat")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    system_prompt = """
You are a music assistant.

Your job is to understand user requests about music and call a tool.

You must:
1. Accept natural language input, even if vague, misspelled, or conversational.
2. Infer the most likely song title, artist, and any useful metadata.
3. Normalize song titles and artist names (remove filler words like "play", "song", "track", etc.).
4. If the user intent is to play or search for a song, call the appropriate tool.
5. If multiple interpretations are possible, choose the most likely one based on popularity and context.
6. Only ask a clarification question if confidence is very low.

When calling a tool:
- Always provide structured arguments.
- Never include extra text outside the tool call.
- Do not explain your reasoning.

If the user is asking a general question about music (facts, lyrics meaning, recommendations), respond in plain text and do NOT call a tool.

When calling the tool, you MUST provide ONLY the allowed argument fields.
The tool open_youtube_video accepts exactly one argument:

{"title": "<song title>"}

Do NOT include any other fields such as "movie", "actor", "id", or anything else.
If you include extra fields, the tool call will fail.
"""

    def __init__(self, query):
        self.human_prompt = query

    async def load_tools(self):
        # Use the same Python interpreter and unbuffered stdio for a stable subprocess.
        client = MultiServerMCPClient(
            {
                "tools_server": {
                    "transport": "stdio",
                    "command": sys.executable,
                    "args": [
                        "-u",
                        r"C:\Users\amita\PycharmProjects\music_assistant\mcp_server\my_mcp.py",
                    ],
                }
            }
        )

        tools = await client.get_tools()
        return tools

    async def search_music_with_ollama(self) -> str:
        try:
            llm = ChatOllama(
                model=self.OLLAMA_MODEL,
                base_url=self.OLLAMA_HOST,
                temperature=0.0
            )

            # await the async tool loader
            tools = await self.load_tools()

            # Build an agent that knows how to call tools
            agent = create_agent(model=llm, tools=tools,
                                 system_prompt=self.system_prompt,
                                 checkpointer=InMemorySaver())

            # Run the agent asynchronously
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": self.human_prompt}]},
                {"configurable": {"thread_id": "1"}},
            )
            # result = await agent.ainvoke({"messages": [HumanMessage(content=self.human_prompt)]})
            print(result['messages'][-1].content)
            return result['messages'][-1].content

        except Exception as e:
            return f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Music Assistant using Ollama + LangChain")
    parser.add_argument("--song", required=True, help="Song title or query")

    args = parser.parse_args()
    ma = MusicAssistant(args.song)

    output = asyncio.run(ma.search_music_with_ollama())
    print(output)


if __name__ == "__main__":
    main()
