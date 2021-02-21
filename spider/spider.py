import os
import json
import logging
import logging.config
import random
import shutil
import sys
from absl import app, flags
from . import config_util, datetime_util
from .models import UserInfo,WeiboInfo
from .util import handle_html
import re
import requests

FLAGS = flags.FLAGS

flags.DEFINE_string('config_path', None, 'The path to config.json.')
flags.DEFINE_string('u', None, 'The user_id we want to input.')
flags.DEFINE_string('user_id_list', None, 'The path to user_id_list.txt.')
flags.DEFINE_string('output_dir', None, 'The dir path to store results.')

logging_path = os.path.split(
    os.path.realpath(__file__))[0] + os.sep + 'logging.conf'
logging.config.fileConfig(logging_path)
logger = logging.getLogger('spider')
search_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"

class Weibo:
    def __init__(self, userid):
        self.config = _get_config()
        self.cookie = self.config['cookie']
        self.userid = userid #对应爬取用户id
        self.url = 'https://weibo.cn/%s' % (userid)
        self.selector = handle_html(self.cookie, self.url)
        
        
    def _get_user_id(self):
        """获取用户id，使用者输入的user_id不一定是正确的，可能是个性域名等，需要获取真正的user_id"""
        user_id = self.userid
        url_list = self.selector.xpath("//div[@class='u']//a")
        for url in url_list:
            if (url.xpath('string(.)')) == u'资料':
                if url.xpath('@href') and url.xpath('@href')[0].endswith(
                        '/info'):
                    link = url.xpath('@href')[0]
                    user_id = link[1:-5]
                    break
        return user_id        

    def get_userinfo(self): 
        try:
            user = UserInfo()
            self.userid = self._get_user_id()
            user.id = self.userid
            self.url = 'https://weibo.cn/%s' % (self.userid)
            self.selector = handle_html(self.cookie, self.url)
            user_info = self.selector.xpath("//div[@class='tip2']/*/text()")
            user.weibo_num = int(user_info[0][3:-1])
            user.following = int(user_info[1][3:-1])
            user.followers = int(user_info[2][3:-1])
                     
            # 获取info页面对应信息
            self.url = 'https://weibo.cn/%s/info' % (self.userid)
            self.selector = handle_html(self.cookie, self.url)
            nickname = self.selector.xpath('//title/text()')[0]
            nickname = nickname[:-3]
            if nickname == u'登录 - 新' or nickname == u'新浪':
                logger.warning(u'cookie错误或已过期')
                sys.exit()
            user.nickname = nickname
            
            basic_info = self.selector.xpath("//div[@class='c'][2]/text()")
            zh_list = [u'会员等级']
            en_list = [
                'VIPlevel'
            ]
            for i in basic_info:
                if i.split('：', 1)[0] in zh_list:
                    setattr(user, en_list[zh_list.index(i.split('：', 1)[0])],
                            int(re.findall(r"\d+\.?\d*",i.split('：', 1)[1].replace('\u3000', ''))[0]))
            print(user)
            
            basic_info = self.selector.xpath("//div[@class='c'][3]/text()")
            zh_list = [u'性别', u'地区', u'生日', u'简介', u'认证', u'达人']
            en_list = [
                'gender', 'location', 'birthday', 'description',
                'verified_reason', 'talent'
            ]
            for i in basic_info:
                if i.split(':', 1)[0] in zh_list:
                    if i.split(':', 1)[0] == u'生日':
                        try:
                            setattr(user, 'birthday',
                                i.split(':', 1)[1].replace('\u3000', ''))
                        except Exception:
                            setattr(user, 'constellation',
                                i.split(':', 1)[1].replace('\u3000', ''))
                    else:
                        setattr(user, en_list[zh_list.index(i.split(':', 1)[0])],
                                i.split(':', 1)[1].replace('\u3000', ''))
            # print(basic_info)
            
            if self.selector.xpath(
                    "//div[@class='tip'][2]/text()")[0] == u'学习经历':
                user.education = self.selector.xpath(
                    "//div[@class='c'][4]/text()")[0][1:].replace(
                        u'\xa0', u' ')
                if self.selector.xpath(
                        "//div[@class='tip'][3]/text()")[0] == u'工作经历':
                    user.work = self.selector.xpath(
                        "//div[@class='c'][5]/text()")[0][1:].replace(
                            u'\xa0', u' ')
            elif self.selector.xpath(
                    "//div[@class='tip'][2]/text()")[0] == u'工作经历':
                user.work = self.selector.xpath(
                    "//div[@class='c'][4]/text()")[0][1:].replace(
                        u'\xa0', u' ')
                    
            try: 
                UserInfo.objects.get(id = self.userid)
                print(UserInfo.objects.get(id = self.userid))
            except UserInfo.DoesNotExist:
                print('except')
                user.save()
            
            
        except Exception as e:
            logger.exception(e)
            
