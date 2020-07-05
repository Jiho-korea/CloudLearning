import pyrebase

config = {
    "apiKey": "AIzaSyDU9epT6v6ByF1ETbO7Wb8bfnjl03jDzeQ",
    "authDomain": "cloudlearning-c6b5b.firebaseapp.com",
    "databaseURL": "https://cloudlearning-c6b5b.firebaseio.com",
    "projectId": "cloudlearning-c6b5b",
    "storageBucket": "cloudlearning-c6b5b.appspot.com",
    "messagingSenderId": "886108415440",
    "appId": "1:886108415440:web:c68e7a51da2ff23a97c5d5",
    "measurementId": "G-7CPKRDBZQ2",
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("CloudLearning").child("Monitoring").update({"CPU": 9999})
db.child("CloudLearning").child("Monitoring").update({"MEMORY": 9999})
