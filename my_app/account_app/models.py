#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


from django.utils import timezone

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password,username,identity):
        """
        Creates and saves a User with the given email, name and password.
        """
        '''email是唯一标识，没有会报错'''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)  # 检测密码合理性
        user.set_username(username)
        user.set_identity(identity)
        user.save(using=self._db)  # 保存密码
        return user


    def create_superuser(self, email, username, password,userID):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(email,
                                password=password,
                                username=username,
                                )
        user.is_admin = True  # 比创建用户多的一个字段
        user.save(using=self._db)
        return user

# user-id、名字、邮箱、身份、性别、年龄、创立时间、(手机号、支付宝账号、个人介绍)、地区
class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    userID=models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    IDENTITY_CHOICE = (
        (u'S', u'Student'),
        (u'T', u'Teacher'),
    )
    identity=models.CharField(max_length=2,choices = IDENTITY_CHOICE,null=False)
    GENDER_CHOICE = (
        (u'男', u'Male'),
        (u'女', u'Female'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICE,default='男')
    age = models.IntegerField(default=20)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    cellphone = models.CharField(max_length=12,default="")
    pay_id = models.CharField(max_length=30,default="")
    zone = models.CharField(max_length=20,default="Beijing,China")
    introduction = models.CharField(max_length=100,default="")
    state = models.BooleanField(default=False)

    objects = UserProfileManager()  # 创建用户

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    '''django自带后台权限控制，对哪些表有查看权限等'''

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    '''用户是否有权限看到app'''

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
#发布的课程信息-id、老师id、信息发布的日期、课程状态、课程名、课程时间、课程内容、人数、标签、图片（最多九张）
class course(models.Model):
    ID=models.AutoField(primary_key=True)
    teacherID=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date_created = models.DateTimeField(('date joined'), default=timezone.now)
    courseName=models.CharField(max_length=256)
    endTime=models.DateField(null=True)
    startTime=models.DateField(null=True)
    courseStartTime=models.TimeField(null=True)
    courseEndTime = models.TimeField(null=True)
    # courseName=models.CharField(max_length=256, default='abc')
    peopleNum=models.IntegerField(default=1)
    courseContent=models.TextField()
    state=models.IntegerField(null=False)#2代表删除 0代表未开课 1代表已结束
    tag=models.TextField(default='')
    scope=models.TextField(default='')
    teaching_age=models.TextField(default='')
    city=models.TextField(default='')
    price = models.FloatField(null=False, default=0)
    left = models.IntegerField(default=1) #剩余位数
    taken = models.IntegerField(default=1) #已占位数
    # salary = models.CharField(max_length=256, default='abc')
    # type=models.CharField(max_length=256)
    picture1 = models.ImageField(null=True)
    picture2 = models.ImageField(null=True)
    picture3 = models.ImageField(null=True)
    picture4 = models.ImageField(null=True)
    picture5 = models.ImageField(null=True)
    picture6 = models.ImageField(null=True)
    picture7 = models.ImageField(null=True)
    picture8 = models.ImageField(null=True)
    picture9 = models.ImageField(null=True)

    class Meta:
        db_table = 'course'

#发布的求职信息-id、学生id、信息发布的日期、是否删除、职位、求职内容、标签、图片（最多九张）
class recruitment_info(models.Model):
    ID=models.AutoField(primary_key=True)
    stuID=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date_created = models.DateTimeField(('date created'), default=timezone.now)
    isDelete=models.BooleanField(default=False)
    recruitmentName = models.CharField(max_length=256, default='abc')
    courseContent=models.TextField()
    tag=models.TextField()
    endTime = models.DateField(null=True)
    startTime = models.DateField(null=True)
    courseStartTime = models.TimeField(null=True)
    courseEndTime = models.TimeField(null=True)
    scope = models.TextField(default='')
    price = models.FloatField(null=False, default=0)
    # salary = models.CharField(max_length=256, default='abc')
    teaching_age = models.TextField(default='')
    city = models.TextField(default='')
    peopleNum = models.IntegerField(default=1)
    picture1=models.ImageField(null=True)
    picture1 = models.ImageField(null=True)
    picture2 = models.ImageField(null=True)
    picture3 = models.ImageField(null=True)
    picture4 = models.ImageField(null=True)
    picture5 = models.ImageField(null=True)
    picture6 = models.ImageField(null=True)
    picture7 = models.ImageField(null=True)
    picture8 = models.ImageField(null=True)
    picture9 = models.ImageField(null=True)

    class Meta:
        db_table = 'recruitment_info'

# 订单-id、学生id、课程id、日期、订单状态
class course_order(models.Model):
    ID=models.AutoField(primary_key=True)
    courseID=models.ForeignKey('course',on_delete=models.CASCADE)
    stuID=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date_created = models.DateTimeField(('date created'), default=timezone.now)
    STATE_CHOICE = (
        (u'C', u'Complete'),
        (u'UP', u'Unpaid'),
        (u'N', u'Not finish'),
        (u'R', u'Refund'),
        (u'D', u'Delete'),
        (u'CL', u'Closed'),
    )#支付后状态为N，课程结束或退款后为C，退款中为R，未支付为UP，D为已经删除，CL为交易已关闭
    state=models.CharField(max_length=4,choices=STATE_CHOICE)
    class Meta:
        db_table = 'course_order'

# 以下是动态建表
# name是表名，fields是字段，app_label是你的应用名(如：flow)，module是应用下的模型（如:flow.models）,options是元类选项
def create_model1(name, fields=None, app_label='', module='', options=None):
    class Meta:  # 模型类的Meta类
        pass

    if app_label:  # 必须在元类中设置app_label，相关属性可参考https://www.cnblogs.com/lcchuguo/p/4754485.html
        setattr(Meta, 'app_label', app_label)  # 更新元类的选项

    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)  # 设置模型的属性
        attrs = {'__module__': module, 'Meta': Meta}  # 添加字段属性
    if fields:
        attrs.update(fields)  # 创建模型类对象
    return type(name, (models.Model,), attrs)

def install(custom_model):
    from django.db import connection
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
    editor = BaseDatabaseSchemaEditor(connection)
    try:
        editor.create_model(model=custom_model)  # 会抛出个异常，不知为啥,但表会创建
    except AttributeError as aerror:
        print(aerror)

