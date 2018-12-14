
#File to get the requests serviced by each server and their final loads
from suds.client import Client
import socket

# Code to get local ip of the machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("7.7.7.7", 80))
localIP = s.getsockname()[0]


serverUrl = 'http://'+localIP+':8000/aosprojectservices?wsdl'
WebClient = Client(serverUrl,timeout=100)
print 'Request Count -> '+ WebClient.service.RequestCount()
print 'SeverLoad -> ' + str(WebClient.service.ServerLoad())

serverUrl2 = 'http://'+localIP+':9000/aosprojectservices?wsdl'
WebClient2 = Client(serverUrl2,timeout=100)
print 'Request Count -> '+ WebClient2.service.RequestCount()
print 'SeverLoad -> ' + str(WebClient2.service.ServerLoad())

serverUrl3 = 'http://'+localIP+':10000/aosprojectservices?wsdl'
WebClient3 = Client(serverUrl3,timeout=100)
print 'Request Count -> '+ WebClient3.service.RequestCount()
print 'SeverLoad -> ' + str(WebClient3.service.ServerLoad())