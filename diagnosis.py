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


class Diagnosis(Resource):
    def get(self):
        from main import usertoken, stafftoken
        try:
            token = request.args.get('token')
            uid = request.args.get('uid')
            diagAt = request.args.get('diagAt')

            if uid is None:  # uid, diagAt 값이 없는 경우
                if token in stafftoken.values():
                    sql = "SELECT D.*, H.수술시작일시, H.수술명, K.이름 FROM (SELECT * FROM 직원 WHERE 직원종류=1) AS K, (SELECT * FROM 진료 ORDER BY 진료일시 DESC LIMIT 30) AS D LEFT JOIN 수술 AS H ON D.환자번호= H.환자번호 AND D.진료일시 = H.진료일시 WHERE K.직원번호 = D.의사번호"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    result = serializeDatetime(result)
                    return {"result": result}
                else:
                    return {"result": "no", "msg": "권한이 없습니다."}
            else:
                uid = int(uid)
                if (isUser(token) and uid == getUID(token)) or isStaff(token):
                    if diagAt is None: 
                        sql = "SELECT D.*, H.수술시작일시, H.수술명, K.이름 FROM (SELECT * FROM 직원 WHERE 직원종류=1) AS K, (SELECT * FROM 진료 WHERE 환자번호 = '%d' ORDER BY 진료일시 DESC LIMIT 30) AS D LEFT JOIN 수술 AS H ON D.환자번호= H.환자번호 AND D.진료일시 = H.진료일시 WHERE K.직원번호 = D.의사번호" % (uid)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        result = serializeDatetime(result)
                        return {"result": result}
                    else:
                        sql = "SELECT * FROM 진료 WHERE 환자번호 = '%d' AND 진료일시 = '%s'" % (
                            uid, diagAt)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        result = serializeDatetime(result)
                        return {"result": result}
                else:
                    return {"result": "no", "msg": "권한이 없습니다."}

        except Exception as e:
            return {"result": "no", "msg": e}

    def post(self):
        try:
            json = request.get_json()
            print(json)
            name = json['name']
            datetime = json['datetime']
            doctor = json['doctor']
            user = json['user']
            text = json['text']

            if doctor is None or name is None or datetime is None or user is None or text is None:
                return {"result": "no", "msg": "필요 정보가 없습니다."}
            else:
                doctor = int(doctor)
                user = int(user)
            
                sql = "INSERT INTO 진료 (진단명, 진료일시, 의사번호, 환자번호, 진료소견) VALUES ('%s', '%s', %d, %d, '%s')"%(name, datetime, doctor, user,text)
                print(sql)
                cursor.execute(sql)
                conn.commit()
                return {"result": "success"}
        
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}



