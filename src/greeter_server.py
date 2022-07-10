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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import asyncio

import grpc
from src.protos import helloworld_pb2 
from src.protos import helloworld_pb2_grpc
from config import CONFIG


LOGGER = logging.getLogger(__name__)


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    async def SayHello(
        self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext
    ) -> helloworld_pb2.HelloReply:
        LOGGER.info("Received request for hello")
        LOGGER.info(dir(request))
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


async def serve():
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    LOGGER.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
    