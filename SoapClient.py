from suds.client import Client
#url="http://www.thomas-bayer.com/axis2/services/BLZService?wsdl"
discoveryUrl = 'http://127.0.2.1:5000/servicediscovery?wsdl'
discoveryClient = Client(discoveryUrl)
#print client ## shows the details of this service

# print client.service.stringReverse("Naveen")
# print client.service.Add(20,10)
# print client.service.Multiply(20,10)

serviceUrl = discoveryClient.service.discover("Add")
serviceClient = Client(serviceUrl)
print serviceClient.service.Add(250,10)


