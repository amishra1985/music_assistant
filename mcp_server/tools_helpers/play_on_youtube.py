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
