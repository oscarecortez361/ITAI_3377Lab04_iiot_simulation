import asyncio
import random
from aiocoap import *

async def simulate_sensor_data():
    protocol = await Context.create_client_context()
    await asyncio.sleep(1)
    while True:
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        payload = f'{{"temperature": {temperature:.2f}, "humidity": {humidity:.2f}}}'.encode("utf-8")
        request = Message(code=POST, payload=payload)
        request.set_request_uri("coap://localhost/sensor/data")
        try:
            response = await protocol.request(request).response
            print(f"Result: {response.code}, {response.payload}")
        except Exception as e:
            print("CoAP error:", e)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(simulate_sensor_data())
