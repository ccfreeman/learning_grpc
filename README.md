# learning_grpc

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