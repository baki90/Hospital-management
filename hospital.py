from flask_restful import Resource
from flask import request
import pymysql
from utils import *

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='pns02089',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

class Hospital(Resource):
    def post(self):
        json = request.get_json()

        starttime = json['starttime'] #입원일시
        endtime = json['endtime'] #퇴원예정
        ward = json['ward'] #병동
        room = json['room'] #병실
        bed = json['bed'] #병상
        uid = json['uid'] #환자번호

        uid = int(uid)
        bed = int(bed)
        room = int(room)
        ward = int(ward)

        sql = "INSERT INTO 입원 (입원일시, 퇴원예정일시, 병상번호, 병실번호, 병동번호, 환자번호) VALUES ('%s', '%s', %d, %d, %d, %d)"%(starttime,endtime, bed, room, ward, uid)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        return {"result": "success"}
        

class HospitalById(Resource):
    def get(self, id):
        try:
            id = int(id)
            sql = "SELECT J.환자번호,J.진단명, N.병동번호, N.병실번호, N.병상번호, N.입원일시, DATEDIFF(NOW(), N.입원일시) AS 입원기간 FROM (SELECT *, (SELECT MAX(D.진료일시) FROM 진료 D WHERE H.환자번호 = D.환자번호 AND H.입원일시 > D.진료일시) AS 진료날 FROM 입원 H NATURAL JOIN (SELECT * FROM 환자 WHERE 환자번호 = '%d') P ) AS N JOIN 진료 J ON N.진료날 = J.진료일시 AND N.환자번호 = J.환자번호" %(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            result = serializeDatetime(result)
            return {"result" : result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}

class HospitalByNow(Resource):
    def get(self):
        try:
            sql = "SELECT P.이름, P.환자번호, H.병동번호, H.병실번호, H.병상번호, DATEDIFF(NOW(), H.입원일시) AS 입원기간  FROM `입원` AS H, `환자` AS P WHERE ((입원일시 <= NOW() AND 퇴원예정일시 >=NOW()) OR 퇴원예정일시 IS NULL) AND P.환자번호 = H.환자번호 ORDER BY 병동번호, 병실번호, 병상번호 ASC"
            cursor.execute(sql)
            result = cursor.fetchall()
            result = serializeDatetime(result)
            return {"result" : result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}