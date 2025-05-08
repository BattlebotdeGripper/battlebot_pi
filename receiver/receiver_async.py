import asyncio
import serial_asyncio

class SerialProtocol(asyncio.Protocol):
    def __init__(self, control):
        self.control = control

    def data_received(self, data: bytes):
        """Roept de process_data-methode van de Control-klasse aan."""
        self.control.process_data(data)

    def connection_lost(self, exc):
        print("Seriële verbinding verbroken")

async def run_control(serial_port: str, baudrate: int, control):
    """Start de asynchrone seriële verbinding."""
    loop = asyncio.get_running_loop()
    _, protocol = await serial_asyncio.create_serial_connection(
        loop, lambda: SerialProtocol(control), serial_port, baudrate=baudrate
    )
    # Houd de verbinding open
    await asyncio.Event().wait()