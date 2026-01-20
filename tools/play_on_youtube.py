from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from langchain_core.tools import tool
import requests
import json

def search_youtube_music(title: str):
    url = "https://music.youtube.com/youtubei/v1/search"

    payload = {
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "1.20230101.01.00"
            }
        },
        "query": title
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()

    results = []

    # Parse YouTube Music search results
    sections = data.get("contents", {}) \
                   .get("tabbedSearchResultsRenderer", {}) \
                   .get("tabs", [])[0] \
                   .get("tabRenderer", {}) \
                   .get("content", {}) \
                   .get("sectionListRenderer", {}) \
                   .get("contents", [])

    for section in sections:
        items = section.get("musicShelfRenderer", {}).get("contents", [])
        for item in items:
            info = item.get("musicResponsiveListItemRenderer", {})
            title = info.get("flexColumns", [])[0] \
                        .get("musicResponsiveListItemFlexColumnRenderer", {}) \
                        .get("text", {}) \
                        .get("runs", [])[0] \
                        .get("text", "")

            video_id = info.get("playlistItemData", {}).get("videoId", None)

            if video_id:
                results.append({
                    "title": title,
                    "videoId": video_id,
                    "url": f"https://music.youtube.com/watch?v={video_id}"
                })

    return results



@tool
def open_youtube_video(title: str) -> str:
    """
           Opens a specific YouTube video in the web browser.
           Input should be the title of the YouTube video only.
           param
           title: str
    """
    print(f"title received from AI agent: {title}")
    songs = search_youtube_music(title)

    # pick the first match
    url = songs[0]["url"]

    print(f"playing url: {url}")

    # 3. Attach Selenium to the existing Chrome session

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    return f"Opened in same tab: {url}"
