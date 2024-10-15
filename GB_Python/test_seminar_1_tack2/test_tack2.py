import requests
import yaml
with open("config.yaml") as f:
    data = yaml.safe_load(f)

def test_step1(login, testtext1):
    header = {"X-Auth-Token": login}
    res = requests.get(data["address"]+"api/posts", params={"owner":"notMe"}, headers=header)
    lisres = [i["title"] for i in res.json()["data"]]
    assert testtext1 in lisres