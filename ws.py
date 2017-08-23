#!/usr/bin/env python

import asyncio
import websockets
import time
import serial

conns = set()

serial_conn = serial.Serial("/dev/ttyUSB0", 115200)

rr = [0.6, 0,   0]
gg = [0,   0.3, 0]
bb = [0,   0,   1]

def color_transform(r, g, b):

    r = max(0, min(1, r / 255))
    g = max(0, min(1, g / 255))
    b = max(0, min(1, b / 255))

    r2 = list(map(lambda x: r * x, rr))
    g2 = list(map(lambda x: g * x, gg))
    b2 = list(map(lambda x: b * x, bb))

    cs = tuple(r2[i] + g2[i] + b2[i] for i in range(3))

    return tuple(int(max(0, min(255, 255 * i))) for i in cs)

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
            serial_conn.write(bytes(color_transform(*c)))
    finally:
        conns.remove(websocket)

start_server = websockets.serve(hello, "0.0.0.0", 1337)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
