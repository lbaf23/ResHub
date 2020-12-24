from channels.db import database_sync_to_async
from django.http import JsonResponse

from ResModel.models import HubUser, Mail, ChatFriends


def get_recent_friends(request):
    mid = request.GET.get('userId')
    f = ChatFriends.objects.filter(MyId_id=mid).order_by('LastMail__SendTime')
    res = list()

    for i in range(0, f.__len__()):
        j = {
            'chatId': f[i].id,
            'friendId': f[i].FriendId_id,
            'friendName': f[i].FriendId.UserName,
            'newMessage': f[i].Unread,
            'friendHead': f[i].FriendId.UserImage
        }
        res.append(j)
    return JsonResponse({'list': res})


def get_chats(request):
    mid = request.GET.get('myId')
    fid = request.GET.get('friendId')
    print(mid,fid)

    c = Mail.objects.filter(SendEmail=HubUser.objects.get(UserEmail=mid)).\
        filter(ReceiveEmail=HubUser.objects.get(UserEmail=fid))
    d = Mail.objects.filter(ReceiveEmail=HubUser.objects.get(UserEmail=mid)).\
        filter(SendEmail=HubUser.objects.get(UserEmail=fid))

    l = (c | d).order_by('SendTime')
    res = list()
    for i in l:
        j = {
            'id': i.id,
            'sendId': i.SendEmail_id,
            'msg': i.MailContent,
            'sendTime': i.SendTime,
        }
        res.append(j)
    return JsonResponse({'list': res})



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
    message['withDraw']=mes.WithDraw
    return message

# 撤回一条消息
@database_sync_to_async
def with_draw_message(mid):
    # 撤回消息
    pass

