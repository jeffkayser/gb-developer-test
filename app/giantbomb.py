import requests

BASE_URL = "https://www.giantbomb.com/api"
USER_AGENT = "GravieBot 0.00 by jeffmk"
HEADERS = {
    "User-Agent": USER_AGENT,
}


def search(query, api_key, page_num=1):
    url = f"{BASE_URL}/search/"
    r = requests.get(
        url,
        headers=HEADERS,
        params={
            "api_key": api_key,
            "format": "json",
            "query": query,
            "resources": ["game"],
            "page": page_num,
        },
    )
    return r


def get_games(guids, api_key):
    session = requests.session()
    results = []
    for guid in sorted(guids):
        url = f"{BASE_URL}/game/{guid}/"
        r = session.get(
            url,
            headers=HEADERS,
            params={
                "api_key": api_key,
                "format": "json",
                "guid": guid,
            },
        )
        results.append(r.json()["results"])
    return results
