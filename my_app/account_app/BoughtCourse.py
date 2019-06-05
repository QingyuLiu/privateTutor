from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from . import models
import json
from .forms import RegistrationForm, LogForm,ModifyPassword,ModifyEmail
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt#显示已购买课程的信息 以及退课或删除已完成课程订单
def BoughtCourseInfo(request):
    if request.method == 'GET':
        courseInfoList=[]
        user = get_user_model()

        # 订单-id、学生id、课程id、日期、订单状态
        orders = models.course_order.objects.filter(stuID_id=request.session.get('userID')).exclude(state='D')

        for order in orders:
            course=models.course.objects.get(ID=order.courseID_id)
            teacher=user.objects.get(userID=course.teacherID_id)
            if order.state == 'C':
                txt='已完成'
            elif order.state == "UP":
                txt='未支付'
            elif order.state == 'N':
                txt='进行中'
            elif order.state == 'R':
                txt='退款审核中'
            elif order.state == 'CL':
                txt='交易已关闭'
            else:
                txt='error'

            courseInfo = {'id':order.ID,'courseName':course.courseName,
                          'teacher':teacher.username, 'tag':course.tag, 'time':course.time,
                          'price':course.price, 'state':txt}
            courseInfoList.append(courseInfo)

        print(courseInfoList)
        return render(request, 'page-employer-resume.html',{
            'courseInfoList': courseInfoList,
        })

    if request.method=="POST":
        id = request.GET.get('id')
        print(id)
        order = models.course_order.objects.get(ID=id)
        if order.state == "C" and order.state == "CL":
            order.update(state="D")
            message = "成功删除订单！"
        elif order.state == "UP":
            order.state = "CL"
            order.save
            message = "成功取消订单！"

        request.session['message'] = message
        return render(request, 'page-employer-resume.html', {
            'message': message,
        })


