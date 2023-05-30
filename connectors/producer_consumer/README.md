# Unified Planning Producer and Consumer

A simple server that produces plan requests and consumes plan results as defined in the unified planning service.

The service defined in the [./producer_consumer.proto](Protobuf file) has two methods.

- `produce` takes no parameters (`Empty` message type) and returns a `PlanRequest`
  - This method may block until a planning problem is ready 
  - If connected to a user interface, it may wait until the user confirms

- `consume` takes a `PlanResult` as an argument and returns no meaningful result (aka the `Empty` message)
  - This method may execute the solution and block until execution is finished 

## How to: Replace the Empty Message

The empty message in both services can be replaced as needed. 

- Define the desired message in `producer_consumer.proto`
- Re-compile Protobuf
 
        python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
- Adjust code in `server.py` to read/write new message types 

## How to: on-board in the AI4Experiments Platform

To perform on-boarding in AI4Experiments, we need two things:

- A docker repository hosting our node (e.g., docker.io)
- A protobuf file without any import statements
  - In this example, replace the line `import "unified_planning.proto";` with the contents of the imported file

### Pushing the Repository
 
In case of docker hub, `<HOST>` and `<PORT>` can be omitted below.

- Log in 

        docker login <HOST>:<PORT> 

- Build the container
        
        docker build -t producer_consumer

- Tag the build image. In case of docker hub, `<REPOSITORY>`will be your username and the name of a repository created there. 
  `<TAG>` identifies an image in a repository. 

        docker tag producer_consumer <HOST>:<PORT>/<REPOSITORY>:<TAG>

- Push the tagged image to the repository

        docker push producer_consumer <HOST>:<PORT>/<REPOSITORY>:<TAG>

### On-boarding

- Goto https://aiexp.ai4europe.eu/#/home and sign in via ECAS
- On the left side, select ON-BOARDING MODEL
- Fill out required information:
  - Name: Name under which your model will appear in the design studio (or marketplace if published)
  - Docker URI: `<HOST>:<PORT>/<REPOSITORY>:<TAG>`
  - Protobuf file: .proto file without any import statements as explained above
- Click "On-Board Model"

### Assembling an Experiment

- Goto https://aiexp.ai4europe.eu/#/home and sign in via ECAS
- On the left side, select DESIGN STUDIO
- Under "Models" and "Other", you should find your on-boarded component under the chosen name
- Drag and drop a component onto the canvas
- Find the unified-planning-service and do the same
- Now you can connect your component to the unified planning service by connecting the input and output ports of the right types

### Running an Experiment

In the design studio:
- Save your solution (top right)
- Validate your solution (next to Save button)
- Deploy for Execution -> AI-Lab Playground

A new page will open and require log-in via ECAS. On this page, you can run the solution, inspect the logs of each component
and access any web-based GUIs running in your components.
