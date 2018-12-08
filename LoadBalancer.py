# import re
# import sched
import threading
import time
# from os.path import split
# from re import split

from flask import Flask
from flask_spyne import Spyne
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from suds.client import Client


app = Flask(__name__)
spyne = Spyne(app)

serversDictionary = {'key':'1'}
#s = sched.scheduler(time.time, time.sleep)

class AOSLoadBalancer(spyne.Service):
    __service_url_path__ = '/loadbalancer'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
   
    @spyne.srpc(Unicode,Unicode, _returns=Unicode)
    def findBestServer(self,inputServersList = []):
        global serversDictionary
        filteredServers = []
        if (serversDictionary is None):
            return "service Dictionary is not defined"
        keys = list(serversDictionary.keys())
        if (len(keys) != 0):
            bestCPU = 0
            for server in inputServersList:
                if (server in serversDictionary) & serversDictionary[server] < int(bestCPU):
                    bestServer = server
            return bestServer
        else:
            return "service Dictionary is empty"

    @staticmethod
    def fetchLoadData():
        while True:
            global serversDictionary
            serversDictionary = {}
            urlArray = ['http://127.0.1.1:5000/aosprojectservices?wsdl']
            for url in urlArray:
                client = Client(url)
                key = url.split('?')[0]
                serversDictionary.update({key:[]})
                serversDictionary[key].append(client.service.ServerLoad())
            time.sleep(10)

if __name__ == '__main__':
    thread = threading.Thread(target= app.run,args=('127.0.3.1',None,None,None))
    #thread.daemon = True                            # Daemonize thread
    thread.start()
    AOSLoadBalancer.fetchLoadData()
    
    