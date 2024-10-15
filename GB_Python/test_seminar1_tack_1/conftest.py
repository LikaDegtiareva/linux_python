import pytest
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def good_text():
    return "Cобака"

@pytest.fixture()
def bad_text():
    return "Cабака"

