import json
from datetime import *

import pymssql
from flask import Flask
from flask.ctx import _request_ctx_stack
from flask_cors import CORS
from flask_restful import Api, Resource
from gevent import pywsgi

from send_email_all import *

# from pyannoteAudioSR import *


app = Flask(__name__)
api = Api(app)
CORS(app, resources=r'/*')

database = 'CN_FstHMST_CyberTA'
host = '47.103.13.21'
user = 'sa'
password = 'chenniao'
# conn_info = 'DRIVER={ODBC Driver 17 for SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s'%(database, host, user, password)
# con = pyodbc.connect(conn_info)
# cur = con.cursor()

conn = pymssql.connect(server=host, user=user, password=password, database=database)
cursor = conn.cursor()


class getonlineid(Resource):
    def get(self):
        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        try:
            had = [59, 51, 53, 50, 49, 58, 54]
            nums = []
            for a in had:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                now = datetime.now()
                out_date = (now + timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
                sql = "select count(ID) as times from I_Emotion where StudentId ='" + str(
                    a + 1) + "' and Time > '" + out_date + "'"
                print(sql)
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                if rowAsList[0] > 5:
                    nums.append(a)
            steps = []
            for b in nums:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                sql = "select RealName from I_Users where ID ='" + str(b) + "'"
                print(sql)
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                # step = { "name": rowAsList[0]}
                steps.append(rowAsList[0])
            print(steps)
        except Exception as e:
            raise e
        response = {
            'names': steps
        }

        return response


class getName(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic['id']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select RealName from I_Users where ID ='" + str(id) + "'"
            print(sql)
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            rowAsList = [x for x in resList[0]]
        except Exception as e:
            raise e
        response = {
            'name': rowAsList[0]
        }

        return response


class getUserInfo(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        name = dic['name']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_paticipater where name ='" + str(name) + "'"
            print(sql)
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (name, stuid, role, ispermanent, ID, pd, email, remark) in resList:
                step = {"name": name, "stuid": stuid, "role": role, "ispermanent": ispermanent, "ID": ID, "pd": pd,
                        "email": email, "remark": remark}
                steps.append(step)
            # print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class getId(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        realname = dic['name']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select ID from I_Users where RealName ='" + str(realname) + "'"
            print(sql)
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            rowAsList = [x for x in resList[0]]
        except Exception as e:
            raise e
        response = {
            'id': rowAsList[0]
        }

        return response


class emotion(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic['id']

        try:
            had = [59, 51, 53, 50, 49, 58, 54]
            nums = []
            for a in had:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                now = datetime.now()
                out_date = (now + timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
                sql = "select count(ID) as times from I_Emotion where StudentId ='" + str(
                    a + 1) + "' and Time > '" + out_date + "'"
                print(sql)
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                if rowAsList[0] > 0:
                    nums.append(a)
            if id in nums:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                sql = "select top 1 angry,disgusted,fearful,happy,sad,surprised,neutral,Time from I_Emotion where StudentId = '" + str(
                    id + 1) + "'order by id desc"
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                response = {
                    'success': 1,
                    'angry': rowAsList[0],
                    'disgusted': rowAsList[1],
                    'fearful': rowAsList[2],
                    'happy': rowAsList[3],
                    'sad': rowAsList[4],
                    'surprised': rowAsList[5],
                    'neutral': rowAsList[6],
                    'time': str(rowAsList[7])
                }
            else:
                response = {
                    'success': 0,
                }
        except Exception as e:
            raise e

        return response


class action(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic["id"]

        try:
            had = [59, 51, 53, 50, 49, 58, 54]
            nums = []
            for a in had:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                now = datetime.now()
                out_date = (now + timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
                sql = "select count(ID) as times from I_Emotion where StudentId ='" + str(
                    a + 1) + "' and Time > '" + out_date + "'"
                print(sql)
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                if rowAsList[0] > 0:
                    nums.append(a)
            if id in nums:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                sql = "select top 1 EatDrink,sleep,Phone,Rehand,Calling,Study,Time from I_Action where StudentId = '" + str(
                    id + 1) + "'order by id desc"
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                response = {
                    'success': 1,
                    'eatdrink': rowAsList[0],
                    'sleep': rowAsList[1],
                    'phone1': rowAsList[2],
                    'rehand': rowAsList[3],
                    'calling': rowAsList[4],
                    'study': rowAsList[5],
                    'time': str(rowAsList[6])
                }
            else:
                response = {
                    'success': 0,
                }
        except Exception as e:
            raise e

        return response


class conscore(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic["id"]

        try:
            had = [59, 51, 53, 50, 49, 58, 54]
            nums = []
            for a in had:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                now = datetime.now()
                out_date = (now + timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
                sql = "select count(ID) as times from I_Emotion where StudentId ='" + str(
                    a + 1) + "' and Time > '" + out_date + "'"
                print(sql)
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                if rowAsList[0] > 0:
                    nums.append(a)
            if id in nums:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                sql = "select top 1 conScore,Time from I_Concentration where StudentId = '" + str(
                    id + 1) + "'order by id desc"
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                response = {
                    'success': 1,
                    'conScore': rowAsList[0],
                    'time': str(rowAsList[1])
                }
            else:
                response = {
                    'success': 0,
                }
        except Exception as e:
            raise e

        return response


class newmeeting(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        # 会议主题
        theme = dic['theme']
        # 会议主持人
        hoster = dic['hoster']
        # 会议日期
        selectDay = dic['selectDay']
        # 会议邀请链接
        link = dic['link']
        #  会议号
        number = dic['number']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            # sql = "insert into M_Meeting (theme,hoster,date,link,number) values ('" + \
            #       theme + "','" + hoster + "','" + str(selectDay) + "','" + link + "','" +number +"')"
            # cur.execute(sql)

            # 构建参数化的 SQL 语句
            sql = """
            INSERT INTO M_Meeting (theme, hoster, date, link, number) 
            VALUES (%s, %s, %s, %s, %s);
            SELECT SCOPE_IDENTITY();
            """
            # 执行 SQL 语句
            cur.execute(sql, (theme, hoster, selectDay, link, number))
            # 获取插入的 会议ID
            inserted_id = int(cur.fetchone()[0])

            # 构建参数化的 SQL 语句，查询常驻人员创建
            sql = "SELECT * FROM M_paticipater WHERE ispermanent = 1"
            # 执行 SQL 语句
            cur.execute(sql)
            # 获取查询结果
            rows = cur.fetchall()
            # 处理查询结果
            sql = """
            INSERT INTO M_MeetingProcess (curmeeting, people, role, meetingid) 
            VALUES (%s, %s, %s, %s);
            """
            for row in rows:
                cur.execute(sql, (theme, row[0], row[2], inserted_id))
            # 提交事务
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response
        # return "ok"


class invitePati(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))

        pati = dic['pati']
        print("pati__________-")
        print(pati)
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select name,email from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()

            # rowAsList = [x for x in resList[0]]
            # print(resList)
            # print(rowAsList)
        except Exception as e:
            raise e
        # 创建一个字典来存储name和email的对应关系
        name_email_dict = {}
        # 遍历pati列表
        for person in pati:
            name = person['name']
            email = person['email']
            name_email_dict[name] = email
        meeting = getCurrentmeeting.post(self)['reslist'][0]
        print("name_lsit:")
        print(name_email_dict)
        theme = meeting['Theme']
        hoster = meeting['Hoster']
        date = meeting['Date']
        link = meeting['link']
        number = meeting['number']
        sendInvite(name_email_dict, "http://124.222.217.145:8082", theme, hoster, date, link, number)

        # 打印name和email对应关系

        response = {
            "success": 1,
        }

        # return response
        # return "ok"


class updateProcess(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))['form']
        print(dic)
        curmeeting = dic['curmeeting']
        topicName = dic['topicName']
        time = dic['time']
        people = dic['people']
        role = dic['role']
        meetingid = dic['meetingid']
        participation = dic['participation']
        participation_mode = dic['participation_mode']
        project = dic['project']
        experiment = dic['experiment']
        algorithm = dic['algorithm']
        paper = dic['paper']
        nextweekplan = dic['nextweekplan']
        completion = dic['completion']
        start_time = dic['start_time']
        end_time = dic['end_time']
        id = dic['id']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "UPDATE M_MeetingProcess SET curmeeting = %s, topicName = %s, time = %s, people = %s, role = %s, meetingid = %s, participation_mode = %s, project = %s, experiment = %s, algorithm = %s, paper = %s, nextweekplan = %s, completion = %s , start_time = %s, end_time = %s WHERE id = %s"
            params = (curmeeting, topicName, time, people, role, meetingid, participation_mode, project,
                      experiment, algorithm, paper, nextweekplan, completion, start_time, end_time, id)
            cur.execute(sql, params)
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response


class newProcess(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))['form']
        print(dic)
        curmeeting = dic['curmeeting']
        topicName = dic['topicName']
        time = dic['time']
        people = dic['people']
        role = dic['role']
        meetingid = dic['meetingid']
        # participation = dic['participation']
        participation_mode = dic['participation_mode']
        project = dic['project']
        experiment = dic['experiment']
        algorithm = dic['algorithm']
        paper = dic['paper']
        nextweekplan = dic['nextweekplan']
        completion = dic['completion']
        # id = dic['id']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "INSERT INTO M_MeetingProcess (curmeeting, topicName, time, people, role, meetingid, participation_mode, project, experiment, algorithm, paper, nextweekplan, completion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (
                curmeeting, topicName, time, people, role, meetingid, participation_mode, project, experiment,
                algorithm,
                paper, nextweekplan, completion)
            cur.execute(sql, params)
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response


class delProcess(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        id = dic['id']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "UPDATE M_MeetingProcess SET topicName = %s, time = %s, participation_mode = %s, project = %s, experiment = %s, algorithm = %s, paper = %s, nextweekplan = %s, completion = %s WHERE id = %s"
            params = (None, None, None, None, None, None, None, None,
                      None, id)
            cur.execute(sql, params)
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response


class newpati(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        name = dic['name']
        role = dic['role']
        email = dic['email']
        remark = dic['remark']
        pd = dic['pd']
        # ispermanent = dic['ispermanent']
        #
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "insert into M_paticipater (name,role,email,remark,pd) values ('" + \
                  name + "','" + role + "','" + email + "','" + remark + "','" + pd + "')"
            cur.execute(sql)
            con.commit()
            con.close()
            # rowAsList = [x for x in resList[0]]
            # print(resList)
            # print(rowAsList)
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response


class getPati(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        try:
            # con = pyodbc.connect(conn_info)
            # cur = con.cursor()
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "SELECT * FROM M_paticipater ORDER BY CASE role WHEN '教师' THEN 1 WHEN '博士生' THEN 2 WHEN '研究生' THEN 3 WHEN '本科生' THEN 4 ELSE 5 END ASC"
            cur.execute(sql)
            # resList = cur.fetchall()
            # con.commit()
            # con.close()
            # steps = []
            # for (name, stuid,role,ispermanent,id,pd,email,remark) in resList:
            #     step = {"id": int(id), "name": name, "role": role}
            #     steps.append(step)
            # print(steps)
            resList = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            con.commit()
            con.close()
            steps = []
            for row in resList:
                step = {column_names[i]: row[i] for i in range(len(column_names))}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class setOnePati(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))['form']
        print(dic)
        id = dic['id']
        stuid = dic['stuid']
        name = dic['name']
        role = dic['role']
        email = dic['email']
        remark = dic['remark']
        pd = dic['pd']
        ispermanent = dic['ispermanent']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            # 更新语句，设置所有需要更新的字段
            sql = """
                UPDATE M_paticipater 
                SET stuid = %s, name = %s, role = %s, email = %s, ispermanent = %s, remark = %s, pd = %s
                WHERE id = %s
                """
            values = (stuid, name, role, email, ispermanent, remark, pd, id)
            cur.execute(sql, values)
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            "success": 1,
        }

        return response


class getPatistate(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            con.commit()
            con.close()
            steps = []
            for row in resList:
                step = {column_names[i]: row[i] for i in range(len(column_names))}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class getListorymeeting(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_Meeting order by id desc"
            cur.execute(sql)
            resList = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            con.commit()
            con.close()
            steps = []
            for row in resList:
                step = {column_names[i]: str(row[i]) for i in range(len(column_names))}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


# 获取最近的一次会议信息
class getCurrentmeeting(Resource):
    def get(self):

        return "get ok"

    def post(self):
        # ctx = _request_ctx_stack.top.copy()
        # new_request = ctx.request
        # dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select TOP 1 Theme,Date,Hoster,id,pati,url,link,number from M_Meeting order by id desc "
            cur.execute(sql)
            resList = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            con.commit()
            con.close()
            steps = []
            for row in resList:
                step = {column_names[i]: str(row[i]) for i in range(len(column_names))}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class sendEmailAll(Resource):
    def get(self):

        return "get ok"

    def post(self):
        try:
            sendAll()
        except Exception as e:
            raise e
        response = {
            'success': 1,
        }

        return response


class getmeetinginfobytheme(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        # print(dic)
        theme = dic['theme']
        print(theme)
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_Meeting where theme = '" + theme + "' order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (Theme, Date, Hoster, id, pati, url, score, summary, chapter1, chapter2, chapter3, chapter4, chapter5,
                 chapter6, engagement, sentiment, reason1, reason2, reason3, tips, highlight1, highlight1url,
                 highlight2, highlight2url, highlight3, highlight3url, link, number) in resList:
                step = {"id": id, "theme": Theme, "date": str(Date), "hoster": Hoster, "pati": str(pati),
                        "url": str(url), "score": str(score), "summary": str(summary), "chapter1": str(chapter1),
                        "chapter2": str(chapter2), "chapter3": str(chapter3), "chapter4": str(chapter4),
                        "chapter5": str(chapter5), "chapter6": str(chapter6), "engagement": str(engagement),
                        "sentiment": str(sentiment), "reason1": str(reason1), "reason2": str(reason2),
                        "reason3": str(reason3), "tips": str(tips), "highlight1": str(highlight1),
                        "highlight1url": str(highlight1url), "highlight2": str(highlight2),
                        "highlight2url": str(highlight2url), "highlight3": str(highlight3),
                        "highlight3url": str(highlight3url)}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class getMeetingProcessData(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        meetingid = dic['meetingid']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_MeetingProcess where meetingid = '" + str(meetingid) + "' order by id asc "
            cur.execute(sql)
            resList = cur.fetchall()
            print(resList)
            column_names = [desc[0] for desc in cur.description]
            con.commit()
            con.close()
            steps = []
            for row in resList:
                step = {}
                for i in range(len(column_names)):
                    # 检查每个字段，如果是datetime类型，则转换为字符串
                    if isinstance(row[i], datetime):
                        step[column_names[i]] = row[i].strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        step[column_names[i]] = row[i]
                steps.append(step)
        except Exception as e:
            raise e
        response = {
            'reslist': steps,
        }

        return response


class getMyProcessData(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        meetingid = dic['meetingid']
        people = dic['people']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = """
            SELECT * FROM M_MeetingProcess 
            WHERE meetingid = %s AND people = %s 
            ORDER BY id ASC
            """
            cur.execute(sql, (meetingid, people))
            resList = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            result = [dict(zip(column_names, row)) for row in resList]
            print(result)
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            'reslist': result,
        }
        return response


class setMyProcessData(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic['id']
        isaccept = dic['isaccept']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            # 构建参数化的 SQL 语句
            sql = """
            UPDATE M_MeetingProcess
            SET participation = %s
            WHERE id = %s;
            """
            # 执行 SQL 语句
            cur.execute(sql, (isaccept, id))
            con.commit()
            con.close()
        except Exception as e:
            raise e
        response = {
            'reslist': 1,
        }
        return response


class login(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        username = dic['userName']
        pd = dic['password']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select pd,role from M_paticipater where name = '" + username + "'"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()

            print(resList)

        except Exception as e:
            raise e
        # 不存在
        if len(resList) == 0:
            response = {
                'mess': "用户不存在",
            }
        else:
            rowAsList = [x for x in resList[0]]
            if rowAsList[0] == pd:
                response = {
                    'mess': "登录成功",
                }
            else:
                response = {
                    'mess': "密码错误",
                }
        return response


# class getSpeaker(Resource):
#     def get(self):
#
#         return "get ok"
#
#     def post(self):
#         ctx = _request_ctx_stack.top.copy()
#         new_request = ctx.request
#         dic = json.loads(new_request.data.decode('utf-8'))
#         print(dic)
#         file_path=dic['pathfile']
#         try:
#             jsonres = getSpeakers(file_path)
#
#         except Exception as e:
#             raise e
#         # 不存在
#         return jsonres


class getCurrAndNextHost(Resource):  # 获得下一个主持人
    def get(self):
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_hosts"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
        except Exception as e:
            raise e
        print(resList)
        response = {
            'reslist': resList,
        }

        return response


class addHost(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        id = dic['id']
        name = dic['name']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "select * from M_hosts"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            print(resList)
        except Exception as e:
            raise e
        print(resList)
        response = {
            'reslist': resList,
        }

        return response


class getQuestionnaire(Resource):
    def post(self):
        ctx = _request_ctx_stack.top.copy()
        request_data = json.loads(ctx.request.data.decode('utf-8'))
        meeting_id = request_data['meeting_id']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor(as_dict=True)
            cur.execute("SELECT * FROM dbo.M_Questionnaire WHERE meeting_id = %s", (meeting_id,))
            questions = cur.fetchall()
            con.close()
        except Exception as e:
            raise e

        return {"questions": questions}

class addQuestion(Resource):
    def post(self):
        ctx = _request_ctx_stack.top.copy()
        request_data = json.loads(ctx.request.data.decode('utf-8'))
        meeting_id = request_data['meeting_id']
        question_text = request_data['question_text']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            cur.execute("INSERT INTO dbo.M_Questionnaire (meeting_id, question_text) VALUES (%s, %s)", (meeting_id, question_text))
            con.commit()
            con.close()
        except Exception as e:
            raise e

        return {"success": 1}

class updateQuestion(Resource):
    def post(self):
        ctx = _request_ctx_stack.top.copy()
        request_data = json.loads(ctx.request.data.decode('utf-8'))
        question_id = request_data['question_id']
        question_text = request_data['question_text']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            cur.execute("UPDATE dbo.M_Questionnaire SET question_text = %s WHERE question_id = %s", (question_text, question_id))
            con.commit()
            con.close()
        except Exception as e:
            raise e

        return {"success": 1}

class delQuestion(Resource):
    def post(self):
        ctx = _request_ctx_stack.top.copy()
        request_data = json.loads(ctx.request.data.decode('utf-8'))
        question_id = request_data['question_id']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            cur.execute("DELETE FROM dbo.M_Questionnaire WHERE question_id = %s", (question_id,))
            con.commit()
            con.close()
        except Exception as e:
            raise e

        return {"success": 1}

class addAnswer(Resource):
    def post(self):
        ctx = _request_ctx_stack.top.copy()
        request_data = json.loads(ctx.request.data.decode('utf-8'))

        meeting_id = request_data['answerInfo']['meeting_id']
        paticipater_id = request_data['answerInfo']['paticipater_id']
        process_id = request_data['answerInfo']['process_id']

        answerData = request_data['answerData']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "INSERT INTO dbo.M_answer (question_id, meeting_id,paticipater_id,process_id,answer) VALUES (%s, %s, %s, %s, %s)"
            for answer in answerData:
                cur.execute(sql, (answer['question_id'], meeting_id,paticipater_id,process_id,answer['answer']))
            con.commit()
            con.close()
        except Exception as e:
            raise e

        return {"success": 1}

api.add_resource(sendEmailAll, '/sendEmailAll')
api.add_resource(getName, '/getName')
api.add_resource(getUserInfo, '/getUserInfo')
api.add_resource(getId, '/getId')
api.add_resource(getListorymeeting, '/getListorymeeting')
api.add_resource(getPatistate, '/getPatistate')
api.add_resource(getPati, '/getPati')
api.add_resource(setOnePati, '/setOnePati')
api.add_resource(newpati, '/newpati')
api.add_resource(newmeeting, '/newmeeting')
api.add_resource(invitePati, '/invitePati')
api.add_resource(getCurrentmeeting, '/getCurrentmeeting')
api.add_resource(updateProcess, '/updateProcess')
api.add_resource(newProcess, '/newProcess')
api.add_resource(delProcess, '/delProcess')
api.add_resource(getMeetingProcessData, '/getMeetingProcessData')
api.add_resource(getMyProcessData, '/getMyProcessData')
api.add_resource(setMyProcessData, '/setMyProcessData')
api.add_resource(getCurrAndNextHost, '/getCurrAndNextHost')
api.add_resource(addHost, '/addHost')

api.add_resource(getQuestionnaire, '/getQuestionnaire')
api.add_resource(addQuestion, '/addQuestion')
api.add_resource(updateQuestion, '/updateQuestion')
api.add_resource(delQuestion, '/delQuestion')

api.add_resource(addAnswer, '/addAnswer')

api.add_resource(getonlineid, '/getonlineid')
api.add_resource(action, '/getActionById')
api.add_resource(conscore, '/getConscoreById')
api.add_resource(emotion, '/getEmotionById')
api.add_resource(getmeetinginfobytheme, '/getmeetinginfobytheme')
api.add_resource(login, '/login')
# api.add_resource(getSpeaker,'/getSpeaker')
#
# if __name__== '__main__':
#     app.run()
if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0',port=5000 , threaded = False,processes=5)
    app.debug = False
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app)
    server.serve_forever()
