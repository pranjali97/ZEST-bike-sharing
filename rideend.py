import json
import os
import requests
from flask import jsonify

info = {'ride_id':'4','cyclenm':'2','dockst':'5', 'dockno':'8', 'string':'12567'}
r = requests.post('http://localhost:5000/endride',json=info)
print (r.text)
