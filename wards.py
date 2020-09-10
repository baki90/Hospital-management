from flask_restful import Resource
from flask import request
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

class Wards(Resource):
  def get(self):
    try:
        sql = "SELECT * FROM 병동"
        sql2 = "SELECT COUNT(*) AS 수용병상, A.병동번호 FROM 병상 A WHERE NOT EXISTS (SELECT * FROM (SELECT * FROM `입원` WHERE (입원일시 <= NOW() AND 퇴원예정일시 >=NOW()) OR 퇴원예정일시 IS NULL ) AS B WHERE A.병상번호 = B.병상번호 AND A.병실번호 = B.병실번호 AND A.병동번호 = B.병동번호) GROUP BY A.병동번호"

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.execute(sql2)
        result2 = cursor.fetchall()

        return {"result": result , "num": result2}
    except Exception as e:
        print(e)
        return {"result": "no", "msg": e}

class Rooms(Resource):
    def get(self, wid):
        try:
            print("hello1")
            sql = "SELECT * FROM 병실 WHERE 병동번호 = '%d'" %(int(wid))       
            sql2 = "SELECT COUNT(*) AS 수용병상, A.병동번호, A.병실번호 FROM (SELECT * FROM 병상 WHERE 병동번호= '%d') A WHERE NOT EXISTS (SELECT * FROM (SELECT * FROM `입원` WHERE (입원일시 <= NOW() AND 퇴원예정일시 >=NOW()) OR 퇴원예정일시 IS NULL ) AS B WHERE A.병상번호 = B.병상번호 AND A.병실번호 = B.병실번호 AND A.병동번호 = B.병동번호) GROUP BY A.병동번호, A.병실번호"%(int(wid))
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            return {"result": result , "num": result2}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}

class Sickbeds(Resource):
    def get(self, wid, rid):
        try:
            sql = "SELECT COUNT(*) AS 수용병상, A.병동번호, A.병실번호, A.병상번호 FROM (SELECT * FROM 병상 WHERE 병동번호= '%d' AND 병실번호 = '%d') A WHERE NOT EXISTS (SELECT * FROM (SELECT * FROM `입원` WHERE (입원일시 <= NOW() AND 퇴원예정일시 >=NOW()) OR 퇴원예정일시 IS NULL ) AS B WHERE A.병상번호 = B.병상번호 AND A.병실번호 = B.병실번호 AND A.병동번호 = B.병동번호) GROUP BY A.병동번호, A.병실번호, A.병상번호" %(int(wid), int(rid))       
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()

            return {"result": result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}
            
