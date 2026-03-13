import asyncio
import os
from aioquic.asyncio.server import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived

class FileTransferServerProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            if event.data == b"GET":
                with open("testfile.bin", "rb") as f:
                    data = f.read()
                self._quic.send_stream_data(event.stream_id, data, end_stream=True)
                self.transmit()

async def main():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain("cert.pem", "key.pem")
    server = await serve(
        "127.0.0.1",
        4433,
        configuration=config,
        create_protocol=FileTransferServerProtocol
    )
    print("QUIC server running on port 4433...")
    await asyncio.Future()

asyncio.run(main())