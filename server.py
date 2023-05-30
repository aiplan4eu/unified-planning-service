from concurrent import futures

import logging
import time
import grpc

import unified_planning
from unified_planning.engines.results import POSITIVE_OUTCOMES
from unified_planning.shortcuts import Problem, OneshotPlanner
from unified_planning.grpc.proto_reader import ProtobufReader
from unified_planning.grpc.proto_writer import ProtobufWriter

import unified_planning.grpc.generated.unified_planning_pb2 as up_pb2
import unified_planning.grpc.generated.unified_planning_pb2_grpc as up_pb2_grpc

from unified_planning.shortcuts import *



class UnifiedPlanningServer(up_pb2_grpc.UnifiedPlanningServicer):
    def __init__(self, port):
        self.port = port

        self.log_format = (
            '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
        self.logger = logging.getLogger("Unified Planning Service")
        logging.basicConfig(level=logging.INFO, format=self.log_format)
        self.reader = ProtobufReader()
        self.writer = ProtobufWriter()

    def planAnytime(self, request, context):
        problem = self.reader.convert(request.problem)
        with AnytimePlanner(problem_kind=problem.kind, anytime_guarantee="INCREASING_QUALITY") as planner:
            for p in planner.get_solutions(problem):
                next_result = self.writer.convert(p)
                yield next_result

    def planOneShot(self, request, context):
        problem = self.reader.convert(request.problem)
        with OneshotPlanner(problem_kind=problem.kind) as planner:
            result = planner.solve(problem)
            if result.status in unified_planning.engines.results.POSITIVE_OUTCOMES:
                self.logger.info(f"{planner.name} found this plan: {result.plan}")
            else:
                self.logger.info("No plan found.")
            answer = self.writer.convert(result)
        return answer

    def validatePlan(self, request, context):
        problem = self.reader.convert(request.problem)
        plan = self.reader.convert(request.plan)
        with PlanValidator(problem_kind=problem.kind, plan_kind=plan.kind) as validator:
            validation_result = validator.validate(problem, plan)
            answer = self.writer.convert(validation_result)
            return answer
    
    def compile(self, request, context):
        problem = self.reader.convert(request)
        with Compiler(
            problem_kind=problem.kind,
            compilation_kinds=[
                # TODO: This should be supplied with request
                CompilationKind.CONDITIONAL_EFFECTS_REMOVING,
                CompilationKind.NEGATIVE_CONDITIONS_REMOVING
                ]) as compiler:
            result = compiler.compile(problem)
            answer = self.writer.convert(result)
            return answer
    
    
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        up_pb2_grpc.add_UnifiedPlanningServicer_to_server(
            self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        self.logger.info("server started on %s" % connection)
        
    def wait_for_termination(self):
        self.server.wait_for_termination()
