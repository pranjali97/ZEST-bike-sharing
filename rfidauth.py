import json
import os
import requests
from flask import jsonify

data = {'string':'12567'}
r = requests.post('http://localhost:5000/rfidauth',json=data)
print (r.text)
flag = r.json()
info = {'ride_id':'4','cyclenm':'2','dockst':'1', 'dockno':'5', 'string':'12567'}

if flag['val']==1:
	print("authentication successful, updating the db")
	r = requests.post('http://localhost:5000/updaterfidtb',json=info)
	print (r.text)
	print("db updated")
else:
	print("authentication failed")


