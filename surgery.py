from flask_restful import Resource
from flask import request
import pymysql
from utils import *

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

class Surgery(Resource):
  def post(self):
        json = request.get_json()

        doctor = json['doctor']
        name = json['name']
        starttime = json['starttime']
        endtime = json['endtime']
        uid = json['uid']
        dtime = json['dtime']

        if doctor is None or starttime is None or uid is None or name is None:
            return {"result": "no", "msg": "필요 정보가 없습니다."}
        else:
            uid = int(uid)
            doctor = int(uid)
            sql = "INSERT INTO 수술 (수술명, 수술시작일시, 수술예상종료일시, 집도의번호, 환자번호, 진료일시) VALUES ('%s', '%s', '%s', %d, %d, '%s')"%(name, starttime,endtime, int(doctor),int(uid),dtime)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return {"result": "success"}

class SurgeryById(Resource):
  def get(self, sid):
    try:
        sid = int(sid)
        if sid > 10000 and sid < 20000:
            beforesql = "SELECT * from 수술 where 집도의번호 = '%d' and 수술예상종료일시 < NOW() ORDER BY 수술시작일시 DESC" %(sid)
            nowsql = "SELECT * from 수술 where 집도의번호 = '%d' and 수술시작일시 < NOW() and 수술예상종료일시 > NOW()" %(sid)
            aftersql = "SELECT * from 수술 where 집도의번호 = '%d' and 수술예상종료일시 > NOW() ORDER BY 수술시작일시 ASC" %(sid)

            cursor.execute(beforesql)
            before = cursor.fetchall()
            cursor.execute(nowsql)
            now = cursor.fetchall()
            cursor.execute(aftersql)
            after = cursor.fetchall()

            before = serializeDatetime(before)
            after = serializeDatetime(now)
            now = serializeDatetime(after)

            return {"result": "success", "before": before, "now": now, "after": after}
        else:
            return {"result": "no", "msg": "의사가 아닙니다."}
    except Exception as e:
        print(e)
        return {"result": "no", "msg": e}
