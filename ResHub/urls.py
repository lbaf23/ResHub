"""ResHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ResHub.controller import Chatting
from ResHub.controller import Login, Browse, Portal
from ResHub.personal_portal import getPersonalPortal
from ResHub.controller import Collection

urlpatterns = [
    path('admin/', admin.site.urls),

    path('identityCheck', Login.identity_check),
    path('recentUsers', Chatting.get_recent_friends),
    path('getChats', Chatting.get_chats),

    path('BrowseHistory', Browse.BrowseHistory),
    path('CatchPortal', Portal.CatchPortal),

    # Matrix.L
    path('getPersonalPortal', getPersonalPortal.getPersonalPortal),

    #LYC
    path('addCollection',Collection.add_collection),
    path('cancelCollection',Collection.del_collection),
]
