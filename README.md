# The Unified Planning Service

Offers unified-planning (version 1.2.0) as a service to the AI on Demand
platform through Protobuf/gRPC.

- [Protobuf Messages and Service Definition](https://github.com/aiplan4eu/unified-planning/blob/master/unified_planning/grpc/unified_planning.proto)

## How to Run

### Locally

In a Python 3.9 environment, run:
    
    pip install -r requirements.txt
    python run.py

### Docker Compose

    docker-compose build
    docker-compose up

### AI4Experiments

## Usage

The following example can be found [./examples/test_client_one_shot.py](here).

### Create a Planning Problem 

Create a problem with the unified-planning API. The following is the basic
example used in the [unified-planning repository
README](https://github.com/aiplan4eu/unified-planning).

```python
    x = Fluent("x")

    a = InstantaneousAction("a")
    a.add_precondition(Not(x))
    a.add_effect(x, True)

    problem = Problem("basic")
    problem.add_fluent(x)
    problem.add_action(a)
    problem.set_initial_value(x, False)
    problem.add_goal(x)
```

### Connect to a Unified Planning Server

Create a channel with host name and port and use the channel to create a stub:

```python
    planner_channel = grpc.insecure_channel('0.0.0.0:8061')
    planner_stub = up_pb2_grpc.UnifiedPlanningStub(planner_channel)
```

### Create a Protobuf Request

Using the ProtoBuf writer supplied by the unfified-planning, we can create a Protobuf
version of our problem and wrap it into a planning request:

```python
    from unified_planning.grpc.proto_writer import ProtobufWriter
    writer = ProtobufWriter()
    
    pb_problem = writer.convert(problem)

    request = up_pb2.PlanRequest(
        problem=pb_problem,
        resolution_mode=up_pb2.PlanRequest.SATISFIABLE,
    )
```

### Call the Unified Planning Service

Finally, we can call the unified-planning service and print the result:

```python
    result = planner_stub.planOneShot(request)
    reader = ProtobufReader()
    result_up = reader.convert(result, problem)
    print(result_up.plan)
```

## Known Issues / TODO

- [X] Add remaining planning modes
- [X] Install additional engines in container
- [ ] Compilation service does not include compilation type information
- [ ] Server-side PlanAnytime stream not stopped when client stops
