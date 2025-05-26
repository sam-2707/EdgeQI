# edge_device/communication/grpc_client.py

import grpc
import time

# Placeholder for actual protobuf imports
# from proto import edge_pb2, edge_pb2_grpc

class GrpcClient:
    def __init__(self, server_address='localhost:50051'):
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        # self.stub = edge_pb2_grpc.EdgeServiceStub(self.channel)

    def send_result(self, task_name, result):
        # Placeholder example - actual implementation depends on your proto messages
        print(f"[gRPC] Sending result for task '{task_name}' to {self.server_address}")
        # request = edge_pb2.TaskResult(task_name=task_name, data=str(result))
        # response = self.stub.SendResult(request)
        # print(f"[gRPC] Server response: {response.status}")

    def close(self):
        self.channel.close()
