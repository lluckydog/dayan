import requests
from .models import UserInfo,WeiboInfo
from .spider import Weibo,Search
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.
class SpiderWeibo:
    def UserAPI(request):
        # 用来获取用户信息
        res = {}
        if request.method=="POST":
            id = request.POST.get("weiboId")
            wb = Weibo(id)         
            print("get user id")
            
            try:
                UserInfo.objects.get(id = wb._get_user_id())
                res['ok'] = "数据库已存在该用户，开始返回数据"
                res['data'] = serializers.serialize("json", UserInfo.objects.filter(id=wb._get_user_id()))
                
                return HttpResponse(json.dumps(res))
            
            except UserInfo.DoesNotExist:
                print("数据库不存在该数据，开始爬虫")
                # wb = Weibo(id)
                wb.get_userinfo()
                res['ok']= "数据库不存在该数据的爬虫"
                res['data'] = serializers.serialize("json", UserInfo.objects.filter(id=wb._get_user_id()))
                return HttpResponse(json.dumps(res))
            
    def Keyword(request):
        #获取关键词返回微博
        res = {}
        
        if request.method=="POST":
            keyword = request.POST.get("keyword")
            
            print("get weibo by keyword")
            
            if WeiboInfo.objects.filter(keyword = keyword).exists():
                res['ok'] = "数据库已存在该用户，开始返回数据"
                res['data'] = serializers.serialize("json", WeiboInfo.objects.filter(keyword=keyword))
                
                return HttpResponse(json.dumps(res))
            else:
                print("数据库不存在该数据，开始爬虫")
                sear = Search(keyword)
                sear.fetch_pages()
                res['ok']= "数据库不存在该数据的爬虫"
                res['data'] = serializers.serialize("json", WeiboInfo.objects.filter(keyword=keyword))
                return HttpResponse(json.dumps(res))
            
            
            