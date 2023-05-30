import os
import sys
import logging
import grpc

from unified_planning.shortcuts import *
from unified_planning.io import PDDLReader
import unified_planning.grpc.generated.unified_planning_pb2 as up_pb2
import unified_planning.grpc.generated.unified_planning_pb2_grpc as up_pb2_grpc

from unified_planning.grpc.proto_reader import ProtobufReader
from unified_planning.grpc.proto_writer import ProtobufWriter
from unified_planning.test.examples import get_example_problems


from unified_planning.test.test_anytime import FILE_PATH as TEST_FILE_PATH

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

    PDDL_DOMAINS_PATH = os.path.join(TEST_FILE_PATH, "pddl")


    reader = PDDLReader()
    domain_filename = os.path.join(PDDL_DOMAINS_PATH, "counters", "domain.pddl")
    problem_filename = os.path.join(PDDL_DOMAINS_PATH, "counters", "problem2.pddl")
    problem = reader.parse_problem(domain_filename, problem_filename)
    problem.add_quality_metric(MinimizeSequentialPlanLength())


    writer = ProtobufWriter()

    pb_problem = writer.convert(problem)

    request = up_pb2.PlanRequest(
        problem=pb_problem,
        resolution_mode=up_pb2.PlanRequest.SATISFIABLE,
    )

    result_stream = planner_stub.planAnytime(request)
    result_counter = 0
    for result in result_stream:
        print(result)
        result_counter += 1
        # TODO: How to make sure server knows we are done?
        if result_counter == 2:
            break
    result_stream.cancel()


if __name__ == "__main__":
    main()
