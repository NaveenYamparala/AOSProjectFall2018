import socket
import threading
import time
from imp import acquire_lock
from ntpath import split
from platform import release
from symbol import continue_stmt
from sys import maxint

from flask import Flask
from flask_spyne import Spyne
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.cache import NoCache
from suds.client import Client
import sys


app = Flask(__name__)
spyne = Spyne(app)

# Web Server URL's
webServerUrls = []

serversDictionary = {'key':'1'}



#s = sched.scheduler(time.time, time.sleep)
lock = threading.Lock()

class AOSLoadBalancer(spyne.Service):
    __service_url_path__ = '/loadbalancer'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
   
   #Webservice used by Service discovery server to get the best available
   #server after load balancing
    @spyne.srpc(Unicode,str, _returns=Unicode)
    def findBestServer(self,inputServersList):
        global serversDictionary,lock
        lock.acquire()
        try:
            inputServersList = inputServersList.split('-')
            if (serversDictionary is None):
                return "service Dictionary is not defined"
            keys = list(serversDictionary.keys())
            if (len(keys) != 0):
                bestCPU = sys.maxint
                bestServer = inputServersList[0]
                for server in inputServersList:
                    if (server in keys) & (serversDictionary[server] < bestCPU):
                        bestServer = server
                        bestCPU = serversDictionary[server]
                lock.release()
                return bestServer
            else:
                lock.release()
                return "service Dictionary is empty"
        except Exception as e:
            lock.release()

    #Method to continously fetch load data from Webservers
    @staticmethod
    def fetchLoadData():
        while True:
            global serversDictionary,lock
            lock.acquire()
            serversDictionary = {}
            urlArray = webServerUrls
            for url in urlArray:
                try:
                    client = Client(url,cache = NoCache(),timeout=30)
                    key = url.split('?')[0]
                    serversDictionary[key] = client.service.ServerLoad()
                except Exception as e:
                    if hasattr(e,'reason') and e.reason.message == 'timed out':
                        webServerUrls.remove(url)
                    elif hasattr(e,'reason') and (e.reason.errno == 111 or e.reason.errno == 10061):
                        webServerUrls.remove(url)
                    continue
            lock.release()
            time.sleep(1)

    #Webservice to register web servers
    @spyne.srpc(Unicode,str)
    def registerServer(self,str):
        global webServerUrls
        webServerUrls.append(str)

if __name__ == '__main__':
    # Code to get local ip of the machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]

    #Service Discovery Server URL
    serviceDiscoveryServerURL = ['http://'+ localIP +':8082/servicediscovery?wsdl','http://'+localIP+':8083/servicediscovery?wsdl']


    #To register Load balncing server with service discovery server
    for server in serviceDiscoveryServerURL:
        try:
            discoveryClient = Client(server,timeout=5)
            discoveryClient.service.registerServer("",'http://'+ localIP + ':9005/loadbalancer?wsdl',True)
        except Exception as identifier:
            continue
        
    thread = threading.Thread(target= app.run,args=('0.0.0.0',9005,None,None))
    thread.start()
    
    AOSLoadBalancer.fetchLoadData()
    
    