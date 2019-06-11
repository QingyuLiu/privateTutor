
def getNotifications(username):
    '''
           ------------------------
           ------通知信息-----
           ------------------------
                                   '''

    notificationInfo = []
    comments=[[]]
    rcomments=[[]]
    courses = models.course.objects.all().values('ID')    #只取ID列

    for courseID_id in orders:
        commentTable = "my_app_comment_" + courseID_id
        with connection.cursor() as cursor:
            # 执行sql语句
            sql = """SELECT from_name FROM '%s' WHERE to_name = '%s' and read = 0""" % (commentTable,username)
            print(sql)
            cursor.execute(sql)
            # 查出一条数据
            # row = cursor.fetchone()
            # 查出所有数据
            rows = cursor.fetchall()
            cursor.close()

        print(rows)
        comments={'courseID':courseID_id,'type':'C','from_name':rows}
