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

#Service Discovery Server URL
serviceDiscoveryServerURL = 'http://10.0.0.40:9000/servicediscovery?wsdl'

#Load Balancing Server URL
loadBalancingServerURL = 'http://10.0.0.40:9005/loadbalancer?wsdl'

class AOSProjectServices(spyne.Service):
    __service_url_path__ = '/aosprojectservices'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, _returns = Unicode)
    def stringReverse(str):
        time.sleep(10)
        reversedString = ''
        index = len(str)
        while index:
            index -= 1                       
            reversedString += str[index]
        return reversedString


    @spyne.srpc(float,float,_returns = float)
    def Add(num1,num2):
        time.sleep(3)
        return num1 + num2


    @spyne.srpc(float,float,_returns = float)
    def Multiply(num1,num2):
        time.sleep(6)
        return num1 * num2

   
    @spyne.srpc(_returns = float)
    def ServerLoad():
        return psutil.cpu_percent()

if __name__ == '__main__':
    # Code to get local ip of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]

    discoveryClient = Client(serviceDiscoveryServerURL,timeout=100)
    discoveryClient.service.registerServer("",'http://'+ localIP + ':8000/aosprojectservices?wsdl')

    loadBalancerClient = Client(loadBalancingServerURL,timeout=100)
    loadBalancerClient.service.registerServer("",'http://'+ localIP + ':8000/aosprojectservices?wsdl')

    app.run(host = '0.0.0.0',port=8005)
