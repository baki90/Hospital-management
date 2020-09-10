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


class Users(Resource):
    def get(self):
        try:
            token = request.args.get('token')
            from main import stafftoken
            if token in stafftoken.values():
                sql = "SELECT P.건강보험증번호, P.내원경로, P.이름, P.이메일, P.전화번호, P.주민등록번호, P.주치의번호, P.환자번호, E.이름 as 의사이름 FROM 환자 P, 직원 E WHERE E.직원번호 = P.주치의번호"
                cursor.execute(sql)
                result = cursor.fetchall()
                return {"result": result}
            else:
                return {"result": "no", "msg": "권한이 없습니다."}

        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}


class UsersById(Resource):
    def get(self, id):
        try:
            id = int(id)
            print(id)
            token = request.args.get('token')
            from main import stafftoken, usertoken
            if token in stafftoken.values():
                sql = "SELECT P.건강보험증번호, P.내원경로, P.이름, P.이메일, P.전화번호, P.주민등록번호, P.주치의번호, P.환자번호, E.이름 as 의사이름 FROM 환자 P, 직원 E WHERE E.직원번호 = P.주치의번호 AND 환자번호 = '%d'" % (id)
                cursor.execute(sql)
                result = cursor.fetchall()
                return result[0]
            elif id in usertoken.keys():
                if usertoken[id] == token:
                    sql = "SELECT P.건강보험증번호, P.내원경로, P.이름, P.이메일, P.전화번호, P.주민등록번호, P.주치의번호, P.환자번호, E.이름 as 의사이름 FROM 환자 P, 직원 E WHERE E.직원번호 = P.주치의번호 AND 환자번호 = '%d'" % (id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result[0]
                else:
                    return {"result": "no", "msg": "권한이 없습니다."}
            else:
                return {"result": "no", "msg": "권한이 없습니다."}

        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}
