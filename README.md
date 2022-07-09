# Learning gRPC

Play around with gRPC (based on the examples at [grpc.io](https://grpc.io/docs/languages/python/quickstart/)). We try out a few things:
1. Running server/client locally.
2. Running the server through docker-compose.

## 1. Running Locally

### (a) Setting up your virtual Python environment

First, Set up your virtual environment using pipenv. If you have not installed pipenv, use the command
```
python3 -m pip install pipenv
```
then
```
python3 -m pipenv install
```
and after the environment has been created, activate it using
```
python3 -m pipenv shell
```

### (b) Compiling protobuff files

After your environment is set up and activated, you want to generate your gRPC code. To do this, you will leverage the native tools of this library to compile your protocol definitions ([found here](src/protos/helloworld.proto)). This is done using the following command.
```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. src/protos/helloworld.proto
```
This will place two generated Python scripts with protobuff definitions in your `src/protos` path. You should see two new files there: `helloworld_pb2.py` and `helloworld_pb2_grpc.py`. 

### (c) Running your server/client program

Now you are ready to launch your server. In a terminal with your virtual environment shell open, launch the gRPC server.
```
python -m src.greeter_server
```
Now open a new terminal, activate your pipenv shell, and run the greeter client script.
```
python -m src.greeter_client
```

## 2. Running the server through Docker

To run a docker-compose build of our server, build and launch a detached container.
```
docker-compose up -d --build
```

Now, compile the `.proto` files if you have not already for the greeter, and execute the greeter script.
```
python -m src.greeter_client
```
You should see a greeting logged on your terminal out.
```
2022-07-09 13:21:14,036 - __main__ - PID 47998 - TID 4302095744 - INFO - run()- Greeter client received: Hello, cole!
```
If you check the logs on your docker container, you'll see that a gRPC call was received from your greeter client.
