from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import UserProfile,course_order
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail, Publish
from .models import UserProfile
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail,Publish
from .models import UserProfile,course_order
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import course, recruitment_info
from django.http import JsonResponse
from datetime import datetime
from django.db import connection
from django.contrib import messages
import os
from .models import course
from django.http import JsonResponse
from datetime import datetime, date, time
from django.db import connection
from django.utils import timezone
from .createTable import CreateNewMessage
import json
from .models import install, create_model1
from django.db import models

global aa, bb, cc
aa = 1
global id
id = 'S'
global fileRoute

'''
------------------------
-----BY AUTHOR ZHU------
------------------------
'''
@csrf_exempt
def check_teacher_info(request):
    if request.is_ajax():
        user = get_user_model()
        user = user.objects.get(email=request.session['user_email'])
        user.state = True
        user.save()
        request.session['state'] = True
        print('lalala')
        # return render(request, 'page-blog-list.html')
        return JsonResponse({'status': 200, 'message': 'add event success'})
    # return render(request, 'page-check.html')
    return render(request, 'page-check.html')
@csrf_exempt
def profile_change_password(request):
    if request.session.get('is_login', None):
        request_dict = {}
        if request.method == 'POST':
            form = ModifyPassword(request.POST)
            if form.is_valid():
                change_origin_password = form.cleaned_data['change_origin_password']
                change_new_password = form.cleaned_data['change_new_password']
                user = get_user_model()
                user = user.objects.get(email=request.session['user_email'])
                print(user)
                if user.password == change_origin_password:
                    user.password = change_new_password
                    user.save()
                    request_dict['modify_success'] = True
                    return render(request, 'page-employer-change-password.html', request_dict)
                else:
                    request_dict['oldpassword_is_wrong'] = True
                    return render(request, 'page-employer-change-password.html', request_dict)
            else:
                print("not valid")
                return render(request, 'page-employer-change-password.html')
        else:
            return render(request, 'page-employer-change-password.html')
    else:
        return render(request, 'index.html')

@csrf_exempt
def profile_person_info(request):
    if request.session.get('is_login', None):
        if request.is_ajax():
            username = request.POST.get("username")
            email = request.POST.get("email")
            cellphone = request.POST.get("cellphone")
            age = request.POST.get("age")
            pay_id = request.POST.get("pay_id")
            gender = request.POST.get("gender")
            introduction = request.POST.get("introduction")
            print(username+email+cellphone+age+pay_id+gender+introduction)
            user = get_user_model()
            user = user.objects.get(email=request.session['user_email'])
            user.username = username
            user.gender = gender
            user.age = age
            user.cellphone = cellphone
            user.pay_id = pay_id
            user.gender = gender
            user.introduction = introduction
            user.save()
            request.session['username'] = username
            request.session['gender'] = gender
            request.session['age'] = age
            request.session['cell_phone'] = cellphone
            request.session['pay_id'] = pay_id
            request.session['introduction'] = introduction
            return JsonResponse({'status': 200, 'message': 'add event success'})
        else:
            return render(request, 'page-employer-profile.html')
    else:
        return render(request, 'index.html')


@csrf_exempt
def protect1(request):
    if request.session.get('is_login', None):
        return render(request,'page-blog-list.html')
    else:
       return  render(request, 'index.html')

@csrf_exempt
def me(request):
    if request.session.get('is_login', None):
        return render(request, 'me.html')
    else:
        return render(request, 'index.html')

