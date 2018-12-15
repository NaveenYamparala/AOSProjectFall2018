import time
import threading
from email.mime import message
from os import errno
#from pip.cmdoptions import timeout
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
loadBalancerServerURL = []

lock = threading.Lock()

serviceDictionary = {'key':['1']}

class AOSServiceDiscovery(spyne.Service):
    __service_url_path__ = '/servicediscovery'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
  
           
    #Web service to find the server which provides the requested service
    @spyne.srpc(Unicode,Unicode, _returns= str)
    def discover(self,requestedService):
        try:
            global serviceDictionary,lock
            lock.acquire()
            filteredServers = []
            if (serviceDictionary is None):
                return "service Dictionary is not defined"
            keys = list(serviceDictionary.keys())
            if (len(keys) != 0):
                #Finds the Web servers in which the req service is available
                for key in keys:
                    for val in serviceDictionary[key]:
                        if (requestedService in val):
                            filteredServers.append(key)
                            continue
                if(len(filteredServers) == 0):
                    lock.release()
                    return "No server is available"
                else:
                    if(len(filteredServers)==1):
                        lock.release()
                        return filteredServers[0] + '?wsdl'
                    else:
                        try:
                            loadBalancerClient = Client(loadBalancerServerURL[0])
                        except Exception as e:
                            if hasattr(e,'errorno') and e.reason.errorno == 111:
                                loadBalancerClient = Client(loadBalancerServerURL[1])
                        
                        filteredServers = '-'.join(filteredServers)
                        #Requests load balancer to find the best server out of the available servers for requested service
                        x = loadBalancerClient.service.findBestServer("",filteredServers)
                        lock.release()
                        return unicode(x).encode('ascii','ignore') + '?wsdl'
            else:
                lock.release()
                return "service Dictionary is empty"
        except Exception as identifier:
            pass
        

    #Method to continously fetch services data from web servers
    @staticmethod
    def fetchServicesData():
        try:
            while True:
                global serviceDictionary,lock
                global webServerUrls,loadBalancerServerURL
                lock.acquire()
                serviceDictionary = {}
                urlArray = webServerUrls
                for url in urlArray:
                    try:
                        client = Client(url,cache = NoCache(),timeout=30)
                        key = url.split('?')[0]
                        serviceDictionary.update({key:[]})
                        for method in client.wsdl.services[0].ports[0].methods.values():    
                            serviceDictionary[key].append(method.name)
                    except Exception as e:
                        if hasattr(e,'reason') and e.reason.message == 'timed out':
                            webServerUrls.remove(url)
                        elif hasattr(e,'reason') and (e.reason.errno == 111 or e.reason.errno == 10061):
                            webServerUrls.remove(url)
                        continue

                for loadurl in loadBalancerServerURL:
                    try:
                        client = Client(loadurl,cache = NoCache(),timeout=30)
                    except Exception as e:
                        if hasattr(e,'reason') and e.reason.message == 'timed out':
                            loadBalancerServerURL.remove(loadurl)
                        elif hasattr(e,'reason') and (e.reason.errno == 111 or e.reason.errno == 10061):
                            loadBalancerServerURL.remove(loadurl)
                        continue
                lock.release()
                time.sleep(5)
        except Exception as identifier:
            pass
        

     
   #Web service to register Load, Web servers
    @spyne.srpc(Unicode,str,bool)
    def registerServer(self,str,isLoadBalancerServer = False):
        global webServerUrls
        global loadBalancerServerURL
        if(isLoadBalancerServer):
             loadBalancerServerURL.append(str)
        else:
            webServerUrls.append(str)
        

if __name__ == '__main__':
    #Spawns a thread to handle incoming requests
    thread = threading.Thread(target= app.run,args=('0.0.0.0',8082,None,None))
    thread.start()

    #Starts continous services data fetching from web servers
    AOSServiceDiscovery.fetchServicesData()
    
    