# 내 생각 -> 진료 데이터를 먼저 만들고 거기에 대해서 예약 데이터를 만들면 괜찮을 거 같음
from datetime import datetime, timedelta
import time
from random import randrange
import random
import pymysql

def get_random_datetime(from_s, to_s):
    from_d = s_t_d(from_s)
    to_d = s_t_d(to_s)
    from_t = d_t_t(from_d)
    to_t = d_t_t(to_d)
    r_t = randrange(from_t, to_t)
    r_d = t_t_d(r_t)
    # 분, 초단위 생략 replace는 datetime 객체를 바꾼다.
    r_d = r_d.replace(minute=int(r_d.minute/10)*10, second=0)
    return r_d


def s_t_d(str):  # str -> datetime
    return datetime.strptime(str, '%Y-%m-%d %H:%M:%S')


def t_t_d(t):  # timestamp -> datetime
    return datetime.fromtimestamp(t)


def d_t_t(d):  # datetime -> timestamp
    return time.mktime(d.timetuple())


def d_t_s(d):  # datetime -> str
    return d.strftime('%Y-%m-%d %H:%M:%S')


print(get_random_datetime('2017-08-01 00:00:00', '2017-08-10 00:00:00'))

conn = pymysql.connect(host = 'localhost', user = 'root', password ='', db='gamja', charset='utf8mb4')
cursor = conn.cursor()


disease = {1: ["만성피로", "관절통", "요통", "전신쇠약", "노화"], 2: ["HIV감염","인플루엔자","풍토병","폐외 결핵","공수병"], 3: ["디스크질환","암성통증","만성통증","복합부위통증증후군",
"만성요통",], 4: ["자궁암","폐암","간암", "방광암","갑상선암"], 5: ["발기부전","요실금","배뇨장애","전립선암","요로결석"
], 6: ["자궁경부암","고위험임신","태아기형","생리불순","폐경"], 7: ["얼굴기형","두경부재건","악안면외상","화상","유방재건"], 8: ["소아 알레르기","아토피","유전 질환","내분비 질환","뇌전증"], 9: ["변비","담석증","간질환","염증성 장질환","과민성장증후군"], 10: ["뇌졸중","말초신경병","치매","근무력증","언어장애"],
11 : ["동맥경화","협심증","심근경색증","허혈성 심질환","고혈압"], 12: ["녹내장","백내장","망막손상","각막손상","안암"], 14: ["치핵", "탈장","대장암","췌장암","당뇨"],
15: ["독극물중독","중증 외상","골절","치아골절","자상"], 16: ["안면마비","평형기관장애","식도암","구강암","후두암"],
17 : ["말초신경손상","인대손상","인대파열","골연골염","탈골"], 18: ["슬관절염","견관절염","족관절염","고관절장애","인공관절손상"], 
19: ["양악수술","턱교정수술","임플란트","안면비대칭","충치치료"], 20: ["늑막질환","기흉","오목가슴","정맥류","기관지염"]}
rann = ["수술", "수술", "수술", "수술", "수술", "수술", "수술", "휴식", "검진", "금주", "규칙적인 생활"]

# 진료 정보 만들기

