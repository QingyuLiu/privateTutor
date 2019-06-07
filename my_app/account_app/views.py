from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import UserProfile
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail,Publish
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import course, recruitment_info
import datetime
from datetime import datetime
from django.contrib import messages
import os
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
        if request.method == 'POST':
            print('ajax')
            return render(request, 'page-employer-profile.html')
        else:
            return render(request, 'page-employer-profile.html')
    else:
        return render(request, 'index.html')


@csrf_exempt
def protect1(request):
    if request.session.get('is_login', None):
        return render(request, 'me.html')
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
                            return render(request, 'page-blog-list.html', {'mes1': "You have already been login."})
                        request.session['user_email'] = email
                        request.session['user_password'] =password
                        request.session['is_login'] = True
                        request.session['username'] =person.username
                        obj=person.date_joined
                        request.session['created_at'] =obj.strftime('%Y-%m-%d %H:%M:%S')

                        request.session['identity'] = person.identity
                        request.session['gender'] = person.gender
                        request.session['age'] = person.age
                        request.session['cell_phone'] = person.cellphone
                        request.session['pay_id'] = person.pay_id
                        request.session['zone'] = person.zone
                        request.session['introduction'] = person.introduction

                        return redirect('/page-blog-list')
                        # return render(request,'/page-blog-list.html')
                    else:
                        return render(request, 'page-blog-list.html', {'mes1': "password is invalid."})
                else:
                    return render(request, 'page-blog-list.html', {'mes1': "email not found."})
        else:
               return render(request, 'page-blog-list.html',{'error':form.errors,'form1': form})

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
    if iden == 'S':
        bb = 'Recruitment'
        cc = 'Hello, dear student!'
        id = 'S'
    else:
        bb = 'Course'
        cc = 'Hello, dear teacher!'
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
            tep = 'info_course/?id='+course_id+'.html'
            print(tep)
            return redirect(tep)
        if "read_recruitment" in request.POST:
            print("read detail information about recruitment")
            re_id = request.POST['re_id']
            print("now let's see recruitment id")
            tep = 'info_course/?id=' + re_id + '.html'
            print(tep)
            return redirect(tep)
        if "submit_info" in request.POST:
            user = get_user_model()
            user = user.objects.get(email=request.session['user_email'])
            if id == 'S':
                print("in submitting the info(student)")
                form = Publish(request.POST)
                if form.is_valid():
                    title = request.POST['title']
                    description = request.POST['description']
                    start = request.POST['start']
                    end = request.POST['end']
                    scope = request.POST['scope']
                    tag = request.POST['tag']
                    salary = request.POST['salary']
                    teaching_age = request.POST['teaching_age']
                    city = request.POST['city']
                    num = request.POST['num']
                    dstart = datetime.strptime(start, '%Y-%m-%d %H:%M')
                    dend = datetime.strptime(end, '%Y-%m-%d %H:%M')
                    route = fileRoute
                    print("now show you the start time and end time")
                    print(dstart)
                    print(dend)
                    print(route)
                    print(num)
                    if dstart < dend:
                        if dstart > datetime.now():
                            r = recruitment_info(stuID_id=user.userID, date_created=datetime.now(), courseContent=description, tag=tag, recruitmentName=title, start_time=start, end_time=end, scope=scope, salary=salary, teaching_age=teaching_age, city=city, peopleNum=num, picture1=route)
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
                            fields = {
                                    'id_from': models.IntegerField(max_length=100),
                                    'id_to': models.IntegerField(max_length=100),
                                    'content': models.CharField(max_length=1024),
                                    'time': models.DateTimeField(max_length=10240),
                                    '__str__': lambda self: '%s %s %s %s' % (self.id_from, self.id_to, self.content, self.time),
                                    }
                            options = {'ordering': ['id_from', 'id_to', 'content', 'time'], 'verbose_name': 'valued customer' }
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
                        print("start date is later than end date")
                        recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                        messages.error(request, "wrong time!")
                        return render(request, 'page-blog-list.html',
                                {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc,
                                 'error': 'wrong time'})
                else:
                    recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                    return render(request, 'page-blog-list.html',{'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc, 'error':form.errors})
            else:
                print("in submitting the info(teacher)")
                form = Publish(request.POST)
                if form.is_valid():
                    title = request.POST['title']
                    description = request.POST['description']
                    start = request.POST['start']
                    end = request.POST['end']
                    scope = request.POST['scope']
                    tag = request.POST['tag']
                    salary = request.POST['salary']
                    teaching_age = request.POST['teaching_age']
                    city = request.POST['city']
                    num = request.POST['num']
                    dstart = datetime.strptime(start, '%Y-%m-%d %H:%M')
                    dend = datetime.strptime(end, '%Y-%m-%d %H:%M')
                    route = fileRoute
                    if dstart < dend:
                        if dstart > datetime.now():
                            c = course(teacherID_id=user.userID, date_created=datetime.now(), courseContent=description, tag=tag, courseName=title, start_time=start, end_time=end, scope=scope, salary=salary, teaching_age=teaching_age, city=city, peopleNum=num, state=0, picture1=route)
                            c.save()
                            course_info = course.objects.filter(state=0).order_by('-date_created')
                            res = course_info.filter(courseContent = description)
                            fields = {
                                'id_from': models.IntegerField(max_length=100),
                                'id_to': models.IntegerField(max_length=100),
                                'content': models.CharField(max_length=1024),
                                'time': models.DateTimeField(max_length=10240),
                                '__str__': lambda self: '%s %s %s %s' % (
                                self.id_from, self.id_to, self.content, self.time),
                            }
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
                            options = {'ordering': ['id_from', 'id_to', 'content', 'time'],
                                       'verbose_name': 'valued customer'}
                            course_message = create_model1(tt, fields, options=options,
                                                           app_label='my_app',
                                                           module='models')
                            install(course_message)  # 同步到数据库中
                            return render(request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                        else:
                            course_info = course.objects.filter(state=0).order_by('-date_created')
                            messages.error(request, "Start date should be later than current date!")
                            return (request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                    else:
                        course_info = course.objects.filter(state=0).order_by('-date_created')
                        messages.error(request, "Start date should be earlier than end date!")
                        return (request, 'page-blog-list.html',
                                {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
                else:
                    course_info = course.objects.filter(state=0).order_by('-date_created')
                    return (request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc, 'error': form.errors})
            pass
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
                    route = os.path.join("/Users/fengyushan/PycharmProjects/privateTutor/my_app/static/images/test_feng", myFile.name)
                    print("the route is")
                    print(route)
                    print("now let's see the route stipped")
                    temp = route.split('/')
                    r = temp[6]+'/'+temp[7]+'/'+temp[8]+'/'+temp[9]
                    print(r)
                    fileRoute = r
                    destination = open(route, 'wb+')  # 打开特定的文件进行二进制的写操作
                    for chunk in myFile.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
                # return HttpResponse("upload over!")
                course_info = course.objects.filter(state=0).order_by('-date_created')
                messages.success(request, "successfully loaded!")
                return render(request, 'page-blog-list.html', {'course_infos': course_info, 'message': bb, 'teacher_student': cc})
            else:
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
                        "/Users/fengyushan/PycharmProjects/privateTutor/my_app/static/images/test_feng", myFile.name)
                    print("the route is")
                    print(route)
                    print("now let's see the route stipped")
                    temp = route.split('/')
                    r = temp[6] + '/' + temp[7] + '/' + temp[8] + '/' + temp[9]
                    print(r)
                    fileRoute = r
                    destination = open(route, 'wb+')  # 打开特定的文件进行二进制的写操作
                    for chunk in myFile.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
                # return HttpResponse("upload over!")
                recruitment = recruitment_info.objects.filter(isDelete=0).order_by('-date_created')
                messages.success(request, "successfully loaded!")
                return render(request, 'page-blog-list.html',
                              {'recruitment_infos': recruitment, 'message': bb, 'teacher_student': cc})

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
        id = request.GET.get('id')
        c = course.objects.get(ID=id)
        teacher = UserProfile.objects.get(userID=c.teacherID_id)
        if request.session.get('is_login', None):
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': True})
        else:
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': False})
    if request.method == 'POST':
        pass