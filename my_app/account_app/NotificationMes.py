from . import models
from django.db import connection
import operator
from django.contrib.auth import get_user_model
def getNotifications(username,identity):
    '''
           ------------------------
           ------通知信息-----
           ------------------------
                                   '''

    notificationInfo = []

    '''课程留言'''
    courses = models.course.objects.all().values('ID')    #只取ID列

    for courseID_id in courses:
        commentTable = "my_app_comment_%d" % (courseID_id['ID'])
        print(commentTable)
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """SELECT from_name,send_time,floor_id FROM '%s' WHERE to_name = '%s' and read = 0""" % (commentTable,username)
            print(sql)
            cursor.execute(sql)
            # 查出一条数据
            # row = cursor.fetchone()
            # 查出所有数据
            rows = cursor.fetchall()
            cursor.close()

        for row in rows:
            temp={'ID':courseID_id['ID'],'floor_id':row[2],'type':'C','from_name':row[0],'time':row[1]}
            notificationInfo.append(temp)

    '''招聘信息留言'''
    recruitment = models.recruitment_info.objects.all().values('ID')  # 只取ID列

    for recruitment_id in recruitment:
        commentTable = "my_app_rcomment_%d" % (recruitment_id['ID'])
        print(commentTable)
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """SELECT from_name,send_time,floor_id FROM '%s' WHERE to_name = '%s' and read = 0""" % (commentTable, username)
            print(sql)
            cursor.execute(sql)
            # 查出一条数据
            # row = cursor.fetchone()
            # 查出所有数据
            rows = cursor.fetchall()
            cursor.close()

        for row in rows:
            temp = {'ID': recruitment_id['ID'], 'floor_id':row[2],'type': 'R', 'from_name': row[0],'time':row[1]}
            notificationInfo.append(temp)

    '''老师审核退课'''
    if identity == 'T':
        teacher=get_user_model().objects.get(username=username)
        courses=models.course.objects.filter(teacherID_id=teacher.userID)

        for course in courses:
            orders = models.course_order.objects.filter(courseID_id=course.ID).order_by('-date_created')

            for order in orders:
                if order.state == 'R':
                    stuName=get_user_model().objects.get(userID=order.stuID_id)
                    temp={'ID':order.ID,'type':'Refund','name':stuName.username,'time':order.date_created}
                    notificationInfo.append(temp)

    print(notificationInfo)
    sorted_x = sorted(notificationInfo, key=operator.itemgetter('time'),reverse=True)
    return sorted_x