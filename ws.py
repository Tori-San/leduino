#!/usr/bin/env python

import asyncio
import websockets
import time
import serial

conns = set()

serial_conn = serial.Serial("/dev/ttyUSB0", 115200)

async def hello(websocket, path):
    print("init")
    conns.add(websocket)
    try:
        while True:
            s = await websocket.recv()
            print(f"< {s}")
            for othersocket in conns:
                if othersocket is websocket:
                    continue
                await othersocket.send(s)
            s = s[1:] # get rid of initial "#"
            c = list(map(lambda x: int(x, 16), [s[i:i+2] for i in range(0, 5, 2)]))
            serial_conn.write(bytes(c))
    finally:
        conns.remove(websocket)

start_server = websockets.serve(hello, "0.0.0.0", 1337)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