def 진료정보만들기():
  visit = set()
  for i in range(1, 5000): # 우리 진료정보 한 3000개는 만들자. 일단 졸라 만들고 보는거임.. 겹치는건 지우면됨
      index = randrange(0,5) #임의의 병 번호 선택
      index2 = randrange(0,len(rann))
      num = randrange(30001, 30501) #환자 랜덤 select
      sql = "SELECT E.직원번호, D.부서번호 FROM 직원 E, 환자 P, 부서 D WHERE P.환자번호 = '%d' AND P.주치의번호 = E.직원번호 AND E.부서번호 = D.부서번호" %(num)
      cursor.execute(sql)
      result = cursor.fetchall()
      dep = int(result[0][1]) #해당 주치의의 부서 번호
      if dep == 13:
          continue
      else:
          doc = int(result[0][0]) #해당 환자의 주치의 번호
          now = get_random_datetime('2019-12-15 00:00:00', '2019-12-25 00:00:00')
          now_s = d_t_s(now)

          h = d_t_s(now) + str(num)
          if(h in visit):
            continue
          visit.add(h)

          # 여기서 만약 입원 가능 시간(09:00-15:00) 이 시간일 경우에만 진료소견에 수술이 들어가면 좋겠음
          # 왜냐하면 진료소견에 수술이 있는 정보로 기준으로 나중에 입원을 시키고 싶기 때문에.. 
          # 대신 수술 확률도 좀 증가시키면 좋을 듯

          diag = "%s으(로) 인한 %s이(가) 필요함." % (disease[dep][index], rann[index2])
          nq = "INSERT INTO 진료 (진단명, 진료일시, 의사번호, 환자번호, 진료소견) VALUES('%s', '%s', '%d', '%d', '%s')" % (
              disease[dep][index], now, doc, num, diag)

          cursor.execute(nq)
          conn.commit()

          one_hour_before = now - timedelta(hours = 1)
          nq = "INSERT INTO 예약 (예약일시, 신청일시, 승인여부, 환자번호, 희망의사번호) VALUES('%s', '%s', '%d', '%d', '%s')" % (
              d_t_s(now), d_t_s(one_hour_before), 1, num, doc)

          cursor.execute(nq)
          conn.commit()
          print(i)
          # 나중에 겹쳐서 위의는 집도의의 수술 시간이 안겹치는걸 가정하고 막 넣었기 때문에 분명히 불가능한 수술도 있을꺼임
          # 이때의 경우에는 이거 다음 수술 정보를 넣을때 불가능한 수술에 대한 진료데이터는 없애버리고 
          # 해당 진료일시 - 1시간에 예약한 예약정보의 승인여부는 거절로 해버리면 될거같음)

  #        cursor.execute(nq)
  #        result = cursor.fetchall()
  #        conn.commit()
  #        print(nq)
def 진료중복삭제():
  for 의사번호 in range(10001, 10101):
    #  위의 진료 정보 중 소견이 수술인걸 의사별로 쫙 긁어오고 진료일시별로 오름차순으로 정렬. 
    #  수술 시간은 랜덤으로 randrange(1,30) * 10분으로 해버리자.

    수술시간 = randrange(1,25) * 10
    q = "SELECT 진료일시 FROM 진료, 환자 WHERE 환자.환자번호 = 진료.환자번호 AND 진료.의사번호 = '"+str(의사번호)+"' AND 진료.진료소견 LIKE '%수술%' ORDER BY 진료.진료일시 ASC"
    cursor.execute(q)
    result = list(cursor.fetchall())

    #     그래서 수술시작시간은 = 진료일시 + 우리가 설정한 기본 진료시간(30분정도)*2
    #   수술 예상종료시간은 수술종료시간 = 수술시작시간 + 수술시간

    for r in range(len(result)):
      진료정보 = result[r]
      print(진료정보)
      진료시작 = 진료정보[0] + timedelta(seconds = 1)
      진료종료 = 진료시작 + timedelta(minutes = 10)

      # 겹치는 진료정보는 삭제한다.


      q = "DELETE FROM 진료 WHERE (진료일시 BETWEEN '%s' AND '%s') AND 의사번호 = '%d'" % (d_t_s(진료시작), d_t_s(진료종료), 의사번호)
      cursor.execute(q)
      conn.commit()
