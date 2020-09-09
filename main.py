from flask import Flask, request, jsonify
import json
import os
import pymysql
from passlib.hash import sha256_crypt
from flask_cors import CORS
from flask_restful import Api

from login import LoginUser, LoginStaff
from reservations import Reservations, ReservationJudge
from users import Users, UsersById
from departments import Departments, DepartmentsById
from diagnosis import Diagnosis
from doctors import Doctors, DoctorsById
from nurses import Nurses, NursesById
from wards import Wards, Rooms, Sickbeds
from schedule import Schedules
from surgery import Surgery, SurgeryById
from hospital import Hospital, HospitalById, HospitalByNow


app = Flask(__name__)
CORS(app)

usertoken = {}
stafftoken = {}


@app.route('/')
def HelloWorld():
    return "Hello Flask!"


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(LoginUser, '/login/user')
    api.add_resource(LoginStaff, '/login/staff')
    api.add_resource(Reservations, '/reservations')
    api.add_resource(ReservationJudge, '/reservations/judge')
    api.add_resource(Users, '/users')
    api.add_resource(UsersById, '/users/<id>')
    api.add_resource(Departments, '/departments')
    api.add_resource(DepartmentsById, '/departments/<id>')
    api.add_resource(Diagnosis, '/diagnosis')
    api.add_resource(Doctors, '/doctors')
    api.add_resource(DoctorsById, '/doctors/<id>')
    api.add_resource(Nurses, '/nurses')
    api.add_resource(NursesById, '/nurses/<id>')
    api.add_resource(Wards, '/wards')
    api.add_resource(Rooms, '/rooms/<wid>')
    api.add_resource(Sickbeds, '/sickbeds/<wid>/<rid>')
    api.add_resource(Schedules, '/schedule/doctor')
    api.add_resource(Surgery, '/surgery')
    api.add_resource(SurgeryById, '/surgery/<sid>')
    api.add_resource(Hospital, '/hospital')
    api.add_resource(HospitalById, '/hospital/<id>')
    api.add_resource(HospitalByNow, '/hospital/now')



    port = os.getenv('PORT', 3000)
    app.run(host='0.0.0.0', port=port)
