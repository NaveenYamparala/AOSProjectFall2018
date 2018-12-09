# import re
# import sched
import socket
import threading
import time
from ntpath import split
from symbol import continue_stmt

from flask import Flask
from flask_spyne import Spyne
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.client import Client


app = Flask(__name__)
spyne = Spyne(app)

# Web Server URL's
webServerUrls = []

#Service Discovery Server URL
serviceDiscoveryServerURL = 'http://10.0.0.40:9000/servicediscovery?wsdl'

serversDictionary = {'key':'1'}
#s = sched.scheduler(time.time, time.sleep)

class AOSLoadBalancer(spyne.Service):
    __service_url_path__ = '/loadbalancer'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode,str)
    def registerServer(self,str):
        global webServerUrls
        webServerUrls.append(str)
   
    @spyne.srpc(Unicode,str, _returns=Unicode)
    def findBestServer(self,inputServersList):
        global serversDictionary
        inputServersList = inputServersList.split('-')
        if (serversDictionary is None):
            return "service Dictionary is not defined"
        keys = list(serversDictionary.keys())
        if (len(keys) != 0):
            bestCPU = 100
            for server in inputServersList:
                if (server in keys) & (serversDictionary[server] < bestCPU):
                    bestServer = server
            return bestServer
        else:
            return "service Dictionary is empty"

    @staticmethod
    def fetchLoadData():
        while True:
            global serversDictionary
            serversDictionary = {}
            urlArray = webServerUrls
            for url in urlArray:
                try:
                    client = Client(url)
                    key = url.split('?')[0]
                    serversDictionary[key] = client.service.ServerLoad()
                except Exception as ex:
                    x = ex
                    continue
            time.sleep(10)

if __name__ == '__main__':
    # Code to get local ip of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]

    discoveryClient = Client(serviceDiscoveryServerURL,timeout=100)
    discoveryClient.service.registerServer("",'http://'+ localIP + ':9005/loadbalancer?wsdl',True)

    thread = threading.Thread(target= app.run,args=('0.0.0.0',9005,None,None))
    #thread.daemon = True                            # Daemonize thread
    thread.start()
    AOSLoadBalancer.fetchLoadData()
    
    