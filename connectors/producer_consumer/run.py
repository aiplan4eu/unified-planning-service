import sys
import logging

from server import UnifiedPlanningProducerConsumer

def main():
    if len(sys.argv) > 1:
        grpcport = int(sys.argv[1])
    else:
        grpcport = 8061
    server = UnifiedPlanningProducerConsumer(grpcport)

    server.logger.info("starting unified planning server on port %s" % grpcport)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()

