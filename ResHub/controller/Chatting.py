from django.http import HttpResponse, JsonResponse
from ResModel.models import HubUser,Mail,ChatFriends
from django.core import serializers
import json
from channels.db import database_sync_to_async

from dwebsocket.decorators import accept_websocket


@database_sync_to_async
def submit_message(info): # 发送一条消息

    # mes = Message(sendId=ChatUser.objects.get(userId=sid),receiveId=ChatUser.objects.get(userId=rid),messageContent=content)
    # mes.save()
    # 保存消息
    return info

# 撤回一条消息
@database_sync_to_async
def with_draw_message(mid):
    # 撤回消息
    pass

