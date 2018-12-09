#import socket
from flask import Flask
from flask_spyne import Spyne
from re import split
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.client import Client
import re
import sched
import time
import threading

app = Flask(__name__)
spyne = Spyne(app)

serviceDictionary = {'key':['1']}
s = sched.scheduler(time.time, time.sleep)

class AOSServiceDiscovery(spyne.Service):
    __service_url_path__ = '/servicediscovery'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
   
    @spyne.srpc(Unicode,Unicode, _returns=Unicode)
    def discover(self,str):
        # serviceDictionary = {}
        # urlArray = ['http://127.0.1.1:5000/AOSProjectServices?wsdl']
        # for url in urlArray:
        #     client = Client(url)
        #     key = url.split('?')[0]
        #     serviceDictionary.update({key:[]})
        #     for method in client.wsdl.services[0].ports[0].methods.values():    
        #         serviceDictionary[key].append(method.name)
 # thread = threading.Thread(target= x.fetchServicesData,args=())
    # #thread.daemon = True                            # Daemonize thread
    # thread.start()
        x = AOSServiceDiscovery()
        serviceDictionary = x.fetchServicesData()
        filteredServers = []
        if (serviceDictionary is None):
            return "service Dictionary is not defined"
        keys = list(serviceDictionary.keys())
        if (len(keys) != 0):
            for key in keys:
                for val in serviceDictionary[key]:
                    if (str in val):
                        filteredServers.append(key)
                        continue
            if(len(filteredServers) == 0):
                return "filtered servers is 0"
            else:
                return filteredServers[0]
        else:
            return "service Dictionary is empty"

   
    def fetchServicesData(self):
        #while True:
            serviceDictionary = {}
            urlArray = ['http://127.0.1.1:5000/AOSProjectServices?wsdl']
            for url in urlArray:
                client = Client(url)
                key = url.split('?')[0]
                serviceDictionary.update({key:[]})
                for method in client.wsdl.services[0].ports[0].methods.values():    
                    serviceDictionary[key].append(method.name)
            return serviceDictionary
            #time.sleep(10)
        
        
# ip_address = socket.gethostbyname(socket.gethostname())
# print ip_address

if __name__ == '__main__':
    #x = AOSServiceDiscovery()
    # thread = threading.Thread(target= x.fetchServicesData,args=())
    # #thread.daemon = True                            # Daemonize thread
    # thread.start()
    #x.fetchServicesData()
    app.run(host='127.0.2.1')
    
