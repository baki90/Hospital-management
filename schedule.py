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

#id, time, token
class Schedules(Resource):
    def get(self):
        try:
            id = request.args.get('id')
            time = request.args.get('time')
            if id is None:
                sql = "SELECT * FROM (SELECT 직원번호, 이름, 부서번호 FROM 직원 WHERE 직원종류 = 1) AS A WHERE NOT EXISTS (SELECT * FROM ((SELECT 집도의번호 as 의사번호 FROM 수술 WHERE 수술시작일시 > NOW() AND 수술예상종료일시 < NOW()) UNION (SELECT R.희망의사번호 FROM (SELECT * FROM 예약 WHERE 승인여부 = 1) AS R WHERE R.예약일시 <= NOW() AND DATE_ADD(R.예약일시, INTERVAL 10 MINUTE) > NOW())) AS B WHERE A.직원번호 = B.의사번호)"
                cursor.execute(sql)
                result = cursor.fetchall()
                return {"result": result}
            else:
                if time is None:
                    sql = "SELECT * FROM (SELECT 직원번호, 이름, 부서번호 FROM 직원 WHERE 직원번호 = '%d' AND 직원종류 = 1) AS A WHERE NOT EXISTS (SELECT * FROM ((SELECT 집도의번호 as 의사번호 FROM 수술 WHERE 수술시작일시 > NOW() AND 수술예상종료일시 < NOW()) UNION (SELECT R.희망의사번호 FROM (SELECT * FROM 예약 WHERE 승인여부 = 1) AS R WHERE R.예약일시 <= NOW() AND DATE_ADD(R.예약일시, INTERVAL 10 MINUTE) > NOW())) AS B WHERE A.직원번호 = B.의사번호)" % (int(id))
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if(len(result) > 0):
                        return {"result": result[0]}
                    else: 
                        return {"result": "no"}  
                else:
                    sql = "SELECT * FROM (SELECT 직원번호, 이름, 부서번호 FROM 직원 WHERE 직원번호 = '%d' AND 직원종류 = 1) AS A WHERE NOT EXISTS (SELECT * FROM ((SELECT 집도의번호 as 의사번호 FROM 수술 WHERE 수술시작일시 > NOW() AND 수술예상종료일시 < '%s') UNION (SELECT R.희망의사번호 FROM (SELECT * FROM 예약 WHERE 승인여부 = 1) AS R WHERE R.예약일시 <= NOW() AND DATE_ADD(R.예약일시, INTERVAL 10 MINUTE) > '%s')) AS B WHERE A.직원번호 = B.의사번호)" % (int(id), time, time)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if(len(result) > 0):
                        return {"result": result[0]}
                    else:
                        return {"result": "no"}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": e}

