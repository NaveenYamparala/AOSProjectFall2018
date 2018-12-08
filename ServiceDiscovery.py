from flask import Flask
from flask_spyne import Spyne
from re import split
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.client import Client
# import re
# import sched
import time
import threading

app = Flask(__name__)
spyne = Spyne(app)

serviceDictionary = {'key':['1']}

class AOSServiceDiscovery(spyne.Service):
    __service_url_path__ = '/servicediscovery'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
   
    @spyne.srpc(Unicode,Unicode, _returns=Unicode)
    def discover(self,str):
        global serviceDictionary
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
                if(len(filteredServers)==1):
                    return filteredServers[0] + '?wsdl'
                else:
                     loadBalancerClient = Client('http://127.0.3.1:5000/aosprojectservices?wsdl')
                     return loadBalancerClient.service.findBestServer("",filteredServers)
        else:
            return "service Dictionary is empty"

    @staticmethod
    def fetchServicesData():
        while True:
            global serviceDictionary
            serviceDictionary = {}
            urlArray = ['http://127.0.1.1:5000/aosprojectservices?wsdl']
            for url in urlArray:
                client = Client(url)
                key = url.split('?')[0]
                serviceDictionary.update({key:[]})
                for method in client.wsdl.services[0].ports[0].methods.values():    
                    serviceDictionary[key].append(method.name)
            time.sleep(10)
        

if __name__ == '__main__':
    thread = threading.Thread(target= app.run,args=('127.0.2.1',None,None,None))
    #thread.daemon = True                            # Daemonize thread
    thread.start()
    AOSServiceDiscovery.fetchServicesData()
    
    