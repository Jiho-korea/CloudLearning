# -*-coding:utf-8 -*-

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import google

cred = credentials.Certificate("./CloudLearning.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'CloudLearning').document(u'Monitoring')
# doc_ref.set({
#     u'CPUTemp': 200
# })

try:
    doc = doc_ref.get()
    print(u'Document data: {}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'No such document!')
