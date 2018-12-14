from suds.cache import NoCache
from suds.client import Client
import socket
import time

# Code to get local ip of the machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("7.7.7.7", 80))
localIP = s.getsockname()[0]

try:
    discoveryUrl = 'http://'+localIP+':8082/servicediscovery?wsdl'
    discoveryClient = Client(discoveryUrl,cache = NoCache(),timeout=100)
except Exception as identifier:
    discoveryUrl = 'http://'+localIP+':8083/servicediscovery?wsdl'
    discoveryClient = Client(discoveryUrl,cache = NoCache(),timeout=100)

#Number of requests
i = 100
start = time.time()
while i > 0:
    serviceUrl = discoveryClient.service.discover("","stringReverse")
    serviceClient = Client(serviceUrl,cache = NoCache(),timeout=5)
    print serviceClient.service.stringReverse('AOS')
    print i
    i = i-1
end = time.time()

print 'completed'
print end - start