class Search:
        
    def __init__(self, keyword, page=10):
        self.keyword = keyword
        self.page = page
        
    def fetch_data(self, page_id):
        resp = requests.get(search_template.format(self.keyword, self.keyword, page_id))
        card_group = json.loads(resp.text)['data']['cards'][0]['card_group']
        print('url：', resp.url, ' --- 条数:', len(card_group))
        for card in card_group:
            wb = WeiboInfo()
            mblog = card['mblog']
            wb.id = mblog['id']
            wb.text = clean_text(mblog['text'])
            wb.user_id = str(mblog['user'] ['id'])
            wb.nickname = mblog['user']['screen_name']
            wb.attitudes_count = int(mblog['reposts_count'])
            wb.comments_count = int(mblog['comments_count'])
            wb.reposts_count = int(mblog['reposts_count'])
            wb.source = clean_text(mblog['source'])
            # wb.created_at = extract_time(mblog['created_at'])
            wb.keyword = self.keyword
            
            try:
                WeiboInfo.objects.get(id=wb.id)
                print("update")
                wb.save()
            except WeiboInfo.DoesNotExist:
                print('except')
                wb.save()
        #     blog = {'mid': mblog['id'],  # 微博id
        #             'text': clean_text(mblog['text']),  # 文本
        #             'userid': str(mblog['user']['id']),  # 用户id
        #             'username': mblog['user']['screen_name'],  # 用户名
        #             'reposts_count': mblog['reposts_count'],  # 转发
        #             'comments_count': mblog['comments_count'],  # 评论
        #             'attitudes_count': mblog['attitudes_count']  # 点赞
        #             }
        
        
    def fetch_pages(self): #获取多页信息
        try:
            for page_id in range(1, self.page+1):
                self.fetch_data(page_id)
                
                
                
        except Exception as e:
            logger.exception(e)
            
        
    
        
            
            
def clean_text(text):
    """清除文本中的标签等信息"""
    # clear_text=re.sub('["\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"]', '', text)
    dr = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    dd = dr.sub('',text)
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    return dd.strip()          
        
        
        
def _get_config():
    """获取config.json数据"""
    src = os.path.split(
        os.path.realpath(__file__))[0] + os.sep + 'config_sample.json'
    config_path = os.getcwd() + os.sep + 'config.json'
    # if FLAGS.config_path:
    #     config_path = FLAGS.config_path
    # elif not os.path.isfile(config_path):
    #     shutil.copy(src, config_path)
    #     logger.info(u'请先配置当前目录(%s)下的config.json文件，'
    #                 u'如果想了解config.json参数的具体意义及配置方法，请访问\n'
    #                 u'https://github.com/dataabc/weiboSpider#2程序设置' %
    #                 os.getcwd())
    #     sys.exit()
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            # print(config)
            return config
    except ValueError:
        logger.error(u'config.json 格式不正确，请访问 '
                     u'https://github.com/dataabc/weiboSpider#2程序设置')
        sys.exit()