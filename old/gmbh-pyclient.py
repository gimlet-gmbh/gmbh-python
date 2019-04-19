import logging
import grpc
import intrigue_pb2
import intrigue_pb2_grpc


def run():
	with grpc.insecure_channel('localhost:50051') as channel:
		stub = intrigue_pb2_grpc.CabalStub(channel)

		# Create a new service for the request
		service = intrigue_pb2.NewService(
			Name = "Service 1",
			Aliases = "None",
			IsServer = False,
			IsClient = True,
			PeerGroups = "None"
		)

		request = intrigue_pb2.NewServiceRequest(
			Service = service,
			Address = "NewService Addy",
			Env = "Env"
			)

		receipt = stub.RegisterService(request)
		print(receipt)

if __name__ == '__main__':
    logging.basicConfig()
    run()