def 수술정보추가():
  for 부서 in range(1,21):
    
    for i in range(0,5):
      의사번호 = 10001 + (부서-1)*5+i

      #  위의 진료 정보 중 소견이 수술인걸 의사별로 쫙 긁어오고 진료일시별로 오름차순으로 정렬. 
      #  수술 시간은 랜덤으로 randrange(1,30) * 10분으로 해버리자.

      수술시간 = randrange(1,25) * 10

      q = "SELECT 환자.환자번호, 진료일시, 진단명, 진료소견 FROM 진료, 환자 WHERE 환자.환자번호 = 진료.환자번호 AND 진료.의사번호 = '"+str(의사번호)+"' AND 진료.진료소견 LIKE '%수술%' ORDER BY 진료.진료일시 ASC"
      print(q)
      cursor.execute(q)
      result = cursor.fetchall()

      #   수술 예상종료시간은 수술종료시간 = 수술시작시간 + 수술시간
      

      for r in range(len(result)):

        진료정보 = result[r]
        수술시작시간 = 진료정보[1] + timedelta(minutes=10)
        수술예상종료시간 = 수술시작시간 + timedelta(minutes=수술시간)


        '''
        일단 수술정보로 위의 수술 시작시간~예상 종료시간을 주치의로 검색해가지고 해당 집도의가 집도가 가능한지 확인한다.
        1) 만약 집도가 가능한 경우

          그래서 수술시작시간 ~ 수술예상종료시간 + 해당 주치의를 진료시간에서 검색해봐서
          진료가 겹치는게 있으면 해당 진료기록을 지워버리고 해당 진료시간으로 예약한 예약정보 승인여부를 거절로 바꿔버리기

        2) 집도가 불가능한 경우 그냥 수술 시키지말자..
          해당 진료기록의 소견을 수술 말고 딴걱로 바꿔버리기... 
        '''


        q = "(SELECT 진료일시 FROM 수술 WHERE (수술시작일시 BETWEEN '%s' AND '%s') OR (수술예상종료일시 BETWEEN '%s' AND '%s') AND 집도의번호 = '%d')" % (수술시작시간, 수술예상종료시간, 수술시작시간, 수술예상종료시간, 의사번호)
        cursor.execute(q)
        result2 = cursor.fetchall()
        print(len(result2))
        if len(result2) > 0: # 집도가 불가능
          pass
          # 수술 기록을 만들지 않음
          
        else: # 집도가 가능

          수술결과 =  ['성공적', '성공적', '성공적', '재수술 필요', '경과를 지켜봐야됨', '재검사 필요'][randrange(0,6)]
          print(수술결과)

          q = "DELETE FROM 진료 WHERE (환자번호, 진료일시) IN (SELECT 환자번호, 진료일시 FROM 수술 WHERE (수술시작일시 BETWEEN '%s' AND '%s') OR (수술예상종료일시 BETWEEN '%s' AND '%s') AND 집도의번호 = '%d')" % (수술시작시간, 수술예상종료시간, 수술시작시간, 수술예상종료시간, 의사번호)
          cursor.execute(q)
          conn.commit()

          q = "INSERT INTO 수술 (환자번호, 진료일시, 수술명, 수술시작일시, 수술예상종료일시, 수술소견, 집도의번호) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%d')" % (진료정보[0], 진료정보[1], 진료정보[2] + '수술', d_t_s(수술시작시간), d_t_s(수술예상종료시간), 수술결과, 의사번호)
          # print(q)
          cursor.execute(q)
          conn.commit()

          
          q = "UPDATE 예약 SET 승인여부 = 2 WHERE (예약일시 BETWEEN '%s' AND '%s') AND (희망의사번호 = '%d')" % (수술시작시간, 수술예상종료시간, 의사번호) 
          cursor.execute(q)
          conn.commit()

