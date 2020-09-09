from flask_restful import Resource
from flask import request, jsonify
from passlib.hash import sha256_crypt
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='pns02089',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


class LoginUser(Resource):
    def get(self):
        from main import usertoken
        id = request.args.get('id')
        id = int(id)
        password = request.args.get('pw')
        print(id, password)
        try:
            if id and password:
                sql = "SELECT 비밀번호, 이름 FROM 환자 WHERE 환자번호 = '%d'" % (id)
                cursor.execute(sql)
                result = cursor.fetchall()
                if len(result) > 0:
                    if sha256_crypt.verify(password, result[0]['비밀번호']):
                        print(str(id)+password)
                        usertoken[id] = sha256_crypt.hash(str(id) + password)
                        name = result[0]['이름']
                        return {"result": "success", "name": name, "id": id, "token": "%s" % (usertoken[id])}
                    else:
                        return {"result": "no", "msg": "비밀번호가 틀렸습니다."}
                else:
                    return {"result": "no", "msg": "존재하지 않는 아이디입니다."}
            else:
                return {"result": "no", "msg": "아이디 및 비밀번호를 입력해 주세요."}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}


class LoginStaff(Resource):
    def get(self):
        from main import stafftoken
        id = request.args.get('id')
        id = int(id)
        password = request.args.get('pw')

        try:
            if id and password:
                sql = "SELECT 비밀번호, 이름 FROM 직원 WHERE 직원번호 = '%d'" % (id)
                cursor.execute(sql)
                result = cursor.fetchall()

                if len(result) > 0:
                    if sha256_crypt.verify(password, result[0]['비밀번호']):
                        stafftoken[id] = sha256_crypt.hash(str(id)+password)
                        name = result[0]['이름']
                        return {"result": "success", "name": name, "id": id, "token": "%s" % (stafftoken[id])}
                    else:
                        return {"result": "no", "msg": "비밀번호가 틀렸습니다."}
                else:
                    return {"result": "no", "msg": "존재하지 않는 아이디입니다."}
            else:
                return {"result": "no", "msg": "아이디 및 비밀번호를 입력해 주세요."}

        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}
