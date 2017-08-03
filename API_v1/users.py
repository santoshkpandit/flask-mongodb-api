from flask import json, request, jsonify, Response
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.json_util import dumps
#import hashlib
from passlib.hash import sha256_crypt


client = MongoClient('localhost', 27017)  
db = client.bis_research  
usersTbl = db.users 

def login():

	user_data = request.json
	if request.method =='POST' and 'email' in user_data and 'password' in user_data :
		if user_data['email'] or user_data['password']:
			results = usersTbl.find({"email":user_data['email']})
			# return dumps(results[0]['password'])
			if results.count()==1 and sha256_crypt.verify(user_data['password'],results[0]['password']):
			  return Response(dumps({"response": { "status": "success","message": "login success", "data":results }}), mimetype='application/json') 
			else :
			  return Response(dumps({"response": { "status": "failed","message": "Invalid email or password","data":"[]" }}), mimetype='application/json')
		else :
				return Response(dumps({"response": {"status": "failed","message": "Missing email or password","data":"[]"  } }), mimetype='application/json')		 	             
	else:
		  return Response(dumps({"response":{ "status": "failed", "message": " Missing required param", "data":"[]"  }  }), mimetype='application/json')


def pwd_hash():
	#generate
	password = sha256_crypt.encrypt("12345678")
	#veryfy
	#sha256_crypt.verify('123',password)
	return dumps(password)