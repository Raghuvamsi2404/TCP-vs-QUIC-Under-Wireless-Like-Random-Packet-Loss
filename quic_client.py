import asyncio
import time
import json
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, StreamReset

class FileTransferClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.received_data = b""
        self.done = asyncio.Event()
        self.start_time = None

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            self.received_data += event.data
            if event.end_stream:
                self.done.set()

async def main():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False

    config.congestion_control_algorithm = "reno"

    start = time.time()
    async with connect("127.0.0.1", 4433, configuration=config,
                       create_protocol=FileTransferClientProtocol) as client:
        stream_id = client._quic.get_next_available_stream_id()
        client._quic.send_stream_data(stream_id, b"GET", end_stream=False)
        client.transmit()
        await client.done.wait()
        fct = (time.time() - start) * 1000
        size_mb = len(client.received_data) / (1024 * 1024)
        goodput = (size_mb * 8) / (fct / 1000)
        result = {
            "fct_ms": round(fct, 2),
            "size_mb": round(size_mb, 3),
            "goodput_mbps": round(goodput, 2)
        }
        print(json.dumps(result))

asyncio.run(main())