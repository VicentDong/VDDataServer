import asyncio
import websockets
import json
from mysqlDataAccess import MysqlDataAccess
import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
logging.debug('websocket服务启动')

# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            logging.debug('认证通过')
            return True
        else:
            content = {"code": 0, "msg": "authentication failed"}
            logging.debug('认证失败')
            await websocket.send(json.dumps(content))

# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def send(websocket):
    while True:
        access = MysqlDataAccess()
        data = access.getData()
        logging.debug('信息发送中')
        await websocket.send(json.dumps(data))

# 服务器端主逻辑
async def main_logic(websocket, path):
    await check_permit(websocket)
    # await recv_msg(websocket)
    await send(websocket)

start_server = websockets.serve(main_logic, 'localhost', 9998)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()






