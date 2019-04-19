import intrigue_pb2
import intrigue_pb2_grpc
import grpc


class CabalServicer(intrigue_pb2_grpc.CabalServicer):
    pass

    def RegisterService(self, request, context):
        print()

    def UpdateRegistration(self, request, context):
        print()

    def Data(self, request, context):
        print()

    def Summary(self, request, context):
        print()

    def WhoIs(self, request, context):
        print()

    def Alive(self, request, context):
        print()