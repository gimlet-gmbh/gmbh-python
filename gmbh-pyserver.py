from concurrent import futures
import logging
import time
import intrigue_pb2
import intrigue_pb2_grpc
import grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intrigue_pb2_grpc.add_CabalServicer_to_server(
        intrigue_pb2_grpc.CabalServicer(), server)
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
