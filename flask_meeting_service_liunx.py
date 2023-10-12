import pyodbc
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask.ctx import _request_ctx_stack
from flask_restful import Api, Resource
from send_email_all import *
import json
from datetime import *
from gevent import pywsgi


app = Flask(__name__)
api = Api(app)
CORS(app, resources=r'/*')


database = 'CN_FstHMST_CyberTA'
host = '47.103.13.21'
user = 'sa'
password = 'chenniao'
conn_info = 'DRIVER={ODBC Driver 17 for SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s'%(database, host, user, password)
# con = pyodbc.connect(conn_info)
# cur = con.cursor()con = pyodbc.connect(conn_info)
# cur = con.cursor()

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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
            con = pyodbc.connect(conn_info)
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
            con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
                con = pyodbc.connect(conn_info)
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
        theme = dic['theme']
        hoster = dic['hoster']
        selectDay = dic['selectDay']
        pati = dic['pati']
        print(pati)
        patistr = ','.join(pati)

        try:
            con = pyodbc.connect(conn_info)
            cur = con.cursor()
            sql = "insert into M_Meeting (theme,hoster,date,pati) values ('" + \
                  theme + "','" + hoster + "','" + str(selectDay) + "','" + patistr + "')"
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
        stuid = dic['stuid']
        role = dic['role']
        ispermanent = dic['ispermanent']

        try:
            con = pyodbc.connect(conn_info)
            cur = con.cursor()
            sql = "insert into M_paticipater (name,stuid,role,ispermanent) values ('" + \
                  name + "','" + stuid + "','" + role + "','" + ispermanent + "')"
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
            con = pyodbc.connect(conn_info)
            cur = con.cursor()
            sql ="select * from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (name, stuid,role,ispermanent,id) in resList:
                step = {"id": int(id), "name": name}
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
            con = pyodbc.connect(conn_info)
            cur = con.cursor()
            sql ="select * from M_paticipater order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (name, stuid,role,ispermanent,id) in resList:
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
            con = pyodbc.connect(conn_info)
            cur = con.cursor()
            sql ="select * from M_Meeting order by id asc"
            cur.execute(sql)
            resList = cur.fetchall()
            con.commit()
            con.close()
            steps = []
            for (Theme, Date,Hoster,id,pati) in resList:
                step = {"id": id, "theme": Theme, "date": str(Date), "hoster": Hoster, "pati": str(pati)}
                steps.append(step)
            print(steps)
        except Exception as e:
            raise e
        response = {
            'reslist':steps,
        }

        return response

class sendEmailByName(Resource):
    def get(self):

        return "get ok"

    def post(self):
        ctx = _request_ctx_stack.top.copy()
        new_request = ctx.request
        dic = json.loads(new_request.data.decode('utf-8'))
        print(dic)
        namelist = dic['namelist']
        print(namelist)
        try:
            sendByName(namelist)
        except Exception as e:
            raise e
        response = {
            'success':1,
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


api.add_resource(sendEmailByName,'/sendEmailByName')
api.add_resource(sendEmailAll,'/sendEmailAll')
api.add_resource(getName,'/getName')
api.add_resource(getId,'/getId')
api.add_resource(getListorymeeting,'/getListorymeeting')
api.add_resource(getPatistate,'/getPatistate')
api.add_resource(getPati, '/getPati')
api.add_resource(newpati, '/newpati')
api.add_resource(newmeeting, '/newmeeting')


api.add_resource(getonlineid, '/getonlineid')
api.add_resource(action, '/getActionById')
api.add_resource(conscore, '/getConscoreById')
api.add_resource(emotion, '/getEmotionById')
#
# if __name__== '__main__':
#     app.run()
if __name__ == '__main__':
    # app.run(debug=False, host='0.0.0.0',port=5000 , threaded = False,processes=5)
    app.debug = False
    server = pywsgi.WSGIServer(('0.0.0.0', 8081), app)
    server.serve_forever()
