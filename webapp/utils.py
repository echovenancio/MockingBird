import grpc
from . import sandbox_pb2
from . import sandbox_pb2_grpc


def run_user_code(test_path, user_code) -> sandbox_pb2.SolutionReply:
    with grpc.insecure_channel("[::1]:50051") as channel:
        service = sandbox_pb2_grpc.CodeRunnerStub(channel)
        response = service.RunUserSolution(
            sandbox_pb2.SolutionRequest(testPath=test_path, solution=user_code)
        )
        return response
