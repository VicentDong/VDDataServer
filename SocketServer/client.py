import asyncio
import websockets
import json


# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    cred_text = "admin:123456"
    while True:
        await websocket.send(cred_text)
        response = await websocket.recv()
        result = json.loads(response)
        if result["code"] == 1:
            print(result["code"], result["msg"])
            return True
        else:
            print(result["code"], result["msg"])


# 向服务器端发送认证后的消息
async def send_msg(websocket, data):
    await websocket.send(data)
    response = await websocket.recv()
    print(response)


# 客户端主逻辑
async def send():
    async with websockets.connect('ws://localhost:9998') as websocket:
        await auth_system(websocket)
        data = {'a': 1, 'b': 2}
        await send_msg(websocket, json.dumps(data))

asyncio.get_event_loop().run_until_complete(send())
