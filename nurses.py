from flask_restful import Resource
from flask import request
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='pns02089',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


class Nurses(Resource):
    def get(self):
        try:
            sql = "SELECT D.부서이름, E.직원번호, 이름, 성별, 전화번호, 직급, 이메일, 직원종류 FROM 직원 AS E, 부서 AS D WHERE E.부서번호 = D.부서번호 AND E.직원종류 = 2"
            cursor.execute(sql)
            result = cursor.fetchall()
            return {"result": result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}


class NursesById(Resource):
    def get(self, id):
        try:
            sql = "SELECT D.부서이름, E.직원번호, 이름, 성별, 전화번호, 직급, 이메일, 직원종류 FROM 직원 AS E, 부서 AS D WHERE E.부서번호 = D.부서번호 AND E.직원종류 = 2 AND E.직원번호 = '%d'" % int(
                id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return result[0]
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}
