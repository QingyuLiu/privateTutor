from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import UserProfile
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import course
from django.http import JsonResponse

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
                        return render(request,'/page-blog-list.html')
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
        id = request.GET.get('id')
        c = course.objects.get(ID=id)
        teacher = UserProfile.objects.get(userID=c.teacherID_id)
        if request.session.get('is_login', None):
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': True})
        else:
            return render(request, 'info_course.html', {'course': c,'teacher': teacher,'enable': False})
    if request.method == 'POST':
        pass