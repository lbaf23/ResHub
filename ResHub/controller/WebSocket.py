from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ResHub.controller import Chatting

# 自定义websocket处理类
class web_socket_connect(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 创建连接时调用
        mid = self.scope['url_route']['kwargs']['pk']
        mid = mid[:-7]
        print(mid)
        print('连接：', mid, self.channel_name)
        await self.accept()
        # 将新的连接加入到群组

        await self.channel_layer.group_add(mid, self.channel_name)

    async def receive_json(self, message):
        # 收到信息时调用
        print('收到消息：', self.channel_name)

        # 信息单发
        # await self.send_json(content=content)

        if message['state'] == 'sendMessage': # 发送信息
            print(message)
            msg = await Chatting.submit_message(message)
            fid = message.get('friendId')[:-7]
            mid = message.get('myId')[:-7]
            await self.channel_layer.group_send(
                fid,
                {
                    "type": 'chat.message',
                    "state": 'sendMessage',
                    "id": msg["id"],
                    "messageContent": msg['messageContent'],
                    "friendId": msg['friendId'],
                    "myId": msg['myId'],
                    "sendDate": msg['sendDate'],
                },
            )
            await self.channel_layer.group_send(
                mid,
                {
                    "type": 'chat.message',
                    "state": 'sendMessage',
                    "id": msg["id"],
                    "messageContent": msg['messageContent'],
                    "friendId": msg['friendId'],
                    "myId": msg['myId'],
                    "sendDate": msg['sendDate'],
                },
            )


    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        print('断开：',self.channel_name)
        mid = self.scope['url_route']['kwargs']['pk']
        mid = mid[:-7]
        await self.channel_layer.group_discard(mid, self.channel_name)
        await self.close()


    async def chat_message(self, event):
        # 发送给自己
        if event['state'] == 'sendMessage':
            print("发送消息")
            await self.send_json({
                "state": 'sendMessage',
                "id": event["id"],
                "msg": event["messageContent"],
                "sendId": event["myId"],
                "receiveId": event["friendId"],
                "sendTime": event['sendDate'],
            })
