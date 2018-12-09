import time
import threading
from re import split

import suds
from flask import Flask
from flask_spyne import Spyne
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.cache import NoCache
from suds.client import Client


app = Flask(__name__)
spyne = Spyne(app)

# Web Server URL's
webServerUrls = []

#Load Balncer Server URL
loadBalancerServerURL = ''

serviceDictionary = {'key':['1']}

class AOSServiceDiscovery(spyne.Service):
    __service_url_path__ = '/servicediscovery'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
   
    @spyne.srpc(Unicode,str,bool)
    def registerServer(self,str,isLoadBalancerServer = False):
        global webServerUrls
        global loadBalancerServerURL
        if(isLoadBalancerServer):
             loadBalancerServerURL = str
        else:
            webServerUrls.append(str)
           

    @spyne.srpc(Unicode,Unicode, _returns= Unicode)
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
                if(len(filteredServers)==0):
                    return filteredServers[0] + '?wsdl'
                else:
                     loadBalancerClient = Client(loadBalancerServerURL)
                     filteredServers = '-'.join(filteredServers)
                     x = loadBalancerClient.service.findBestServer("",filteredServers)
                     return unicode(x).encode('ascii','ignore') + '?wsdl'
        else:
            return "service Dictionary is empty"

    @staticmethod
    def fetchServicesData():
        while True:
            global serviceDictionary
            serviceDictionary = {}
            urlArray = webServerUrls
            for url in urlArray:
                try:
                    client = Client(url,cache = NoCache())
                    key = url.split('?')[0]
                    serviceDictionary.update({key:[]})
                    for method in client.wsdl.services[0].ports[0].methods.values():    
                        serviceDictionary[key].append(method.name)
                except Exception as e:
                    x = e
                    continue
            time.sleep(10)
        

if __name__ == '__main__':
    thread = threading.Thread(target= app.run,args=('0.0.0.0',9000,None,None))
    #thread.daemon = True                            # Daemonize thread
    thread.start()
    AOSServiceDiscovery.fetchServicesData()
    
    