import grpc
import intrigue_pb2 as pb2
import intrigue_pb2_grpc as pb2_g


class CabalServicer(pb2_g.CabalServicer):
    pass

    def RegisterService(self, request, context):
        return pb2.Receipt(Message="operation.invalid")

    def UpdateRegistration(self, request, context):
        print()

    def Data(self, request, context):
        print()

    def Summary(self, request, context):
        print()

    def WhoIs(self, request, context):
        return pb2.WhoIsResponse(Error="unsupported in client")

    def Alive(self, request, context):
        print()
