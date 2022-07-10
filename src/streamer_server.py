# from concurrent import futures
import asyncio
import logging
from io import BytesIO
import numpy as np
import pandas as pd
import grpc

from src.protos import streamer_pb2 
from src.protos import streamer_pb2_grpc
from config import CONFIG


LOGGER = logging.getLogger(__name__)


class Streamer(streamer_pb2_grpc.StreamerServicer):

    chunk_size = 64 * 1024 # Recommended chunk size for gRPC is 16-64 KiB (https://github.com/grpc/grpc.github.io/issues/371)

    async def StreamDataFrame(
        self, request: streamer_pb2.StreamerRequest, context: grpc.ServicerContext
    ) -> streamer_pb2.StreamerResponse:
        LOGGER.info("Received request for stream")
        arr = np.random.randn(request.n, request.m)
        df = pd.DataFrame(arr, columns=[str(i) for i in range(request.m)])
        with BytesIO() as buffer:
            df.to_parquet(buffer)
            buffer.seek(0)
            while True:
                content = buffer.read(self.chunk_size)
                if not content:
                    break
                yield streamer_pb2.StreamerResponse(bytes=content)


async def serve():
    # server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()
    streamer_pb2_grpc.add_StreamerServicer_to_server(Streamer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    LOGGER.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
    