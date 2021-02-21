from django.urls import path

from .views import SpiderWeibo

urlpatterns = [
    path('user/', SpiderWeibo.UserAPI, name='user'),
    path('keyword/', SpiderWeibo.Keyword, name='keyword'),
]