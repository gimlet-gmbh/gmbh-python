import os

import options as opts
import rpc_client
import rpc_server as serv
import data as data
import datetime
import signal
import time
from threading import Thread, Lock
import enum

State = enum.Enum('State', 'Connected Disconnected')
global g

class registration:
    def __init__(self, id, address, fingerprint):
        self.id = id
        self.mode = ""
        self.address = address
        self.fingerprint = fingerprint

class connection:
    def __init__(self, address, server, connected):
        self._server = None
        self._address = ""
        self._connected = False

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

        # If the conection is meant to be closed or not
        self._closed = False

        self._opts = opts
        self.mu = Lock()

        if self._opts.service.name == "":
            raise Exception("service name cannot be empty")
        if self._opts.service.name == "CoreData":
            raise Exception("\"CoreData\" is a reserved service name")

        if self._env == "C":
            self._myAddress = os.environ.get('ADDR')
            # self._req = req.requester(self._myAddress, self._opts, self._env)
            print("using core address from environment=",self._myAddress)
        else:
            # self._req = req.requester(self._opts.standalone.coreAddress, self._opts, self._env)
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
        if self._env == "M":
            print("managed mode; ignoring sigint; listening for sigusr2")
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGUSR2, self.__shutdown)
        else:
            signal.signal(signal.SIGINT, self.__shutdown)

        d = datetime.datetime.now()
        print("started, time=" + d.isoformat('T'))
        t = Thread(target = self.__connect())
        t.start()

        signal.pause()

    def __connect(self):
        print("attempting to connect to coreData")

        # If the service is already registered, then exit
        if self.state == State.Connected:
            print("state reported as connected; thread closing")
            return

        # Get a registration and print the details. 
        # If the address was not received, then exit
        while True:
            try:
                reg = rpc_client.register(
                    self._opts.standalone.coreAddress,
                    self._opts.service.name,
                    self._opts.service.aliases,
                    self._opts.service.peerGroups,
                    self._env)

                break
            except:
                pass

        
        print("registration details:")
        print("id=" + str(reg.id) + "; address=" +
              str(reg.address) + "; fingerprint=" + reg.fingerprint)

        if reg.address == "":
            print("registration address not received")
            return
            
        self.mu.acquire()
        try:
            self._registration = reg
            self._con = connection(reg.address, serv.CabalServicer(), False)
            self.state = State.Connected
        finally:
            self.mu.release()

        print("connected; coreAddress=(" + reg.address + ")")

# client needs to listen for shutdown notification in the server
# need to pass options and environment as parameters

    def __shutdown(self, signum, frame):
            print("shutdown procedures started...")

            self.mu.acquire()
            try:
                self._closed = True
                self.registration = None
            finally:
                self.mu.release()

            rpc_client.unregister(self._opts.standalone.coreAddress, self._opts.service.name)
            self.__disconnect()

            print("shutdown complete...")

    def __disconnect(self):
        print("disconnecting from gmbh-core")

        self.mu.acquire()
        try:
            if self._con:
                print("con exists; can send formal disconnect")
                self._con._connected = False
                if self._con._server:
                    self._con._server.Stop()
                    self._con._connected = False
                    self._con._server = None
                self._con._address = "-"
            else:
                print("con has been disconnected")

            self._registration = None
            self.state = State.Disconnected
        finally:
            self.mu.release()

        if not self._closed:
            time.sleep(5)
            self.__connect()
