import os

import grpc
import intrigue_pb2
import intrigue_pb2_grpc
import gmbh

# class requester:

# def __init__(self, coreAddress, options, environment):
#     # pass
#     self.coreAddress = coreAddress
#     self.opts = options
#     self.env = environment

'''
    make a registration request to gmbhCore.

    @return: registration object
    !!! should raise an exception if could not get back a valid registration
'''
def register(coreAddress, name, aliases, peergroups, environment):
    with grpc.insecure_channel(coreAddress) as channel:
        stub = intrigue_pb2_grpc.CabalStub(channel)
        
        
        request = intrigue_pb2.NewServiceRequest(
            Service=intrigue_pb2.NewService(
                Name = name,
                Aliases = aliases,
                IsServer = True,
                IsClient = True,
                PeerGroups = peergroups
            ),
            Address=coreAddress,
            Env=environment
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
        else:
            raise Exception("registration.gmbhUnavailable")

def unregister(coreAddress, name):
    with grpc.insecure_channel(coreAddress) as channel:
        stub = intrigue_pb2_grpc.CabalStub(channel)

        request = intrigue_pb2.ServiceUpdate(
            Request="shutdown.notif",
            Message=name
        )

        stub.UpdateRegistration(request)
        
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
