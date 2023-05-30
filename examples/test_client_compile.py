import logging
import grpc

import unified_planning.grpc.generated.unified_planning_pb2 as up_pb2
import unified_planning.grpc.generated.unified_planning_pb2_grpc as up_pb2_grpc

from unified_planning.grpc.proto_writer import ProtobufWriter
from unified_planning.test.examples import get_example_problems
from unified_planning.shortcuts import *


def main():
    if len(sys.argv) > 1:
        grpcport = int(sys.argv[1])
    else:
        grpcport = 8061

    logger = logging.getLogger("Unified Planning Test Client")
    planner_conn = f'0.0.0.0:{grpcport}'
    logger.info("connecting to Unified Planning Service at %s", planner_conn)
    planner_channel = grpc.insecure_channel('0.0.0.0:8061')
    planner_stub = up_pb2_grpc.UnifiedPlanningStub(planner_channel)

    problems = get_example_problems()
    problem = problems["basic_conditional"].problem
    writer = ProtobufWriter()

    pb_problem = writer.convert(problem)

    result = planner_stub.compile(pb_problem)
    print(result)


if __name__ == "__main__":
    main()
