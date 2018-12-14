from suds.client import Client
import socket

# Code to get local ip of the machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("7.7.7.7", 80))
localIP = s.getsockname()[0]

try:
    discoveryUrl = 'http://'+localIP+':8082/servicediscovery?wsdl'
    discoveryClient = Client(discoveryUrl,timeout=100)
except Exception as identifier:
    discoveryUrl = 'http://'+localIP+':8083/servicediscovery?wsdl'
    discoveryClient = Client(discoveryUrl,timeout=100)


serviceRequired = raw_input("Enter number of required service ( 1 --> Add, 2 - Multiply, 3 --> String Reverse ) \n")


try:
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
except Exception as identifier:
    x=identifier
    pass

