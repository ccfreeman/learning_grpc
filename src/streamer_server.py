from concurrent import futures
import logging

import numpy as np
import pandas as pd
import grpc
from io import BytesIO

from src.protos import streamer_pb2 
from src.protos import streamer_pb2_grpc
from config import CONFIG


LOGGER = logging.getLogger(__name__)


class Streamer(streamer_pb2_grpc.StreamerServicer):

    def StreamDataFrame(
        self, request: streamer_pb2.StreamerRequest, context: grpc.ServicerContext
    ) -> streamer_pb2.StreamerResponse:
        LOGGER.info("Received request for stream")
        arr = np.random.randn(request.n, request.m)
        df = pd.DataFrame(arr, columns=[str(i) for i in range(request.m)])
        with BytesIO() as buffer:
            df.to_parquet(buffer)
            buffer.seek(0)
            while True:
                content = buffer.read(1024)
                if not content:
                    break
                yield streamer_pb2.StreamerResponse(bytes=content)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streamer_pb2_grpc.add_StreamerServicer_to_server(Streamer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
    