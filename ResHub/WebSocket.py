from channels.generic.websocket import AsyncJsonWebsocketConsumer

from ResHub.controller import Chatting


# 自定义websocket处理类
class web_socket_connect(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # 创建连接时调用
        mid = self.scope['url_route']['kwargs']['pk']

        print('连接：',mid,self.channel_name)
        await self.accept()
        # 将新的连接加入到群组
        await self.channel_layer.group_add(mid, self.channel_name)

    async def receive_json(self, message):
        # 收到信息时调用
        print('收到消息：',self.channel_name)

        # 信息单发
        # await self.send_json(content=content)

        if message['state']=='sendMessage': # 发送信息
            msg = await Chatting.submit_message(message)

            await self.channel_layer.group_send(
                message.get('receiveId'),
                {
                    "type": 'chat.message',
                    "state": message['state'],
                    "id": msg["id"],
                    "messageContent": msg['messageContent'],
                    "receiveId": msg['receiveId'],
                    "sendId": msg['sendId'],
                    "sendDate": msg['sendDate'],
                },
            )
            await self.channel_layer.group_send(
                message.get('sendId'),
                {
                    "type": 'chat.message',
                    "state": message['state'],
                    "id": msg["id"],
                    "messageContent": msg['messageContent'],
                    "receiveId": msg['receiveId'],
                    "sendId": msg['sendId'],
                    "sendDate": msg['sendDate'],
                },
            )

        elif message['state']=='withdraw': # 撤回消息
            await Chatting.with_draw_message(message['id'])
            await self.channel_layer.group_send(
                message.get('receiveId'),
                {
                    "type": 'chat.message',
                    "state": message['state'],
                    "id": message['id'],
                    "sendId": message['sendId'],
                    "receiveId": message['receiveId']
                },
            )
        elif message['state']=='addFriend':
            pass

    async def disconnect(self, close_code):
        # 连接关闭时调用
        # 将关闭的连接从群组中移除
        print('断开：',self.channel_name)
        mid = self.scope['url_route']['kwargs']['pk']
        await self.channel_layer.group_discard(mid, self.channel_name)
        await self.close()


    async def chat_message(self, event):
        # 发送给自己
        if event['state']=='sendMessage':
            await self.send_json({
                "state": 'sendMessage',
                "id": event["id"],
                "messageContent": event["messageContent"],
                "sendId": event["sendId"],
                "receiveId": event["receiveId"],
                "sendDate": event['sendDate'],
            })
        elif event['state']=='login':
            await self.send_json({
                "state": 'login',
                "friendId": event["friendId"],
            })
        elif event['state']=='exit':
            await self.send_json({
                "state": 'exit',
                "friendId": event["friendId"],
            })
        elif event['state']=='withdraw':
            await self.send_json({
                "state": 'withdraw',
                "id": event["id"],
                "sendId": event['sendId'],
                "receiveId": event['receiveId']
            })