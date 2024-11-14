import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-real-tim-4a64a-default-rtdb.firebaseio.com/"
 }
)

dataFolder = db.reference('Students')


data = {

    "Z1": 
    {
        "id": "Z1",
        "name": "Elon Musk",
        "company": "Tesla",
        "Joined year": 2008,
        "total attendance": 0,
        "nationality": "American",
        "gender": "male",
        "last attendance time": "2004-02-28 00:00:00",
    },

    "Z2": 
    {
        "id": "Z2",
        "name": "Tim Cook",
        "company": "Apple",
        "Joined year": 2011,
        "total attendance": 0,
        "nationality": "American",
        "gender": "male",
        "last attendance time": "2004-02-28 00:00:00",
    },

    "Z3": 
    {
        "id": "Z3",
        "name": "Krithivasan",
        "company": "Tata",
        "Joined year": 2023,
        "total attendance": 0,
        "nationality": "Indian",
        "gender": "male",
        "last attendance time": "2004-02-28 00:00:00",
    },

    "Z4": 
    {
        "id": "Z4",
        "name": "Emily Blunt",
        "company": "Actress",
        "Joined year": 2003,
        "total attendance": 0,
        "nationality": "UK",
        "gender": "female",
        "last attendance time": "2004-02-28 00:00:00",
    },

    "Z5": 
    {
        "id": "Z5",
        "name": "Sunder Pichai",
        "company": "Google",
        "Joined year": 2015,
        "total attendance": 0,
        "nationality": "Indian",
        "gender": "male",
        "last attendance time": "2004-02-28 00:00:00",
    },
    
    "Z6": 
    {
        "id": "Z6",
        "name": "Leonor",
        "company": "Spain",
        "Joined year": 2005,
        "total attendance": 0,
        "nationality": "Spain",
        "gender": "female",
        "last attendance time": "2003-09-21 01:00:00",
    },
    "Z7": 
    {
        "id": "Z7",
        "name": "Hari",
        "company": "Student",
        "Joined year": 2003,
        "total attendance": 0,
        "nationality": "Indian",
        "gender": "male",
        "last attendance time": "2003-09-21 00:00:00",
    },

    "Z8": 
    {
        "id": "Z8",
        "name": "Ryan Roslansky",
        "company": "Linkdin",
        "Joining year": 2020,
        "total attendance": 0,
        "nationality": "American",
        "gender": "female",
        "last attendance time": "2004-02-28 00:00:00",
    },


}
for key, value in data.items():
    dataFolder.child(key).set(value)

