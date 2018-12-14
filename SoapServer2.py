import socket
import psutil
import time
from flask import Flask
from flask_spyne import Spyne
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.client import Client



app = Flask(__name__)
spyne = Spyne(app)

extraCPULoad = 0
reqCount = 0

class AOSProjectServices(spyne.Service):
    __service_url_path__ = '/aosprojectservices'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    #String Reverse Service
    @spyne.srpc(Unicode, _returns = Unicode)
    def stringReverse(str):
        global extraCPULoad 
        global reqCount 
        extraCPULoad = extraCPULoad + 1
        reqCount = reqCount + 1
        # time.sleep(3)
        reversedString = ''
        index = len(str)
        while index:
            index -= 1                       
            reversedString += str[index]
        return 'Server 2 -> ' + reversedString

    #Add Service
    @spyne.srpc(float,float,_returns = str)
    def Add(num1,num2):
        global extraCPULoad 
        global reqCount 
        extraCPULoad = extraCPULoad + 1
        reqCount = reqCount + 1
        # time.sleep(1)
        return 'Server 2 -> ' + str(num1 + num2)

    #Multiply Service
    @spyne.srpc(float,float,_returns = str)
    def Multiply(num1,num2):
        global extraCPULoad 
        global reqCount 
        extraCPULoad = extraCPULoad + 1
        reqCount = reqCount + 1
        # time.sleep(2)
        return 'Server 2 -> ' + str(num1 * num2)

    #Service to return server load to Load Balancing server
    @spyne.srpc(_returns = float)
    def ServerLoad():
        #return psutil.cpu_percent() + extraCPULoad
        return 20 + extraCPULoad

    #Service to find the number of requests handled by web server
    @spyne.srpc(_returns = str)
    def RequestCount():
        return 'Server 2 -> ' + str(reqCount)

if __name__ == '__main__':
    # Code to get local ip of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]


    #Service Discovery Server URL
    serviceDiscoveryServerURL = ['http://'+ localIP +':8082/servicediscovery?wsdl','http://'+localIP+':8083/servicediscovery?wsdl']

    #Load Balancing Server URL
    loadBalancingServerURL = ['http://'+ localIP +':9005/loadbalancer?wsdl','http://'+localIP+':9006/loadbalancer?wsdl']

    #To registers webserver with Service Discovery server
    for server in serviceDiscoveryServerURL:
        discoveryClient = Client(server,timeout=5)
        discoveryClient.service.registerServer("",'http://'+ localIP + ':9000/aosprojectservices?wsdl')

    #To register webserver with Load balancing server
    for server in loadBalancingServerURL:
        loadBalancerClient = Client(server,timeout=5)
        loadBalancerClient.service.registerServer("",'http://'+ localIP + ':9000/aosprojectservices?wsdl')

    #Runs the webserver
    app.run(host = '0.0.0.0',port=9000)
