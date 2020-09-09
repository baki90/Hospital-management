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


class Departments(Resource):
    def get(self):
        try:
            sql = "SELECT *, 직원.이름 as 부서장이름 FROM 부서, 직원 WHERE 직원.직원번호 = 부서.직원번호"
            cursor.execute(sql)
            result = cursor.fetchall()
            return {"result": result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": str(e)}


class DepartmentsById(Resource):
    def get(self, id):
        try:
            sql = "SELECT * FROM 직원 WHERE 부서번호 = '%d'" % int(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return {"result": result}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": str(e)}
