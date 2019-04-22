import os

import grpc
import intrigue_pb2 as pb2
import intrigue_pb2_grpc as pb2_g
import datetime 
from threading import Thread, Lock
import gmbh

class CabalServicer(pb2_g.CabalServicer):
    pass

    def RegisterService(self, request, context):
        return pb2.Receipt(Message="operation.invalid")

    def UpdateRegistration(self, serviceUpdate, context):
        print("-> Update Registration; Message=", serviceUpdate.Message)

        req = serviceUpdate.Request
        if req == "core.shutdown":
            print("received shutdown")

            # Either shutdown for real or disconnect and try and reach again if
            # the service wasn't forked from gmbh-core
            if gmbh.g._env == "M":
                t = Thread(target=gmbh.g.__shutdown())
                t.start()
            elif not gmbh.g.closed:
                gmbh.g.mu.acquire()
                try:
                    gmbh.g._registration = None
                finally:
                    gmbh.g.mu.release()
                
                gmbh.g.__disconnect()
                # gmbh.g.__connect()
        
        return pb2.Receipt(Error="unknown.request")


    def Data(self, request, context):
        print()

    def Summary(self, request, context):
        print()

    def WhoIs(self, request, context):
        return pb2.WhoIsResponse(Error="unsupported in client")

    def Alive(self, request, context):
        return pb2.Pong(Time=gmbh.datetime.datetime.now())
