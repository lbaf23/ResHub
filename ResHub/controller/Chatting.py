from django.http import HttpResponse, JsonResponse
from ResModel.models import HubUser,Mail,ChatFriends
from django.core import serializers
import json
from channels.db import database_sync_to_async

from dwebsocket.decorators import accept_websocket


def get_recent_friends(request):
    mid = request.GET.get('userId')
    f = ChatFriends.objects.filter(myId=mid).order_by('lastMail__SendTime')
    res = list()

    for i in range(0,f.__len__()):
        j = {
            'chatId': f[i].id,
            'friendId': f[i].friendId_id,
            'friendName': f[i].friendId.UserName,
            'newMessage': f[i].unread,
            'friendHead': f[i].friendId.UserImage
        }
        res.append(j)
    return JsonResponse({'list' : res})


@database_sync_to_async
def submit_message(info): # 发送一条消息
    content = info.get('content')
    mid = info.get('myId')
    fid = info.get('friendId')
    mes = Mail(SendEmail=HubUser.objects.get(UserEmail=mid),ReceiveEmail=HubUser.objects.get(UserEmail=fid),MailContent=content)
    mes.save()
    message = {}
    message['id']=mes.id
    message['messageContent']=content
    message['myId']=mid
    message['sendDate']=str(mes.SendTime)
    message['friendId']=fid
    message['withDraw']=mes.withDraw
    return message

# 撤回一条消息
@database_sync_to_async
def with_draw_message(mid):
    # 撤回消息
    pass

