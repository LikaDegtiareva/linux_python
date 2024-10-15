#не доделан из-за очень длин.подписи

from zeep import Client, Settings

wsdl = "http://dss.cryptopro.ru/verify/service.svc?wsdl"
sign = ""

settings = Settings(strict=False)

client = Client(wsdl=wsdl, settings=settings)

#def test_step1():
#    assert client.service.VerifySignature('CMS', sign)['Resilt']