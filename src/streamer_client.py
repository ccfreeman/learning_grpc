import sys 
import logging
import asyncio
from io import BytesIO
import pandas as pd

import grpc
from src.protos import streamer_pb2 
from src.protos import streamer_pb2_grpc
from config import CONFIG


LOGGER = logging.getLogger(__name__)


async def _stream_dataframe(stream: grpc.aio._call.UnaryStreamCall) -> pd.DataFrame:
    with BytesIO() as buffer:
        i = 1
        async for bytes_chunk in stream:
            LOGGER.info(i)
            i += 1
            buffer.write(bytes_chunk.bytes)
        buffer.seek(0)
        return pd.read_parquet(buffer)


async def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    if len(sys.argv) == 3:
        n, m = int(sys.argv[1]), int(sys.argv[2])
    else:
        n, m = 2, 3

    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = streamer_pb2_grpc.StreamerStub(channel)
        stream = stub.StreamDataFrame(streamer_pb2.StreamerRequest(n=n, m=m))
        df = await _stream_dataframe(stream)
    LOGGER.info(df)


if __name__ == '__main__':
    asyncio.run(run())
