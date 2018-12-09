from suds.client import Client
#url="http://www.thomas-bayer.com/axis2/services/BLZService?wsdl"
discoveryUrl = 'http://10.0.0.40:9000/servicediscovery?wsdl'
discoveryClient = Client(discoveryUrl,timeout=100)
#print client ## shows the details of this service

# print client.service.stringReverse("Naveen")
# print client.service.Add(20,10)
# print client.service.Multiply(20,10)
serviceRequired = raw_input("Enter number of required service ( 1 --> Add, 2 - Multiply, 3 --> String Reverse ) \n")

if serviceRequired == '1':
    serviceUrl = discoveryClient.service.discover("","Add")
    serviceClient = Client(serviceUrl,timeout=100)
    print serviceClient.service.Add(250,50)
elif serviceRequired == '2':
    serviceUrl = discoveryClient.service.discover("","Multiply")
    serviceClient = Client(serviceUrl)
    print serviceClient.service.Multiply(250,50)
elif serviceRequired == '3':
    serviceUrl = discoveryClient.service.discover("","stringReverse")
    serviceClient = Client(serviceUrl)
    print serviceClient.service.stringReverse('OperatingSystems')
else:
    print "Enter proper service name"

