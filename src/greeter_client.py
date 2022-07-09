# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import sys
import logging

import time
import grpc
from src.protos import helloworld_pb2
from src.protos import helloworld_pb2_grpc
from config import CONFIG

LOGGER = logging.getLogger(__name__)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    if len(sys.argv) == 1:
        name = 'you'
    else:
        name = sys.argv[1]

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=name))
        LOGGER.info("Greeter client received: " + response.message)
        time.sleep(1)

        response = stub.SayHelloAgain(helloworld_pb2.Empty())
        LOGGER.info("Greeter client received: " + response.message)
        time.sleep(1)

        response = stub.ForgetMe(helloworld_pb2.Empty())
        LOGGER.info("Greeter client received: " + response.message)
        time.sleep(1)

        response = stub.SayHelloAgain(helloworld_pb2.Empty())
        LOGGER.info("Greeter client received: " + response.message)
        time.sleep(1)
        

if __name__ == '__main__':
    for i in range(10):
        run()
        time.sleep(2)
