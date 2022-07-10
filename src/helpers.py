from io import BytesIO
import pandas as pd

import grpc
from src.protos import streamer_pb2
from config import CONFIG

def stream_dataframe_out(df: pd.DataFrame):
    with BytesIO() as buffer:
        df.to_parquet(buffer)
        buffer.seek(0)
        while True:
            content = buffer.read(64 * 1024)
            if not content:
                break
            yield streamer_pb2.StreamBlock(bytes=content)


async def stream_dataframe_in(stream: grpc.aio._call.UnaryStreamCall) -> pd.DataFrame:
    with BytesIO() as buffer:
        async for bytes_chunk in stream:
            buffer.write(bytes_chunk.bytes)
        buffer.seek(0)
        return pd.read_parquet(buffer)
