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

import producer_consumer_pb2 as pc_pb2
import producer_consumer_pb2_grpc as pc_pb2_grpc

from unified_planning.shortcuts import *



class UnifiedPlanningProducerConsumer(pc_pb2_grpc.UnifiedPlanningProducerConsumer):
    def __init__(self, port):
        self.port = port

        self.log_format = (
            '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')
        self.logger = logging.getLogger("Unified Planning Service")
        logging.basicConfig(level=logging.INFO, format=self.log_format)
        self.reader = ProtobufReader()
        self.writer = ProtobufWriter()

    def produce(self, request, context):
        # Produce a planning problem
        # - Arguments are ignored (type is Empty message)
        # - May block until a problem is ready (e.g., check if a button has been pressed in a UI)
        # - Below we just wait for 5 seconds to avoid looping to fast if this is part of an orchestrated solution
        time.sleep(5)
        x = Fluent("x")
        a = InstantaneousAction("a")
        a.add_precondition(Not(x))
        a.add_effect(x, True)
        problem = Problem("basic")
        problem.add_fluent(x)
        problem.add_action(a)
        problem.set_initial_value(x, False)
        problem.add_goal(x)
        writer = ProtobufWriter()
        pb_problem = writer.convert(problem)

        request = up_pb2.PlanRequest(
            problem=pb_problem,
            resolution_mode=up_pb2.PlanRequest.SATISFIABLE,
        )
        return request

    def consume(self, request, context):
        # Consume a PlanGenerationResult
        # - May block until execution is finished
        # - Below we just print the result and return the empty message
        print(request)
        return pc_pb2.Empty()
    
    def start(self):
        connection = '0.0.0.0:%d' % (self.port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pc_pb2_grpc.add_UnifiedPlanningProducerConsumerServicer_to_server(
            self, self.server)
        self.server.add_insecure_port(connection)
        self.server.start()
        self.logger.info("server started on %s" % connection)
        
    def wait_for_termination(self):
        self.server.wait_for_termination()
