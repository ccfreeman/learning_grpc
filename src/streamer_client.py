import sys 
import logging
import asyncio

import numpy as np
import pandas as pd

import grpc
from src.helpers import stream_dataframe_in, stream_dataframe_out
from src.protos import streamer_pb2 
from src.protos import streamer_pb2_grpc
from config import CONFIG


LOGGER = logging.getLogger(__name__)


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
        
        LOGGER.info("STREAMING DATAFRAME INTO CLIENT")
        init_metadata = (('name', 'client'), )
        stream = stub.StreamDataFrameOut(streamer_pb2.Dimensions(n=n, m=m), metadata=init_metadata)
        df_in = await stream_dataframe_in(stream)
        LOGGER.info("Received dataframe")
        trailing_metadata = await stream.trailing_metadata()
        LOGGER.info("Printing metadata")
        for k, v in trailing_metadata:
            LOGGER.info(f"{k}: {v}")

        LOGGER.info("STREAMING DATA OUT OF CLIENT")
        arr = np.random.randn(n, m)
        df_out = pd.DataFrame(arr, columns=[str(i) for i in range(m)])
        await stub.StreamDataFrameIn(stream_dataframe_out(df_out))
        
    LOGGER.info(df_in)


if __name__ == '__main__':
    asyncio.run(run())
