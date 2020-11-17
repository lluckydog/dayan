from django.shortcuts import render

from .models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo, ImgInfo
from .spider import Weibo

from os import path
import json
import re
import requests
import base64

# Create your views here.


class SpiderWeibo:
    @csrf_exempt
    def SpiderAPI(request):
        res = {}
        if request.method == "POST":
            keyword = request.POST.get("keyword")
            
            try:
                print("开始爬虫关键词")
                Target.objects.filter(id=1).update(keyword=keyword)
                resp = list(Target.objects.values('keyword', 'cookie', 'add_time'))
                print(resp)

                cookie = {"Cookie": resp[0]["cookie"]}
                wb = Weibo(keyword,cookie)
                wb.get_weibo_keyword()

                
