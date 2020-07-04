# -*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(
    "./CloudLearning.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'CloudLearning').document(u'Monitoring')
doc_ref.set({
    u'CPU': 20,
    u'Memory': 200
})
