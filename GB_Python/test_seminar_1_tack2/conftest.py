import pytest
import yaml
import requests
from lxml.html.diff import token
from Post import Post
from Connection import Connection

connection = Connection("config.yaml")

@pytest.fixture
def login():
    res1 = requests.post(
        url=connection.host + "gateway/login",
        data={"username":connection.username, "password": connection.password}
    )
    print(res1.content)
    return res1.json()["token"]

@pytest.fixture
def testtext1():
    return "Test post 8"


@pytest.fixture
def new_post():
    return Post("config.yaml")

