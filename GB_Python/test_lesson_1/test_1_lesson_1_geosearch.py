import requests
S = requests.Session()

def get_sites(lat, long, radius, limit=100):
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "format": "json",
        "list": "geosearch",
        "gscoord": f"{lat}|{long}",
        "gslimit": f"{limit}",
        "gsradius": f"{radius}",
        "action": "query"
    }
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PLACES = DATA['query']['geosearch']
    sites = [i["title"] for i in PLACES]
    return sites

def test_step1():
    assert "One Montgomery Tower" in get_sites("37.7891838", "-122.4033522", 100), "not found"

test_step1()