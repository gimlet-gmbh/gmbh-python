import os

import options as opts
import rpc_server as serv
import socket
import data
import datetime
import signal
import time
from concurrent import futures
from threading import Thread, Lock
import enum

# Import grpc for the client stubs
import grpc
from grpc_reflection.v1alpha import reflection
import intrigue_pb2
import intrigue_pb2_grpc

State = enum.Enum('State', 'Connected Disconnected')
g = None

def newClient(opts=opts.new()):
    print("newclient")
    # if g != None:
    #     return g

    g = client(opts)
    
    if g._opts.service.name == "CoreData":
        raise Exception()
    return g

class registration:
    def __init__(self, id, address, fingerprint):
        self.id = id
        self.mode = ""
        self.address = address
        self.fingerprint = fingerprint

class connection:
    def __init__(self, address, server, connected):
        self._server = server
        self._address = address
        self._connected = connected

class client:

    def __init__(self, opts):
            
        self._registration = None
        self._con = None
        self._msgCounter = 0
        self.state = None

        self._registeredFunctions = {}
        self._whoIs = {}

        self._myAddress = ""
        self._parentID = ""
        self._env = os.environ.get('ENV')

        # If the connection is meant to be closed or not
        self._closed = False

        self._opts = opts
        self.mu = Lock()

        if self._opts.service.name == "":
            raise Exception("service name cannot be empty")
        if self._opts.service.name == "CoreData":
            raise Exception("\"CoreData\" is a reserved service name")

        if self._env == "C":
            self._myAddress = os.environ.get('ADDR')
            print("using core address from environment=",self._myAddress)
        else:
            print("core address=", self._opts.standalone.coreAddress)

        print("                    _                 ")
        print("  _  ._ _  |_  |_| /  | o  _  ._ _|_  ")
        print(" (_| | | | |_) | | \\_ | | (/_ | | |_ ")
        print("  _|                                  ")
        print("service started from", 
               os.path.dirname(os.path.realpath(__file__)))
        print("PeerGroup=",self._opts.service.peerGroups)

    '''User called methods'''
    def route(self, route, handler):
        self._registeredFunctions[route] = handler

    def makeRequest(self, target, method, payload):
        # response = self.__data()
        print("Hi from makeRequest")

    '''class called methods'''  
    def start(self):
        if self._opts.runtime.blocking:
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
                reg = self.__register(
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

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        intrigue_pb2_grpc.add_CabalServicer_to_server(serv.CabalServicer(), server)
        self.mu.acquire()
        try:
            self._registration = reg
            self._con = connection(reg.address, server, False)
            self.state = State.Connected
        finally:
            self.mu.release()

        # Connect to server
        if self._con._address == "":
            raise Exception("connection.connect.noAddress")
        
        reflection.enable_server_reflection(self._opts.service.name,
                                            self._con._server)
        server.add_insecure_port(self._con._address)
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except:
            server.stop(0)

        print("connected; coreAddress=(" + reg.address + ")")

# client needs to listen for shutdown notification in the server
    def __shutdown(self, signum, frame):
            print("shutdown procedures started...")

            self.mu.acquire()
            try:
                self._closed = True
                self.registration = None
            finally:
                self.mu.release()

            self.__unregister(self._opts.standalone.coreAddress,
                              self._opts.service.name)
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
    

    def __resolveAddress(self, target):
        addr = self._whoIs[target]

        print("getting address for ", target)

        self.__whoIs(self._opts.standalone.coreAddress, target)

    '''
        make a registration request to gmbhCore.

        @return: registration object
        !!! should raise an exception if could not get back a 
            valid registration
    '''
    def __register(self, coreAddress, name, aliases, peergroups, environment) :
        with grpc.insecure_channel(coreAddress) as channel:
            stub = intrigue_pb2_grpc.CabalStub(channel)

            request = intrigue_pb2.NewServiceRequest(
                Service=intrigue_pb2.NewService(
                    Name=name,
                    Aliases=aliases,
                    IsServer=True,
                    IsClient=True,
                    PeerGroups=peergroups
                ),
                Address=coreAddress,
                Env=environment
            )

            receipt = stub.RegisterService(request)

            if receipt.Message == "acknowledged":
                reg = receipt.serviceInfo
                r = registration(
                    id=reg.ID,
                    address=reg.Address,
                    fingerprint=reg.Fingerprint
                )
                return r
            else:
                raise Exception("registration.gmbhUnavailable")

    def __unregister(self, coreAddress, name):
        with grpc.insecure_channel(coreAddress) as channel:
            stub = intrigue_pb2_grpc.CabalStub(channel)

            request = intrigue_pb2.ServiceUpdate(
                Request="shutdown.notif",
                Message=name
            )
            print("Helllllllllllllo")

            stub.UpdateRegistration(request)

    '''
        @param target string
        @param method string
        @param data payload object

        @return responder object
        !!! should raise an exception if error
        
    # '''
    # def __data(self, target, method, data, name, env):
    #     with grpc.insecure_channel(coreAddress) as channel:
    #         stub = intrigue_pb2_grpc.CabalStub(channel)

    #         print("hit from data")

    #         # t = datetime.datetime.now()
    #         # request = intrigue_pb2.DataRequest(
    #         #     Request=intrigue_pb2.Request(
    #         #         Tport=intrigue_pb2.Transport(
    #         #             Target=target,
    #         #             Method=method,
    #         #             Send=name
    #         #         ),
    #         #         Pload=data.payload.proto()
    #         #     )
    #         # )

    #         # if env != "C" or os.getenv("LOGGING") == "1":
    #         #     print("<=" + str(msgCounter) + "= target" + target + ", method: " + method)

    #         # response = stub.Data(request)
    #         # t = datetime.datetime.now() - t
    #         # if env != "C" or os.getenv("LOGGING") == "1":
    #         #     print(" =" + str(msgCounter) + "=> " + "time=" + str(t))

    #         # if response.Responder:
    #         #     return data.responder()

    #         # return data.responder.fromProto(response.responder)


    '''
        @param target string

        !!! should raise an exception if error
    '''
    def __whoIs(self, coreAddress, target):
        with grpc.insecure_channel(coreAddress) as channel:
            stub = intrigue_pb2_grpc.CabalStub(channel)
            print("hi from whoIs")
