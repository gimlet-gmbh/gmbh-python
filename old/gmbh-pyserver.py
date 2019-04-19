from concurrent import futures
import logging
import time
import intrigue_pb2
import intrigue_pb2_grpc
import grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class CabalServicer(intrigue_pb2_grpc.CabalServicer):
    pass

    def RegisterService(self, request, context):
        
        # Create the service summary for the receipt
        serviceSummary = intrigue_pb2.ServiceSummary(
            Address = "Summary Address",
            ID = "Service Summary ID",
            Fingerprint = "Service Summary Fingerprint"
        )

        # Generate Receipt
        # - ServiceSummary serviceInfo
        # - string Message
        # - string Followup
        # - string Error
        response = intrigue_pb2.Receipt(
            serviceInfo = serviceSummary,
            Message = "Hi Client",
            Followup = "Fuck this",
            Error = "No Error"
        )

        return response
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intrigue_pb2_grpc.add_CabalServicer_to_server(
        CabalServicer(), server)
    print("Server Now Listening")
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()
