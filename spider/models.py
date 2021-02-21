from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """ 个人信息 """
    id = models.CharField(max_length=20, verbose_name=u"用户id", primary_key=True, help_text= "用户ID")  # 用户ID
    nickname = models.CharField(max_length=30, verbose_name=u"昵称", help_text="昵称") #昵称
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")), default="female",verbose_name=u"性别", help_text="性别") # 性别
    location = models.CharField(max_length=30, verbose_name=u"地区", help_text="地区", blank=True)  # 所在城市
    description = models.CharField(max_length=500, verbose_name=u"简介", blank=True)  # 简介
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)  # 生日
    constellation = models.CharField(max_length=30, verbose_name=u"星座", blank=True)
    # Constellation = models.CharField(max_length=30, verbose_name=u"星座", blank=True)  # 所在城市
    weibo_num = models.IntegerField(default=0, verbose_name=u'微博数')  # 微博数
    following = models.IntegerField(default=0, verbose_name=u'关注数')  # 关注数
    followers = models.IntegerField(default=0, verbose_name=u'粉丝数', blank=True)  # 粉丝数
    # SexOrientation = models.CharField(max_length=30, verbose_name=u"性取向", blank=True)  # 性取向
    # Sentiment = models.CharField(max_length=30, verbose_name=u"感情状况", blank=True)  # 感情状况
    VIPlevel = models.IntegerField(default=0, verbose_name=u"会员等级")  # 会员等级
    verified_reason = models.CharField(max_length=100, verbose_name=u"认证", blank=True)  # 认证
    talent = models.CharField(max_length=30, verbose_name=u"达人", help_text="达人", blank=True) #达人
    education = models.CharField(max_length=30, verbose_name=u"学习经历", blank=True)  # 学习经历
    work = models.CharField(max_length=30, verbose_name=u"工作经历", blank=True)  # 工作经历
    
    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}".format(self.nickname) 
    
class WeiboInfo(models.Model):
    "微博信息"
    """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(20) NOT NULL,
                bid varchar(12) NOT NULL,
                user_id varchar(20),
                nickname varchar(30),
                text varchar(100000),
                article_url varchar(100),
                topics varchar(200),
                at_users varchar(1000),
                location varchar(100),
                created_at DATETIME,
                source varchar(30),
                attitudes_count INT,
                comments_count INT,
                reposts_count INT,
                retweet_id varchar(20),
                keyword varchar(100),
                PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                
    """
    id = models.CharField(max_length=20, verbose_name=u"微博id", primary_key=True, help_text= "微博id")  # 微博id
    # bid = models.CharField(max_length=20, verbose_name=u"微博bid", help_text= "微博bid")  # 微博bid
    user_id = models.CharField(max_length=20, verbose_name=u"用户id", help_text="用户id")
    nickname = models.CharField(max_length=30, verbose_name=u"用户昵称", help_text="用户昵称") #昵称
    text = models.CharField(max_length=3000, verbose_name=u"微博正文", help_text="微博正文")
    # article_url = models.CharField(max_length=300, verbose_name=u"文章url", help_text="微博url")
    # topics = models.CharField(max_length=200, verbose_name=u"话题")
    # at_users = models.CharField(max_length=1000, verbose_name=u"@用户")
    # location = models.CharField(max_length=100, verbose_name=u"地址")
    # created_at = models.DateTimeField(verbose_name=u"发布时间")
    source = models.CharField(max_length=30, verbose_name=u"发布工具")
    attitudes_count = models.IntegerField(default=0, verbose_name=u"点赞数")
    comments_count = models.IntegerField(default=0, verbose_name=u"评论数")
    reposts_count = models.IntegerField(default=0, verbose_name=u"转发数")
    # retweet_id = models.CharField(max_length=30, verbose_name=u"转发id")
    keyword = models.CharField(max_length=100, verbose_name=u"搜索关键词")
    
    class Meta:
        verbose_name = u"微博信息"
        verbose_name_plural = verbose_name


    
    
    
    
    
    