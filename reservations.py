from flask_restful import Resource
from flask import request
from utils import *
import pymysql
from datetime import datetime 
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='gamja',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


class Reservations(Resource):
    def get(self):
        from main import usertoken, stafftoken
        token = request.args.get('token')
        uid = request.args.get('uid')
        sid = request.args.get('sid')
        print(token, uid)
        try:
            if isValidToken(token):
                if uid is None and sid is None: #uid, sid 없이 직원이 전체를 조회하는 경우
                    if isStaff(token):
                        now = datetime.now()
                        time = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
                        sql = "SELECT R.예약번호, R.예약일시, R.신청일시, R.승인여부, R.희망의사번호, E.이름 AS 의사이름, P.이름 AS 환자이름 FROM 예약 R,환자 P, 직원 E WHERE '%s' < R.예약일시 AND R.환자번호 = P.환자번호 AND R.희망의사번호 = E.직원번호 ORDER BY 예약번호 LIMIT 100" %(time)
                        print(sql)
                        cursor.execute(sql)
                        result = list(cursor.fetchall())
                        result = serializeDatetime(result)
                        return {"result": result}
                    else: 
                        return {"result": "no", "msg": "토큰이 유효하지 않습니다."}
                elif sid is None: #uid로 회원의 정보 조회
                    uid = int(uid)
                    if isUser(token):  # 로그인 한 사람이 유저
                        if uid == getUID(token):
                            sql = "SELECT R.예약번호, R.예약일시, R.신청일시, R.승인여부, R.희망의사번호, E.이름 AS 의사이름, P.이름 AS 환자이름 FROM 예약 R,환자 P, 직원 E WHERE R.환자번호 = '%d' AND R.환자번호 = P.환자번호 AND R.희망의사번호 = E.직원번호 ORDER BY 예약번호 LIMIT 100" % (uid)
                            print(sql)
                            cursor.execute(sql)
                            result = list(cursor.fetchall())
                            result = serializeDatetime(result)
                            return {"result": result}
                        else:
                            return {"result": "no", "msg": "자신의 정보만 열람하세요."}    
                    else:  # 직원일때
                        sql = "SELECT R.예약번호, R.예약일시, R.신청일시, R.승인여부, R.희망의사번호, E.이름 AS 의사이름, P.이름 AS 환자이름 FROM 예약 R,환자 P, 직원 E WHERE R.환자번호 = '%d' AND R.환자번호 = P.환자번호 AND R.희망의사번호 = E.직원번호 ORDER BY 예약번호 LIMIT 100" % (uid)
                        print(sql)
                        cursor.execute(sql)
                        result = list(cursor.fetchall())
                        result = serializeDatetime(result)
                        return {"result": result}
                        
                else: #sid로 자신의 진료 기록 조회
                    sid = int(sid)
                    if isStaff(token):
                        now = datetime.now()
                        time = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
                        sql = "SELECT R.예약번호, R.예약일시, R.신청일시, R.승인여부, R.희망의사번호, E.이름 AS 의사이름, P.이름 AS 환자이름 FROM 예약 R,환자 P, 직원 E WHERE E.직원번호 = '%d' AND '%s' < R.예약일시 AND R.환자번호 = P.환자번호 AND R.희망의사번호 = E.직원번호 ORDER BY 예약번호 LIMIT 100" %(sid, time)
                        print(sql)
                        cursor.execute(sql)
                        result = list(cursor.fetchall())
                        result = serializeDatetime(result)
                        return {"result": result}
                    else:
                        return {"result": "no", "msg": "직원 권한이 아닙니다."} 
            else:
                return {"result": "no", "msg": "토큰이 유효하지 않습니다."}
        except Exception as e:
            print(e)
            return {"result": "no", "msg": str(e)}

    def post(self):
        json = request.get_json()
        print(json)
        # TODO : verify
        datetime = json['datetime']
        doctor = int(json['doctor'])
        token = json['token']
        if isValidToken(token):
            uid = getUID(token)
            if(uid):
                try:
                    sql = "INSERT INTO 예약 (예약일시, 승인여부, 희망의사번호, 환자번호) VALUES ('%s', 0, %d, %d)" % (
                        datetime, doctor, uid)
                    print(sql)
                    cursor.execute(sql)
                    conn.commit()
                    return {"result": "success"}
                except Exception as e:
                    print(e)
                    return {"result": "no", "msg": e}

            return {"result": "no", "msg": "유저 정보를 불러올 수 없습니다."}

        return {"result": "no", "msg": "유효하지 않는 토큰입니다."}


class ReservationJudge(Resource):
    def post(self):
        json = request.get_json()
        num = int(json['id'])
        val = int(json['val'])
        token = json['token']
        if isStaff(token):
            try: 
                sql = "UPDATE 예약 SET 승인여부 = '%d' WHERE 예약번호 = '%d'" %(val, num)
                print(sql)
                cursor.execute(sql)
                conn.commit()
                return {"result": "success"}
            except Exception as e:
                    print(e)
                    return {"result": "no", "msg": e}
        else:
            return {"result": "no", "msg": "유효하지 않은 토큰입니다."}
        
