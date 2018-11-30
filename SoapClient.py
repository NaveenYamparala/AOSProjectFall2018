from suds.client import Client
#url="http://www.thomas-bayer.com/axis2/services/BLZService?wsdl"
url = 'http://127.0.0.1:5000/aosprojectservices?wsdl'
client = Client(url)
#print client ## shows the details of this service

print client.service.stringReverse("Naveen")
print client.service.Add(20,10)
print client.service.Multiply(20,10)