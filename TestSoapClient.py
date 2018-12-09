from suds.client import Client


#url="http://www.thomas-bayer.com/axis2/services/BLZService?wsdl"
url = 'http://127.0.0.1:5000/aosprojectservices?wsdl'
client = Client(url)

for method in client.wsdl.services[0].ports[0].methods.values():    
    print method.name ## shows the details of this service
# for method in client.wsdl.services[0].ports:    
#     print method ## shows the details of this service

#print client.service.discover("Add")
# print client.service.Add(20,10)
# print client.service.Multiply(20,10)
print client.service.ServerLoad()
