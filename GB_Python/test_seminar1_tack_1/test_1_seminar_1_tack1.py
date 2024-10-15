import yaml
from zeep import Client, Settings

with open ("config.yaml") as f:
    data = yaml.safe_load(f)

wsdl = data[0]["wsdl"]
settings = Settings(strict=False)
client = Client(wsdl=wsdl, settings=settings)

def checkText(text):
    response = client.service.checkText(text)
    return response[0]["s"]