@csrf_exempt
def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user=get_user_model()
                if user.objects.filter(email=email):
                    person = user.objects.get(email=email)
                    print(person.password)
                    print(password)
                    if person.password == password:
                        if request.session.get('is_login', None):
                            print("already logged in")
                            return render(request, 'page-blog-list.html', {'mes1': "You have already been login."})
                        request.session['user_email'] = email
                        request.session['is_login'] = True
                        request.session['username'] =person.username
                        request.session['userID'] = person.userID
                        obj=person.date_joined
                        request.session['created_at'] =obj.strftime('%Y-%m-%d %H:%M:%S')

                        request.session['identity'] = person.identity
                        request.session['gender'] = person.gender
                        request.session['age'] = person.age
                        request.session['cell_phone'] = person.cellphone
                        request.session['pay_id'] = person.pay_id
                        request.session['zone'] = person.zone
                        request.session['introduction'] = person.introduction
                        request.session['state'] = person.state
                        if person.identity == 'T':
                            if person.state == False:
                                return redirect('/check')
                        print("now to homepage")
                        return redirect('/page-blog-list')
                        #return render(request,'page-blog-list.html')
                    else:
                        return render(request, 'index.html', {'mes1': "password is invalid."})
                else:
                    return render(request, 'index.html', {'mes1': "email not found."})
        else:
               return render(request, 'index.html',{'error':form.errors,'form1': form})

    return render(request, 'page-blog-list.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            username = form.cleaned_data['username']
            identity=request.POST['identity']

            user_profile = UserProfile(email=email,password=password,username=username,identity=identity)
            user_profile.save()
            return render(request, 'index.html')
        else:
            return render(request, 'index.html',{'error':form.errors,'form': form})
    return render(request, 'index.html')


@csrf_exempt
def login_validate(request):
    return render(request, 'index.html')

'''
------------------------
-----BY AUTHOR FENG------
------------------------
'''
@csrf_exempt
def homepage(request):
    global aa, bb, cc
    global id
    global fileRoute
    user = get_user_model()
    user = user.objects.get(email=request.session['user_email'])
    print("now I can see the user----")
    print(user)
    iden = user.identity
    print(request.method)
    if iden == 'S':
        bb = '招募'
        cc = '欢迎您，亲爱的学生 ' + user.username + '!'
        id = 'S'
    else:
        bb = '课程'
        cc = '欢迎您，亲爱的老师 ' + user.username + '!'
        id = 'T'
    if request.method == 'GET':
        print("now in homepage get")
        course_info = course.objects.filter(state=0).order_by('-date_created')
        # recruitment = recruitment_info.objects.all().order_by('-date_created')
        print("print course info")
        print(course)
        return render(request, 'page-blog-list.html',
                      {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
    if request.method == 'POST':
        print("now in homepage post")
        if "search_box" in request.POST:
            if aa == 1:
                content=request.POST['search_box']
                print("now search, the searching content is(course):")
                print(content)
                course_search = course.objects.filter(tag=content, state=0)
                return render(request,'page-blog-list.html',{'course_infos':course_search, 'message': bb, 'teacher_student': cc})
            else:
                content = request.POST['search_box']
                print("now search, the searching content is(recruitment):")
                print(content)
                recruitment_search = recruitment_info.objects.filter(tag=content, isDelete=0)
                print("the search result is")
                print(recruitment_search)
                return render(request, 'page-blog-list.html', {'recruitment_infos': recruitment_search, 'message': bb, 'teacher_student': cc})
        if "show_course" in request.POST:
            print("now show course content")
            course_info = course.objects.filter(state=0).order_by('-date_created')
            aa = 1
            return render(request, 'page-blog-list.html',{'course_infos': course_info, 'message': bb, 'teacher_student': cc})
        if "show_recruitment" in request.POST:
            print("now show recruitment content")
            recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
            aa = 0
            return render(request, 'page-blog-list.html',{'recruitment_infos':recruitment, 'message': bb, 'teacher_student': cc})
        if "read_course" in request.POST:
            print("read detail information about course")
            course_id = request.POST['course_id']
            print("now let's see course id")
            tep = 'info_course/?id='+course_id
            print(tep)
            return redirect(tep)
        if "read_recruitment" in request.POST:
            print("read detail information about recruitment")
            re_id = request.POST['re_id']
            print("now let's see recruitment id")
            tep = 'info_course/?id=' + re_id
            print(tep)
            return redirect(tep)
        if "submit_info" in request.POST:
            user = get_user_model()
            user = user.objects.get(email=request.session['user_email'])
            id = user.identity
            print("aaaaaaaaa let's see his identity!!!!!")
            print(id)
            if id == 'S':
                print("in submitting the info(student)")
                form = Publish(request.POST)
                if form.is_valid():
                    title = request.POST['title']
                    description = request.POST['description']
                    start_date = request.POST['start_date']
                    start_time = request.POST['start_time']
                    end_date = request.POST['end_date']
                    end_time = request.POST['end_time']
                    scope = request.POST['scope']
                    tag = request.POST['tag']
                    price = request.POST['price']
                    teaching_age = request.POST['teaching_age']
                    city = request.POST['city']
                    num = request.POST['num']
                    dstart_date = datetime.strptime(start_date, '%Y-%m-%d')
                    dstart_time = datetime.strptime(start_time,'%H:%M')
                    dend_date = datetime.strptime(end_date, '%Y-%m-%d')
                    dend_time = datetime.strptime(end_time,'%H:%M')
                    global route
                    route = fileRoute
                    print("now show you the start time and end time")
                    print(dstart_date)
                    print(dstart_time)
                    print(dend_date)
                    print(dend_time)
                    print(route)
                    print(num)
                    if dstart_date == dend_date:
                        if dstart_time < dend_time:
                            if dstart_date > datetime.now():
                                r = recruitment_info(stuID_id=user.userID, date_created=datetime.now(), courseContent=description, tag=tag, recruitmentName=title, startTime=dstart_date,courseStartTime=dstart_time, endTime=dend_date, courseEndTime=dend_time, scope=scope, price=price, teaching_age=teaching_age, city=city, peopleNum=num, picture1=route)
                                r.save()
                                recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                                res = recruitment.filter(courseContent=description)
                                print("now let's see the res")
                                print(res)
                                i = str(res[0])
                                print("i")
                                print(i)
                                temp = i.split( )
                                print("temp")
                                print(temp)
                                ii = temp[2]
                                print("ii")
                                print(ii)
                                id = ii.strip('(').strip(')')
                                tt = 'rcomment_' + id
                                print("now let's see the table name of this dynamic table:")
                                print(tt)
                                aa = 1
                                aa = 0
                                # CreateNewMessage(tt)
                                fields = {
                                    "floor_id": models.AutoField(primary_key=True),
                                    "from_name": models.CharField(max_length=32),
                                    "to_floor": models.IntegerField(default=0),
                                    "to_name": models.CharField(max_length=32),
                                    "send_time": models.DateTimeField(default=timezone.now),
                                    "content": models.TextField(),
                                    "read": models.IntegerField(default=0),
                                    '__str__': lambda self: '%d %s %d %s %s %s %d' % (
                                        self.floor_id, self.from_name, self.to_floor, self.to_name, self.send_time,
                                        self.content,self.read),
                                }
                                options = {'ordering': ['floor_id', 'from_name', 'to_floor', 'to_name', 'send_time',
                                                        'content','read'],
                                           'verbose_name': 'valued customer'}
                                course_message = create_model1(tt, fields, options=options, app_label='my_app',
                                                               module='models')
                                install(course_message)  # 同步到数据库中
                                return render(request, 'page-blog-list.html', {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc})
                            else:
                                print("start date is earlier than current date")
                                recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                                messages.error(request, "wrong time!")
                                return render(request, 'page-blog-list.html',
                                        {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc,
                                         'error': 'wrong time'})
                        else:
                            print("start time is later than current time")
                            recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                            messages.error(request, "wrong time!")
                            return render(request, 'page-blog-list.html',
                                          {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc,
                                           'error': 'wrong time'})
                    elif dstart_date < dend_date:
                        if dstart_date > datetime.now():
                            r = recruitment_info(stuID_id=user.userID, date_created=datetime.now(),
                                                 courseContent=description, tag=tag, recruitmentName=title, startTime=dstart_date, courseStartTime=dstart_time, endTime=dend_date, courseEndTime=dend_time, scope=scope, price=price,
                                                 teaching_age=teaching_age, city=city, peopleNum=num, picture1=route)
                            r.save()
                            recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                            res = recruitment.filter(courseContent=description)
                            print("now let's see the res")
                            print(res)
                            i = str(res[0])
                            print("i")
                            print(i)
                            temp = i.split()
                            print("temp")
                            print(temp)
                            ii = temp[2]
                            print("ii")
                            print(ii)
                            id = ii.strip('(').strip(')')
                            tt = 'rcomment_' + id
                            print("now let's see the table name of this dynamic table:")
                            print(tt)
                            aa = 1
                            aa = 0
                            # CreateNewMessage(tt)

                            fields = {
                                "floor_id": models.AutoField(primary_key=True),
                                "from_name": models.CharField(max_length=32),
                                "to_floor": models.IntegerField(default=0),
                                "to_name": models.CharField(max_length=32),
                                "send_time": models.DateTimeField(default=timezone.now),
                                "content": models.TextField(),
                                "read": models.IntegerField(default=0),
                                '__str__': lambda self: '%d %s %d %s %s %s %d' % (
                                    self.floor_id, self.from_name, self.to_floor, self.to_name, self.send_time,
                                    self.content, self.read),
                            }
                            options = {'ordering': ['floor_id', 'from_name', 'to_floor', 'to_name', 'send_time',
                                                    'content', 'read'],
                                       'verbose_name': 'valued customer'}
                            course_message = create_model1(tt, fields, options=options, app_label='my_app',
                                                           module='models')
                            install(course_message)  # 同步到数据库中
                            return render(request, 'page-blog-list.html',
                                          {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc})
                        else:
                            print("start date is earlier than current date")
                            recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                            messages.error(request, "wrong time!")
                            return render(request, 'page-blog-list.html',
                                          {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc,
                                           'error': 'wrong time'})
                    else:
                        print("start date is later than end date")
                        recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                        messages.error(request, "wrong time!")
                        return render(request, 'page-blog-list.html',
                                      {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc,
                                       'error': 'wrong time'})
                else:
                    print("form is not valid!")
                    recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                    messages.error(request, "wrong time!")
                    return render(request, 'page-blog-list.html',{'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc, 'error':form.errors})
            else:
                print("in submitting the info(teacher)")
                form = Publish(request.POST)
                if form.is_valid():
                    title = request.POST['title']
                    description = request.POST['description']
                    start_date = request.POST['start_date']
                    start_time = request.POST['start_time']
                    end_date = request.POST['end_date']
                    end_time = request.POST['end_time']
                    scope = request.POST['scope']
                    tag = request.POST['tag']
                    price = request.POST['price']
                    teaching_age = request.POST['teaching_age']
                    city = request.POST['city']
                    num = request.POST['num']
                    dstart_date = datetime.strptime(start_date, '%Y-%m-%d')
                    dstart_time = datetime.strptime(start_time, '%H:%M')
                    dend_date = datetime.strptime(end_date, '%Y-%m-%d')
                    dend_time = datetime.strptime(end_time, '%H:%M')
                    route = fileRoute
                    print("now show you the start time and end time")
                    print(dstart_date)
                    print(dstart_time)
                    print(dend_date)
                    print(dend_time)
                    route = fileRoute
                    if dstart_date == dend_date:
                        if dstart_time < dend_time:
                            if dstart_date > datetime.now():
                                c = course(teacherID_id=user.userID, date_created=datetime.now(), courseContent=description, tag=tag, courseName=title, startTime=dstart_date,courseStartTime=dstart_time, endTime=dend_date, courseEndTime=dend_time, scope=scope, price=price, teaching_age=teaching_age, city=city, peopleNum=num,left=num, taken=0, state=0, picture1=route)
                                c.save()
                                course_info = course.objects.filter(state=0).order_by('-date_created')
                                res = course_info.filter(courseContent = description)

                                print("now let's see the res")
                                print(res)
                                i = str(res[0])
                                print("i")
                                print(i)
                                temp = i.split()
                                print("temp")
                                print(temp)
                                ii = temp[2]
                                print("ii")
                                print(ii)
                                id = ii.strip('(').strip(')')
                                tt = 'comment_' + id
                                print("now let's see the table name of this dynamic table:")
                                print(tt)
                                fields = {
                                    "floor_id": models.AutoField(primary_key=True),
                                    "from_name": models.CharField(max_length=32),
                                    "to_floor": models.IntegerField(default=0),
                                    "to_name": models.CharField(max_length=32),
                                    "send_time": models.DateTimeField(default=timezone.now),
                                    "content": models.TextField(),
                                    "read": models.IntegerField(default=0),
                                    '__str__': lambda self: '%d %s %d %s %s %s %d' % (
                                        self.floor_id, self.from_name, self.to_floor, self.to_name, self.send_time,
                                        self.content, self.read),
                                }
                                options = {'ordering': ['floor_id', 'from_name', 'to_floor', 'to_name', 'send_time',
                                                        'content', 'read'],
                                           'verbose_name': 'valued customer'}
                                course_message = create_model1(tt, fields, options=options, app_label='my_app',
                                                               module='models')
                                install(course_message)  # 同步到数据库中
                                return render(request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                            else:
                                course_info = course.objects.filter(state=0).order_by('-date_created')
                                messages.error(request, "Start date should be later than current date!")
                                return render (request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                        else:
                            course_info = course.objects.filter(state=0).order_by('-date_created')
                            messages.error(request, "Start time should be earlier than end time!")
                            return render (request, 'page-blog-list.html',
                                    {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                    elif dstart_date < dend_date:
                        if dstart_date > datetime.now():
                            c = course(teacherID_id=user.userID, date_created=datetime.now(), courseContent=description,
                                       tag=tag, courseName=title, startTime=dstart_date,courseStartTime=dstart_time, endTime=dend_date, courseEndTime=dend_time, scope=scope,
                                       price=price, teaching_age=teaching_age, city=city, peopleNum=num, state=0, left=num, taken=0,
                                       picture1=route)
                            c.save()
                            course_info = course.objects.filter(state=0).order_by('-date_created')
                            res = course_info.filter(courseContent=description)

                            print("now let's see the res")
                            print(res)
                            i = str(res[0])
                            print("i")
                            print(i)
                            temp = i.split()
                            print("temp")
                            print(temp)
                            ii = temp[2]
                            print("ii")
                            print(ii)
                            id = ii.strip('(').strip(')')
                            tt = 'comment_' + id
                            print("now let's see the table name of this dynamic table:")
                            print(tt)
                            fields = {
                                "floor_id": models.AutoField(primary_key=True),
                                "from_name": models.CharField(max_length=32),
                                "to_floor": models.IntegerField(default=0),
                                "to_name": models.CharField(max_length=32),
                                "send_time": models.DateTimeField(default=timezone.now),
                                "content": models.TextField(),
                                "read": models.IntegerField(default=0),
                                '__str__': lambda self: '%d %s %d %s %s %s %d' % (
                                    self.floor_id, self.from_name, self.to_floor, self.to_name, self.send_time,
                                    self.content, self.read),
                            }
                            options = {'ordering': ['floor_id', 'from_name', 'to_floor', 'to_name', 'send_time',
                                                    'content', 'read'],
                                       'verbose_name': 'valued customer'}
                            course_message = create_model1(tt, fields, options=options, app_label='my_app',
                                                           module='models')
                            install(course_message)  # 同步到数据库中
                            return render(request, 'page-blog-list.html',
                                          {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                        else:
                            course_info = course.objects.filter(state=0).order_by('-date_created')
                            messages.error(request, "Start date should be later than current date!")
                            return render(request, 'page-blog-list.html',
                                    {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                    else:
                        course_info = course.objects.filter(state=0).order_by('-date_created')
                        messages.error(request, "Start date should be earlier than end date!")
                        return render(request, 'page-blog-list.html',
                                {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                else:
                    course_info = course.objects.filter(state=0).order_by('-date_created')
                    messages.error(request, "wrong time!")
                    return render(request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc, 'error': form.errors})
            pass
        if "logout" in request.POST:
            request.session['is_login'] = False
            return render(request, 'index.html')
        else:
            if aa == 1:
                print("in other conditions//upload pictures//teacher")
                myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
                print("now lets see myfile")
                print(myFile)
                if not myFile:
                    print("no my file")
                    course_info = course.objects.filter(state=0).order_by('-date_created')
                    messages.error(request, "You do not choose any file!")
                    return render(request, 'page-blog-list.html',{'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                    #return HttpResponse("no file to upload!")
                else:
                    route = os.path.join("../static/images/test_feng", myFile.name)
                    print("the route is")
                    print(route)
                    print("now let's see the route stipped")
                    temp = route.split('/')
                    r = temp[1] + '/' + temp[2] + '/' + temp[3] + '/' + temp[4]
                    print(r)
                    fileRoute = r
                    destination = open(fileRoute, 'wb+')  # 打开特定的文件进行二进制的写操作
                    for chunk in myFile.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
                # return HttpResponse("upload over!")
                course_info = course.objects.filter(state=0).order_by('-date_created')
                messages.success(request, "successfully loaded!")
                return render(request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
            else:
                if iden == 'S':
                    print("in other conditions//upload pictures//student")
                    myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
                    print("now lets see myfile")
                    print(myFile)
                    if not myFile:
                        print("no my file")
                        recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                        messages.error(request, "You do not choose any file!")
                        return render(request, 'page-blog-list.html',
                                      {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc})
                        # return HttpResponse("no file to upload!")
                    else:
                        route = os.path.join(
                            "../static/images/test_feng", myFile.name)
                        print("the route is")
                        print(route)
                        print("now let's see the route stipped")
                        temp = route.split('/')
                        r = temp[1] + '/' + temp[2] + '/' + temp[3] + '/' + temp[4]
                        print(r)
                        fileRoute = r
                        destination = open(fileRoute, 'wb+')  # 打开特定的文件进行二进制的写操作
                        for chunk in myFile.chunks():  # 分块写入文件
                            destination.write(chunk)
                        destination.close()
                    # return HttpResponse("upload over!")
                    recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                    messages.success(request, "successfully loaded!")
                    return render(request, 'page-blog-list.html',
                                  {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc})
                elif iden == 'T':
                    print("in other conditions//upload pictures//teacher")
                    myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
                    print("now lets see myfile")
                    print(myFile)
                    if not myFile:
                        print("no my file")
                        course_info = course.objects.filter(state=0).order_by('-date_created')
                        messages.error(request, "You do not choose any file!")
                        return render(request, 'page-blog-list.html',
                                      {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                        # return HttpResponse("no file to upload!")
                    else:
                        route = os.path.join(
                            "../static/images/test_feng",
                            myFile.name)
                        print("the route is")
                        print(route)
                        print("now let's see the route stipped")
                        temp = route.split('/')
                        r =  temp[1] + '/' + temp[2] + '/' + temp[3] + '/' + temp[4]
                        print(r)
                        fileRoute = r
                        destination = open(fileRoute, 'wb+')  # 打开特定的文件进行二进制的写操作
                        for chunk in myFile.chunks():  # 分块写入文件
                            destination.write(chunk)
                        destination.close()
                    # return HttpResponse("upload over!")
                    course_info = course.objects.filter(state=0).order_by('-date_created')
                    messages.success(request, "successfully loaded!")
                    return render(request, 'page-blog-list.html',
                                  {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
#
# @csrf_exempt
# def password_modify(request):
#     form = ModifyPassword(request.POST)
#     if form.is_valid():
#         oldpassword= form.cleaned_data['password3']
#         newpassword = form.cleaned_data['password4']
#         # user = auth.authenticate(email=email, password=password)
#         user = get_user_model()
#
#         person = user.objects.get(email=request.session.get('user_email'))
#         if(person.password==oldpassword):
#             request.session['user_password'] = newpassword
#             person.password=newpassword
#             person.save()
#             render(request, 'password_modify.html', {'mes1': "Success modify password!"})
#         else:
#             return render(request, 'password_modify.html', {'mes': "password is invalid."})
#
#     return render(request, 'password_modify.html', {'error': form.errors, 'form': form})
#
# @csrf_exempt
# def email_modify(request):
#     form = ModifyEmail(request.POST)
#     if form.is_valid():
#         newemail= form.cleaned_data['newemail']
#         # user = auth.authenticate(email=email, password=password)
#         user = get_user_model()
#         person = user.objects.get(email=request.session.get('user_email'))
#         request.session['user_email'] = newemail
#         person.email= newemail
#         person.save()
#         return render(request, 'email_modify.html', {'mes1': "Success modify email!"})
#
#     return render(request, 'email_modify.html', {'error': form.errors, 'form': form})
#
# def email_modify1(request):
#     if request.session.get('is_login', None):
#        return render(request, 'email_modify.html',{'email':request.session.get('username')})
#     else:
#         return render(request, 'login.html')
#
# def password_modify1(request):
#     if request.session.get('is_login', None):
#         return render(request, 'password_modify.html',{'email':request.session.get('username')})
#     else:
#         return render(request, 'login.html')


@csrf_exempt
def info_course(request):
    if request.method == 'GET': #使用？id=xxx传参
        courseID_id = request.GET.get('id')
        print("the course id is")
        print(courseID_id)
        commentTable = "my_app_comment_" + courseID_id
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """SELECT * FROM '%s'""" % (commentTable)
            cursor.execute(sql)
            # 查出一条数据
            # row = cursor.fetchone()
            # 查出所有数据
            rows = cursor.fetchall()
            cursor.close()
        comments_raw = [[] for _ in range(len(rows))]
        comments = []
        index = []
        for i,row in enumerate(rows):
           #row[2]为to_floor
            if row[2] == 0:
                comments_raw[i].append(row)
                index.append(row[0])
            else:
                for j,item in enumerate(index):
                    if row[2]==item:
                        comments_raw[item-1].append(row)
                        break
        '''
        删掉空元素
        for i,comment_raw in enumerate(comments_raw):
            if comment_raw == []:
                continue
            comments.append(comment_raw)
        print(comments)'''
        # 把二维数组拆开
        for i,comment_raw in enumerate(comments_raw):
            if comment_raw == []:
                continue
            for comment_item in comment_raw:
                dict = {
                    'floor_id': comment_item[0],
                    'from_name': comment_item[1],
                    'to_floor': comment_item[2],
                    'to_name': comment_item[3],
                    'send_time': comment_item[4],
                    'content': comment_item[5]
                }
                comments.append(dict)
        print("这是comment")
        print(comments)
        c = course.objects.get(ID=courseID_id)
        print("这是c")
        print(c.teacherID_id)
        teacher = UserProfile.objects.get(userID=c.teacherID_id)
        '''测试comments内容
        for comment in comments:
            if len(comment)!=1:
                print("显示")
                print(comment[0])
                for i in range(1,len(comment)):
                    print("楼中楼显示")
                    print(comment[i])
            else:
                print("显示")
                print(comment)
        #测试comments内容
        for comment in comments:
            print("\n\n")
            print(comment)'''
        #并没有写进身份
        #print(request.session['identity'])
        user = get_user_model()
        user = user.objects.get(email=request.session['user_email'])
        iden = user.identity
        if request.session.get('is_login', None):
            if c.left > 0:
                if iden == 'S':
                    return render(request, 'info_course.html',{'course': c, 'teacher': teacher, 'enable': True, 'enable_comment': True,'comments': comments})
                else:
                    return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': False,'enable_comment': True,'comments':comments})
            else:
                return render(request, 'info_course.html',{'course': c, 'teacher': teacher, 'enable': False, 'enable_comment': True,'comments': comments})
        else:
            print('进来2')
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': False,'enable_comment': False,'comments':comments})
    if request.method == 'POST':
        if request.POST.get('operation') == 'purchase':
            state = request.POST.get('state')
            courseID_id = request.GET.get('id')
            user = UserProfile.objects.get(email = request.session['user_email'])
            c_obj = course.objects.get(ID=courseID_id)
            course.objects.filter(ID=courseID_id).update(left=c_obj.left - 1)
            course.objects.filter(ID=courseID_id).update(taken=c_obj.taken + 1)
            course_order.objects.create(date_created=datetime.now(),state=state, courseID=courseID_id, stuID=user.userID)
        else:
            print('留言')
            courseID_id = request.GET.get('id')
            commentTable = "my_app_comment_" + courseID_id
            content = request.POST.get('review')
            to_name = request.POST.get('to_name')
            to_floor = request.POST.get('to_id')
            from_name=request.session['username']
            send_time=datetime.now()
            print('内容')
            print(content)
            #插入数据库
            with connection.cursor() as cursor:
                # 执行sql语句
                sql = """INSERT INTO '%s' (from_name,to_floor,to_name,send_time,content) VALUES ('%s','%d','%s','%s','%s')""" % (
                    commentTable, from_name, int(to_floor), to_name, send_time, content)
                cursor.execute(sql)
                cursor.close()
            print("成功")
            return redirect("/?id=")
            #course_order.objects.create(send_time=datetime.now(),from_name=from_name,to_name=to_name,to_floor=to_floor,content=content)

@csrf_exempt
def info_recruitment(request):
    if request.method == 'GET': #使用？id=xxx传参
        recruitment_id = request.GET.get('id')
        commentTable = "my_app_rcomment_" + recruitment_id
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """SELECT * FROM '%s'""" % (commentTable)
            cursor.execute(sql)
            # 查出一条数据
            # row = cursor.fetchone()
            # 查出所有数据
            rows = cursor.fetchall()
            cursor.close()
        comments_raw = [[] for _ in range(len(rows))]
        comments = []
        index = []
        for i,row in enumerate(rows):
           #row[2]为to_floor
            if row[2] == 0:
                comments_raw[i].append(row)
                index.append(row[0])
            else:
                for j,item in enumerate(index):
                    if row[2]==item:
                        comments_raw[item-1].append(row)
                        break
        '''
        删掉空元素
        for i,comment_raw in enumerate(comments_raw):
            if comment_raw == []:
                continue
            comments.append(comment_raw)
        print(comments)'''
        # 把二维数组拆开
        for i,comment_raw in enumerate(comments_raw):
            if comment_raw == []:
                continue
            for comment_item in comment_raw:
                dict = {
                    'floor_id': comment_item[0],
                    'from_name': comment_item[1],
                    'to_floor': comment_item[2],
                    'to_name': comment_item[3],
                    'send_time': comment_item[4],
                    'content': comment_item[5]
                }
                comments.append(dict)
        print("这是comment")
        print(comments)
        r = recruitment_info.objects.get(ID=recruitment_id)
        student = UserProfile.objects.get(userID=r.stuID_id)
        '''测试comments内容
        for comment in comments:
            if len(comment)!=1:
                print("显示")
                print(comment[0])
                for i in range(1,len(comment)):
                    print("楼中楼显示")
                    print(comment[i])
            else:
                print("显示")
                print(comment)
        #测试comments内容
        for comment in comments:
            print("\n\n")
            print(comment)'''
        #并没有写进身份
        #print(request.session['identity'])
        if request.session.get('is_login', None):
            return render(request, 'info_recruitment.html', {'recruitment_info': r,'student': student,'enable_comment': True,'comments':comments})
        else:
            return render(request, 'info_recruitment.html', {'recruitment_info': r,'student': student,'enable_comment': False,'comments':comments})
    if request.method == 'POST':
        recruitment_id = request.GET.get('id')
        commentTable = "my_app_comment_" + recruitment_id
        content = request.POST.get('review')
        to_name = request.POST.get('to_name')
        to_floor = request.POST.get('to_id')
        from_name= request.session['username']
        send_time=datetime.now()
        print('这是内容')
        print(content)
        #插入数据库
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """INSERT INTO '%s' (from_name,to_floor,to_name,send_time,content) VALUES ('%s','%d','%s','%s','%s')""" % (
                commentTable, from_name, int(to_floor), to_name, send_time, content)
            cursor.execute(sql)
            cursor.close()
        print("成功")
        return redirect("/?id=")
        #course_order.objects.create(send_time=datetime.now(),from_name=from_name,to_name=to_name,to_floor=to_floor,content=content)
