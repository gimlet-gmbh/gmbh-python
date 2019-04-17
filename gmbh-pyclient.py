import logging
import grpc
import intrigue_pb2
import intrigue_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
	with grpc.insecure_channel('localhost:50051') as channel:
		stub = intrigue_pb2_grpc.CabalStub(channel)
		print("-------------- Summary --------------")
		print(stub.Summary)

if __name__ == '__main__':
    logging.basicConfig()
    run()