def 입원정보추가():
  q = "SELECT 병상번호, 병실번호, 병동번호 FROM 병상"
  cursor.execute(q)
  병상목록 = list(t + ([],) for t in list(cursor.fetchall()))

  for 환자번호 in range(30001, 30501):

    q = "SELECT 환자번호, 진료일시 FROM 진료 WHERE 진료소견 LIKE '%수술%'" + "AND 환자번호 = '%d' ORDER BY 진료.진료일시 ASC" % (환자번호)
    cursor.execute(q)
    result = cursor.fetchall()
    for i in range(len(result)):
      f = result[i][1]
      if i == len(result)-1:
        t = f + timedelta(days=3)
      else:
        t = result[i+1][1]

      ## 병상 선택하기 -------------------
      for j in range(len(병상목록)):
        # 해당 병상의 입원목록 = 병상목록[j][3]
        flag = False
        for k in 병상목록[j][3]:
          if not (t < k[0] or k[1] <f):
            flag = True
            break

        if not flag: # 입원 가능할 때
          병상목록[j][3].append((f,t))
          q = "INSERT INTO 입원 (입원일시, 퇴원예정일시, 병상번호, 병실번호, 병동번호, 환자번호) VALUES ('%s', '%s', '%d', '%d', '%d', '%d')" % (d_t_s(f), d_t_s(t), 병상목록[j][0], 병상목록[j][1], 병상목록[j][2], 환자번호)
          cursor.execute(q)
          conn.commit()
          break

def 입원간호사추가():
  q = "SELECT 직원번호 FROM 직원 WHERE 직원종류=2"
  cursor.execute(q)
  간호사목록 = list(t + ([],) for t in list(cursor.fetchall()))
  random.shuffle(간호사목록)
  print(간호사목록)
  def find간호사(n, f, t):
    r = []
    for i in range(n):
      for j in range(200):
        flag = False
        for k in 간호사목록[j][1]:
          if not (t < k[0] or k[1] <f):
            flag = True
            break
        if not flag:
          r.append(간호사목록[j][0])
          간호사목록[j][1].append((f,t))
          break
    return r
  q = "SELECT 환자번호, 입원일시, 퇴원예정일시 FROM 입원 WHERE 퇴원예정일시 < NOW()" # 과거의 정보에만추가
  cursor.execute(q)
  result = list(cursor.fetchall())

  for i in range(len(result)): #입원정보
    n = randrange(1, 4)
    f = result[i][1]
    t = result[i][2]
  
    간호사들 = find간호사(n, f, t)
    날짜들 = [get_random_datetime(d_t_s(f), d_t_s(t)) for j in range(n)]
    날짜들.sort()
    _f = f
    print(i, n, 간호사들, 날짜들, f, t)
    날짜들[n-1] = t
    for j in range(n):
      시작 = _f
      끝 = 날짜들[j]
      직원번호 = 간호사들[j]
      q = "INSERT INTO 입원_간호사 (직원번호, 배정시작일시, 배정종료일시, 환자번호, 입원일시) VALUES ('%d', '%s', '%s', '%d', '%s')" % (직원번호, d_t_s(시작), d_t_s(끝), result[i][0], result[i][1])
      cursor.execute(q) 
      conn.commit()
      _f = 날짜들[j] + timedelta(seconds=1)

# 환자번호, 진료일시, 검사종류
'''
DELETE FROM 입원_간호사;
DELETE FROM 입원;
DELETE FROM 수술;
DELETE FROM 진료;
DELETE FROM 예약;
'''

#진료정보만들기() 
#진료중복삭제()  
#수술정보추가()
#입원정보추가()
#입원간호사추가()
def 검사정보추가():
  q = "SELECT 직원번호 from 직원"
  cursor.execute(q)
  직원 = list(cursor.fetchall())
  random.shuffle(직원)
  cnt = 0
  q = "SELECT * from 진료"
  cursor.execute(q)
  result = list(cursor.fetchall())
  for d in result:
    검사일시 = d[1] + timedelta(minutes=10)
    진료일시 = d[1]
    환자번호 = d[3]
    검사종류 = ['CT', '내시경', 'X-RAY', '혈액', 'MRI'][randrange(0, 5)]
    소견 = ['정상', '문제발견', '재검 요망'][randrange(0, 3)]
    try:
      q = "INSERT INTO 검사 VALUES ('%s', '%s', '%s', '%d', '%s')" % (검사종류, d_t_s(검사일시), 소견, 환자번호, 진료일시)
      cursor.execute(q)
      conn.commit()
  
      q = "INSERT INTO 검사_직원 VALUES ('%d', '%d', '%s', '%s')" % (직원[cnt][0], 환자번호, 진료일시, 검사종류)
      cnt += 1
      cnt %= len(직원)
      cursor.execute(q)
      conn.commit()
    except Exception as e:
      pass


  
