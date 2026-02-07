import requests
from langchain_core.tools import tool

@tool
def verify_song(track, artist):
    """
    verifies if song and artist combination is present in music brainz database or not.
    Input should be two params: the track name and artist name .
           param
           track: str
           artist: str
    """
    url = "https://musicbrainz.org/ws/2/recording/"
    params = {
        "query": f'recording:"{track}" AND artist:"{artist}"',
        "fmt": "json",
        "limit": 1
    }
    headers = {"User-Agent": "LLM-Verifier/1.0"}
    r = requests.get(url, params=params, headers=headers)

    if r.status_code != 200:
        return {"found": False}

    r = r.json()
    if r['count'] == 0:
        return {"found": False}
    song_found = r['recordings'][0]['title']
    return {"found": True, "song_title": song_found}

# x = verify_song("tum hi ho", "arijita singh")
# print(x)