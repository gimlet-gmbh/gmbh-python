import os

import options as opts
import rpc_client as req
import rpc_server as serv
import data as data
import time
from threading import Thread, Lock
import enum

def fromClient():
    print("cli-ent")

State = enum.Enum('State', 'Connected Disconnected')

class registration:
    def __init__(self, id, address, fingerprint):
        self.id = id
        self.mode = ""
        self.address = address
        self.fingerprint = fingerprint

class client:

    def __init__(self, opts=opts.new()):

        self._registration = None
        self._con = None
        self.state = None

        self._registeredFunctions = {}
        self._whoIs = {}

        self._myAddress = ""
        self._parentID = ""
        self._env = os.environ.get('ENV')
        self._closed = False

        self._opts = opts
        self.mu = Lock()

        if self._opts.service.name == "":
            raise Exception("service name cannot be empty")
        if self._opts.service.name == "CoreData":
            raise Exception("\"CoreData\" is a reserved service name")

        if self._env == "C":
            self._myAddress = os.environ.get('ADDR')
            self._req = req.requester(self._myAddress, self._opts, self._env)
            print("using core address from environment=",self._myAddress)
        else:
            self._req = req.requester(self._opts.standalone.coreAddress, self._opts, self._env)
            print("core address=", self._opts.standalone.coreAddress)

        print("                    _                 ")
        print("  _  ._ _  |_  |_| /  | o  _  ._ _|_  ")
        print(" (_| | | | |_) | | \\_ | | (/_ | | |_ ")
        print("  _|                                  ")
        print("service started from", os.path.dirname(os.path.realpath(__file__)))
        print("PeerGroup=",self._opts.service.peerGroups)
    
    def start(self):
        if self._opts.runtime.blocking :
            self.__start()
        else:
            t = Thread(target = self.__start())
            t.start()

    def __start(self):

        print("Should print __connect() time here")
        t = Thread(target = self.__connect())
        t.start()

    def __shutdown(self):
        print("shutdown...")

    def __connect(self):
        print("attempting to connect to coreData")

        # If the service is already registered, then exit
        if self.state == State.Connected:
            print("state reported as connected; thread closing")
            return

        # Get a registration and print the details. 
        # If the address was not received, then exit
        reg = self._req.register()
        if reg.address == "":
            print("registration address not received")
        
        print("registration details:")
        print("id=" + str(reg.id) + "; address=" +
              str(reg.address) + "; fingerprint=" + reg.fingerprint)

        self.mu.acquire()
        try:
            self._registration = reg
            # self._con = newcabalconnect
            self.state = State.Connected
        finally:
            self.mu.release()

    def __disconnect(self):
        print("disconnecting from gmbh-core")




    # def __init__(self, registration, options, rpcConnection, registeredFunc, timeDuration, address, state, parentID, whoIs, msgCounter, mu, errors, warnings, env, closed):
    #     self.registration = registration
    #     self.options = options
    #     self.rpcConnection = rpcConnection
    #     self. registeredFunc = registeredFunc
    #     self.timeDuration = timeDuration
    #     self.address = address
    #     self.state = state
    #     self.parentID = parentID
    #     self.whoIs = whoIs
    #     self.msgCounter = msgCounter
    #     self.mu = mu
    #     self.errors = errors
    #     self.warnings = warnings
    #     self.env = env
    #     self.closed = closed
    
    # NewClient should be called only once. It returns the object in which parameters, and
    # handler functions can be attached to gmbh Client.
    # def NewClient(self, *opts):
        
    # Start()
    # Shutdown(src)
    # resolveAddress(target)
    # disconnect()
    # failed
    # makeUnregisterRequest()
    # getReg()
    


# if __name__ == '__main__':
#     cli = Client("reg", "options", "rpc", "register", 10, "addy", "state", 1, "whois", 0, "mu", "errors", "warnings", "env", "closed")
#     cli.NewClient("option1", "option2", "option3")

    
