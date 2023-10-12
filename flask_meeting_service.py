import pyodbc
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from flask.ctx import _request_ctx_stack
from flask_restful import Api, Resource
from send_email_all import *
import json
import io
from datetime import *
import base64
import time
from gevent import pywsgi
import pymssql
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
            had = [59,51,53,50,49,58,54]
            nums = []
            for a in had:
                con = pymssql.connect(server=host, user=user, password=password, database=database)
                cur = con.cursor()
                now = datetime.now()
                out_date = (now + timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
                sql ="select count(ID) as times from I_Emotion where StudentId ='" + str(a+1)+"' and Time > '" + out_date + "'"
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
            sql ="select RealName from I_Users where ID ='" + str(id)+"'"
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
            sql ="select ID from I_Users where RealName ='" + str(realname)+"'"
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
                sql = "select top 1 angry,disgusted,fearful,happy,sad,surprised,neutral,Time from I_Emotion where StudentId = '" + str(id+1) + "'order by id desc"
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
                sql ="select top 1 EatDrink,sleep,Phone,Rehand,Calling,Study,Time from I_Action where StudentId = '" + str(id+1) + "'order by id desc"
                cur.execute(sql)
                resList = cur.fetchall()
                con.commit()
                con.close()
                rowAsList = [x for x in resList[0]]
                response = {
                    'success' : 1,
                    'eatdrink': rowAsList[0],
                    'sleep': rowAsList[1],
                    'phone1': rowAsList[2],
                    'rehand': rowAsList[3],
                    'calling': rowAsList[4],
                    'study': rowAsList[5],
                    'time': str(rowAsList[6])
                }
            else :
                response = {
                    'success' : 0,
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
                sql ="select top 1 conScore,Time from I_Concentration where StudentId = '" + str(id + 1) + "'order by id desc"
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
            else :
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

        # pati = dic['pati']

        # data = request.files
        # print("start...")
        # print(type(data))
        # file = data['file']
        # print(file.filename)
        # print(request.headers)
        # # 文件写入磁盘
        # file.save(file.filename)
        # print("end...")

        # print(pati)
        # patistr = ','.join(pati)

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "insert into M_Meeting (theme,hoster,date,link,number) values ('" + \
                  theme + "','" + hoster + "','" + str(selectDay) + "','" + link + "','" +number +"')"
            cur.execute(sql)
            con.commit()
            con.close()
            # rowAsList = [x for x in resList[0]]
            # print(resList)
            # print(rowAsList)
            # sendInvite(pati, "http://124.222.217.145:8082/login",theme,hoster,str(selectDay))
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
        # data = request.files
        # print("start...")
        # print(type(data))
        # file = data['file']
        # print(file.filename)
        # print(request.headers)
        # # 文件写入磁盘
        # file.save(file.filename)
        # print("end...")

        # print(pati)
        # patistr = ','.join(pati)
        #
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
            # 在resList中查找匹配的email
            for result in resList:
                if name == result[0]:
                    email = result[1]
                    name_email_dict[name] = email
                    break  # 找到匹配的email后，可以跳出内层循环，继续处理下一个name
        print(name_email_dict)
        meeting = getCurrentmeeting.post(self)['reslist'][0]
        theme = meeting['theme']
        hoster = meeting['hoster']
        date = meeting['date'].split(' ')[0]
        link = meeting['link']
        number = meeting['number']
        sendInvite(name_email_dict, "http://124.222.217.145:8082",theme,hoster,date,link,number)

        # 打印name和email对应关系

        response = {
            "success": 1,
        }

        # return response
        # return "ok"
class newProcess(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        curmeeting = dic['curmeeting']
        topicName = dic['topicName']
        time = dic['time']
        people = dic['people']
        role = dic['role']

        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "insert into M_MeetingProcess (curmeeting,topicName,time,people,role) values ('" + \
                  curmeeting + "','" + topicName + "','" + time + "','" + people +"','" +role+ "')"
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
        # ispermanent = dic['ispermanent']
        #
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql = "insert into M_paticipater (name,role,email,remark) values ('" + \
                  name + "','" + role + "','" + email + "','" + remark + "')"
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
            sql ="select * from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (name, stuid,role,ispermanent,id,pd,email,remark) in resList:
                step = {"id": int(id), "name": name, "role": role}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
            sql ="select * from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (name, stuid,role,ispermanent,id,pd) in resList:
                step = {"id": int(id), "name": name, "stuid": int(stuid), "role": role, "ispermanent": int(ispermanent)}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
            sql ="select Theme,Date,Hoster,id,pati,url from M_Meeting order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (Theme, Date,Hoster,id,pati,url) in resList:
                step = {"id": id, "theme": Theme, "date": str(Date), "hoster": Hoster, "pati": str(pati), "url" : str(url)}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
            sql ="select TOP 1 Theme,Date,Hoster,id,pati,url,link,number from M_Meeting order by id desc "
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (Theme, Date,Hoster,id,pati,url,link,number) in resList:
                step = {"id": id, "theme": Theme, "date": str(Date), "hoster": Hoster, "pati": str(pati), "url" : str(url), "link" : str(link), "number" : str(number)}
                steps.append(step)
            # print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
            'success':1,
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
            sql ="select * from M_Meeting where theme = '" + theme + "' order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (Theme, Date,Hoster,id,pati,url,score,summary,chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,engagement,sentiment,reason1,reason2,reason3,tips,highlight1,highlight1url,highlight2,highlight2url,highlight3,highlight3url,link,number) in resList:
                step = {"id": id, "theme": Theme, "date": str(Date), "hoster": Hoster, "pati": str(pati), "url" : str(url), "score": str(score), "summary": str(summary), "chapter1": str(chapter1), "chapter2": str(chapter2), "chapter3": str(chapter3), "chapter4": str(chapter4), "chapter5": str(chapter5), "chapter6": str(chapter6), "engagement": str(engagement), "sentiment": str(sentiment), "reason1": str(reason1), "reason2": str(reason2), "reason3": str(reason3), "tips": str(tips), "highlight1": str(highlight1), "highlight1url": str(highlight1url), "highlight2": str(highlight2), "highlight2url": str(highlight2url), "highlight3": str(highlight3), "highlight3url": str(highlight3url)}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
        meeting = dic['curmeeting']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql ="select * from M_MeetingProcess where curmeeting = '" + meeting + "' "
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (curmeeting, topicName,time,people,role) in resList:
                step = {"topicName": topicName,"time":time,"people":people,"role":role}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
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
        username=dic['userName']
        pd=dic['password']
        try:
            con = pymssql.connect(server=host, user=user, password=password, database=database)
            cur = con.cursor()
            sql ="select pd from M_paticipater where name = '" + username + "'"
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
    

class getSpeaker(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        file_path=dic['pathfile']
        try:
            jsonres = getSpeakers(file_path)

        except Exception as e:
            raise e
        # 不存在
        return jsonres



api.add_resource(sendEmailAll,'/sendEmailAll')
api.add_resource(getName,'/getName')
api.add_resource(getId,'/getId')
api.add_resource(getListorymeeting,'/getListorymeeting')
api.add_resource(getPatistate,'/getPatistate')
api.add_resource(getPati, '/getPati')
api.add_resource(newpati, '/newpati')
api.add_resource(newmeeting, '/newmeeting')
api.add_resource(invitePati, '/invitePati')
api.add_resource(getCurrentmeeting,'/getCurrentmeeting')
api.add_resource(newProcess,'/newProcess')
api.add_resource(getMeetingProcessData,'/getMeetingProcessData')


api.add_resource(getonlineid, '/getonlineid')
api.add_resource(action, '/getActionById')
api.add_resource(conscore, '/getConscoreById')
api.add_resource(emotion, '/getEmotionById')
api.add_resource(getmeetinginfobytheme,'/getmeetinginfobytheme')
api.add_resource(login,'/login')
api.add_resource(getSpeaker,'/getSpeaker')
#
# if __name__== '__main__':
#     app.run()
if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0',port=5000 , threaded = False,processes=5)
    app.debug = False
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app)
    server.serve_forever()
