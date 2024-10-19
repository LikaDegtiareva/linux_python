import requests

from Connection import Connection

connection = Connection("config.yaml")

def test_step1(login, testtext1):
    header = {"X-Auth-Token": login}
    res = requests.get(connection.host+"api/posts", params={"owner":"notMe"}, headers=header)
    lisres = [i["title"] for i in res.json()["data"]]
    assert testtext1 in lisres

def test_create_post(login, new_post):
    x_auth_token = {"X-Auth-Token": login}
    res = requests.post(connection.host + "api/posts", headers=x_auth_token, data=new_post.payload())
    assert res.status_code == 200