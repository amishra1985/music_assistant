from mcp.server.fastmcp import FastMCP
import logging


mcp = FastMCP("tools_server")
logging.info("Starting MCP server with FastMCP...")


@mcp.tool()
def open_youtube_video(title: str) -> dict:
    """
           Opens a specific YouTube video in the web browser.
           Input should be the title of the YouTube video only.
           param
           title: str
    """
    # selenium 4
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    from selenium.webdriver.chrome.options import Options
    from tools_helpers.play_on_youtube import search_youtube_music

    logging.info(f"title received from AI agent: {title}")
    songs: list = search_youtube_music(title)

    if not songs:
        return {
            "status": "not_found",
            "message": f"No results found for '{title}'"
        }

    # pick the first match
    url = songs[0]["url"]

    logging.info(f"playing url: {url}")

    # 3. Attach Selenium to the existing Chrome session

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    return {
        "status": "playing",
        "title": songs[0]["title"],
        "url": url
    }





if __name__ == "__main__":
    mcp.run(transport="stdio")