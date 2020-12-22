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

from rest_framework import routers
from ResModel.views import PaperSearchViewSet

from ResHub.controller import Chatting
from ResHub.controller import Login, Browse, Portal, Concern
from ResHub.personal_portal import getPersonalPortal
from ResHub.institutions import getResearchInstitute
from ResHub.history import getSearchRecord, deleteSearchRecord
from ResHub.user import newPassword, changeHead
from ResHub.controller import Collection
from ResHub.controller import Search
from ResHub.controller import Administrator
from ResHub.controller import searchHistory

urlpatterns = [
    path('admin/', admin.site.urls),

    path('identityCheck', Login.identity_check),
    path('bandWidthTest', Login.bandwidth_test),
    path('recentUsers', Chatting.get_recent_friends),
    path('getChats', Chatting.get_chats),

    # WXJ
    path('BrowseHistory', Browse.browse_history),
    path('CatchPortal', Portal.catch_portal),
    path('getMyConcern', Concern.get_my_concern),
    path('cancelConcern', Concern.cancel_concern),
    path('newPortal', Portal.new_portal),
    path('appealPortal', Portal.appeal_portal),
    path('passwordLost', Login.passwordLost),
    path('getList', Administrator.getList),
    path('changeHead', changeHead.changeHead),
    path('addConcern', Concern.add_concern),


    # LKY
    #path('temp', temp.temp),
    path('getPersonalPortal', getPersonalPortal.getPersonalPortal),
    path('getResearchInstitute', getResearchInstitute.getResearchInstitute),
    path('getSearchRecord', getSearchRecord.getSearchRecord),
    path('deleteSearchRecord', deleteSearchRecord.deleteSearchRecord),
    path('newPassword', newPassword.newPassword),


    # LYC
    path('addCollection', Collection.add_collection),
    path('cancelCollection', Collection.del_collection),
    path('getMyCollection', Collection.get_collection),
    path('addBrowseHistory', Browse.add_browse_history),
    path('addViewSum', Browse.add_view_num),
    path('registerInformation', Login.register),
    path('verificationCode', Login.verification),
    path('pass1', Administrator.pass_review),
    path('reject1', Administrator.reject_review),
    path('pass2', Administrator.pass_appeal),
    path('reject2', Administrator.reject_appeal),
    path('addSearchRecord', searchHistory.add_search_history),


    path('searchWords', Search.search_words),
    path('openPaper', Search.show_paper_info),
    path('searchAuthors', Search.search_authors),
    path('fastSearch', Search.fast_search)
]

router = routers.DefaultRouter()
router.register('paper/search', PaperSearchViewSet, basename='paper_search')
urlpatterns += router.urls
