import pymysql
import random
from datetime import datetime

conn = pymysql.connect(host = 'localhost', user = 'root', password ='pns02089', db='gamja', charset='utf8mb4')
cursor = conn.cursor()


disease = {1: ["만성피로", "관절통", "요통", "전신쇠약", "노화"], 2: ["HIV감염","인플루엔자","풍토병","폐외 결핵","공수병"], 3: ["디스크질환","암성통증","만성통증","복합부위통증증후군",
"만성요통",], 4: ["자궁암","폐암","간암", "방광암","갑상선암"], 5: ["발기부전","요실금","배뇨장애","전립선암","요로결석"
], 6: ["자궁경부암","고위험임신","태아기형","생리불순","폐경"], 7: ["얼굴기형","두경부재건","악안면외상","화상","유방재건"], 8: ["소아 알레르기","아토피","유전 질환","내분비 질환","뇌전증"], 9: ["변비","담석증","간질환","염증성 장질환","과민성장증후군"], 10: ["뇌졸중","말초신경병","치매","근무력증","언어장애"],
11 : ["동맥경화","협심증","심근경색증","허혈성 심질환","고혈압"], 12: ["녹내장","백내장","망막손상","각막손상","안암"], 14: ["치핵", "탈장","대장암","췌장암","당뇨"],
15: ["독극물중독","중증 외상","골절","치아골절","자상"], 16: ["안면마비","평형기관장애","식도암","구강암","후두암"],
17 : ["말초신경손상","인대손상","인대파열","골연골염","탈골"], 18: ["슬관절염","견관절염","족관절염","고관절장애","인공관절손상"], 
19: ["양악수술","턱교정수술","임플란트","안면비대칭","충치치료"], 20: ["늑막질환","기흉","오목가슴","정맥류","기관지염"]}
rann = ["수술", "휴식", "검진", "금주", "규칙적인 생활"]

print(disease[7][1])

def randomTime():
    year = random.randrange(2017, 2020)
    month = random.randrange(1, 13)
    day = random.randrange(1, 29)
    hour = random.randrange(9, 19)
    minute = random.randrange(0, 60)
    sec = random.randrange(0, 59)
    date = datetime(year, month, day, hour, minute, sec)
    return date

for i in range(1, 100):
    index = random.randrange(0,5) #임의의 병 번호 선택
    num = random.randrange(30001, 30501) #환자 랜덤 select
    sql = "SELECT E.직원번호, D.부서번호 FROM 직원 E, 환자 P, 부서 D WHERE P.환자번호 = '%d' AND P.주치의번호 = E.직원번호 AND E.부서번호 = D.부서번호" %(num)
    cursor.execute(sql)
    result = cursor.fetchall()
    dep = int(result[0][1]) #해당 주치의의 부서 번호
    if dep == 13:
        continue
    else:
        doc = int(result[0][0]) #해당 환자의 주치의 번호
        diag = "%s으(로) 인한 %s이(가) 필요함." %(disease[dep][index], rann[index])
        now = randomTime()
        time = '%s-%s-%s %s:%s:%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        nq = "INSERT INTO 진료 (진단명, 진료일시, 의사번호, 환자번호, 진료소견) VALUES('%s', '%s', '%d', '%d', '%s')" %(disease[dep][index], now, doc, num, diag)
        cursor.execute(nq)
        result = cursor.fetchall()
        conn.commit()
        print(nq)

                                