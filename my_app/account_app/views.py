from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import UserProfile,course_order
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import course
from django.http import JsonResponse
from datetime import datetime
from django.db import connection

import json

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

                        return redirect('/page-blog-list')
                        return render(request,'/page-blog-list.html')
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

@csrf_exempt
def homepage(request):
    return render(request,'page-blog-list.html')

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
        commentTable = "comment_" + courseID_id
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
        if request.session.get('is_login', None) & c.left > 0:
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': True,'comments':comments})
        else:
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': False,'comments':comments})
    if request.method == 'POST':
        if request.POST.get('operation') == 'purchase':
            state = request.POST.get('state')
            courseID_id = request.GET.get('id')
            user = UserProfile.objects.get(email = request.session['user_email'])
            c_obj = course.objects.get(ID=courseID_id)
            course.objects.filter(ID=courseID_id).update(left=c_obj.left - 1)
            course.objects.filter(ID=courseID_id).update(taken=c_obj.taken + 1)
            course_order.objects.create(date_created=datetime.now(),state=state, courseID_id=courseID_id, stuID_id=user.userID)
        else:
            courseID_id = request.GET.get('id')
            commentTable = "comment_" + courseID_id
            content = request.POST.get('review')
            to_name = request.POST.get('to_name')
            to_floor = request.POST.get('to_id')
            from_name=request.session['username']
            send_time=datetime.now()
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


