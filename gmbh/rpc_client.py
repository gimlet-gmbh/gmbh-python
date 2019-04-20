import os

import grpc
import intrigue_pb2
import intrigue_pb2_grpc
import gmbh

class requester:

    def __init__(self, coreAddress, options, environment):
        self.coreAddress = coreAddress
        self.opts = options
        self.env = environment

    '''
        make a registration request to gmbhCore.

        @return: registration object
        !!! should raise an exception if could not get back a valid registration
    '''
    def register(self):
        with grpc.insecure_channel(self.coreAddress) as channel:
            stub = intrigue_pb2_grpc.CabalStub(channel)
            print("Core address", self.coreAddress)
            
            request = intrigue_pb2.NewServiceRequest(
                Service=intrigue_pb2.NewService(
                    Name = self.opts.service.name,
                    Aliases = self.opts.service.aliases,
                    IsServer = True,
                    IsClient = True,
                    PeerGroups = self.opts.service.peerGroups
                ),
                Address=self.coreAddress,
                Env=self.env
            )

            receipt = stub.RegisterService(request)

            if receipt.Message == "acknowledged":
                reg = receipt.serviceInfo
                r = gmbh.registration(
                    id=reg.ID,
                    address=reg.Address,
                    fingerprint=reg.Fingerprint
                )
                return r
                

    '''
        @param target string
        @param method string
        @param data payload object

        @return responder object
        !!! should raise an exception if error
        
    '''
    def data(self, target, method, data):
        print("")


    '''
        @param target string

        !!! should raise an exception if error
    '''
    def whoIs(self, target):
        print("")