검사정보추가()

'''
UPDATE 수술 SET 수술소견 = '' WHERE 수술시작일시 > NOW();
DELETE FROM 진료 WHERE 진료일시 > NOW();
DELETE FROM 입원 WHERE 입원일시 > NOW();
'''

conn.close()
'''

# 수술 정보 넣기
  for 의사정보 <- random:
    
    위의 진료 정보 중 소견이 수술인걸 의사별로 쫙 긁어오고 진료일시별로 오름차순으로 정렬. 
    수술 시간은 랜덤으로 randrange(1,30) * 10분으로 해버리자.

    그래서 수술시작시간은 = 진료일시 + 우리가 설정한 기본 진료시간(30분정도)*2
    수술 예상종료시간은 수술종료시간 = 수술시작시간 + 수술시간

    일단 수술정보로 위의 수술 시작시간~예상 종료시간을 주치의로 검색해가지고 해당 집도의가 집도가 가능한지 확인한다.
    1) 만약 집도가 가능한 경우

      그래서 수술시작시간 ~ 수술예상종료시간 + 해당 주치의를 진료시간에서 검색해봐서
      진료가 겹치는게 있으면 해당 진료기록을 지워버리고 해당 진료시간으로 예약한 예약정보 승인여부를 거절로 바꿔버리기

    2) 집도가 불가능한 경우 그냥 수술 시키지말자..
      해당 진료기록의 소견을 수술 말고 딴걱로 바꿔버리기... 
      아니면 다른 방안 찾아뵉 

    진료정보에서 찾아본다.

    위의 진료정보에서 


    그리고 수술 정보를 삽입한다.

    또 쿼리를 날려서 만약 진료일시 + 40분
    만약 해당 주치의가 

# 입원 정보 넣기 => 위의 진료 쿼리에서 의사별로 GROUP_BY

for 환자번호 <- random: (psuedo 코드임 파이썬 문법아님)
  진료정보들 <- 해당 환자번호에 대한 모든 진료정보 중에서 진료 소견이 수술인 것,
  그리고 미래에 입원 시킬 수는 없으므로 NOW()보다 작은 진료일시만 뽑아내기 MYSQL의 NOW()찾아보기
  그리고 진료일시 순으로 오름차순 정렬
    # 설명
    진료1 -> 수술
    진료2 -> 수술X
    진료3 -> 수술
    진료4 -> 수술X
    진료5 -> 수술
    일때 진료1~진료3, 진료3~진료5 입원시키기
    n = len(진료정보)
    for i in range(n):
      진료정보[i]진료일시부터 진료정보[i+1]진료일시까지 입원시켜버리기
      만약 i+1 == n일때는 퇴원예정시간 = NULL로 하던지 아니면 임의로 진료정보[i]진료일시보다 이틀 더 하던지.. (datetime에 timedelta 더하면 됨, 위에 있는 함수 활용하기)

      여기서 환자의 부서에 있는 간호사를 랜덤으로 배정시킨다.
      근데 만약 입원_간호사 테이블에서 간호사번호로 조회하고 배정시작일시를 기준으로 내림차순으로 정렬했을때
      정보가 하나 이상이고 제일 위에있는 정보(index가 0인) 입원_간호사 튜플의 배정종료일시가 NULL 이면 
      배정이 불가능한 간호사니까 새로운 간호사를 선택하던지 아니면 배정종료(배정종료시간=진료정보[i]진료일시)시키고 새로운 입원정보를 배정시켜도 될듯
'''
