from suds.client import Client
url="http://www.thomas-bayer.com/axis2/services/BLZService?wsdl"
client = Client(url)
##print client ## shows the details of this service

result = client.service.getBank('34250000')
print result.bezeichnung ## see: restult.txt below