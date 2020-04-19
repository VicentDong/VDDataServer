import asyncio
import websockets
import json
from mysqlDataAccess import MysqlDataAccess
import logging
from datetime import datetime
import time

interval = 60

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
logging.info('websocket服务启动')

# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            logging.info('认证通过')
            return True
        else:
            content = {"code": 0, "msg": "authentication failed"}
            logging.info('认证失败')
            await websocket.send(json.dumps(content))

# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def send(websocket):
    await send_data(websocket)
    while True:
        await send_data(websocket)
        time.sleep(interval)

# 服务器端主逻辑
async def main_logic(websocket, path):
    await check_permit(websocket)
    # await recv_msg(websocket)
    await send(websocket)

async def send_data(websocket):
    access = MysqlDataAccess()
    data = access.getData()
    logging.info('数据获取完成')
    await websocket.send(json.dumps(data))
    logging.info('信息发送中')


start_server = websockets.serve(main_logic, 'localhost', 9998)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()






