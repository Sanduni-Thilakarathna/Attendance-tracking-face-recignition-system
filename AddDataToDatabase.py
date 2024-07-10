import firebase_admin
from firebase_admin import credentials, db  ## Import db module

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
   'databaseURL' :"https://faceattendancerealtime-a8879-default-rtdb.firebaseio.com/"
   })

ref = db.reference('Students')

#attence and last_attendance_time will be updated by the main.py when detecting

data = {
    "000192":
    {
        "name": "Pasindu Thiwanka",
        "major": "Electronic",
        "starting_year":2021,
        "total_attendance":7,
        "standing": "G",    #Good
        "year":3,
        "last_attendance_time":"2022-12-11 00:54:34"
    },
    "000217":
    {
        "name": "Vishmi Dilusha",
        "major": "Computer",
        "starting_year":2021,
        "total_attendance":10,
        "standing": "G",    #Good
        "year":3,
        "last_attendance_time":"2022-12-11 00:54:34"
    },
    "000001":
    {
        "name": "Elon Musk",
        "major": "Mechanical",
        "starting_year":2022,
        "total_attendance":2,
        "standing": "B",    #Bad
        "year":2,
        "last_attendance_time":"2022-12-11 00:54:34"
    },
     "000024":
    {
        "name": "Lahiru Bulathwatta",
        "major": "Civil",
        "starting_year":2022,
        "total_attendance":6,
        "standing": "B",    #Bad
        "year":2,
        "last_attendance_time":"2022-12-11 00:54:34"
    },
     "000040":
    {
        "name": "Poornima Ekanayake",
        "major": "Electrical",
        "starting_year":2021,
        "total_attendance":7,
        "standing": "B",    #Bad
        "year":3,
        "last_attendance_time":"2022-12-11 00:54:34"
    },
     "000158":
    {
        "name": "Sanduni Mihisarani",
        "major": "Computer",
        "starting_year":2020,
        "total_attendance":8,
        "standing": "B",    #Bad
        "year":4,
        "last_attendance_time":"2022-12-11 00:54:34"
    }
    }


for key,value in data.items():
    ref.child(key).set(value)


