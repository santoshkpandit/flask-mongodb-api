from flask import json, request, jsonify, Response
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.json_util import dumps
#import hashlib
from passlib.hash import sha256_crypt


client = MongoClient('localhost', 27017)  
db = client.bis_research

usersTbl = db.users
planTbl  = db.plan_master 

#Post Login
def login():
	usersTbl = db.users
	planTbl  = db.plan_master 
	user_data = request.json

	if request.method =='POST' and 'email' in user_data and 'password' in user_data :
		if user_data['email'] and user_data['password']:

			userLogin = usersTbl.find_one({"email":user_data['email']})
			# return dumps(userLogin['plan_id'])

			if 'password' in userLogin and sha256_crypt.verify(user_data['password'],userLogin['password']):
				if 'plan_id' in userLogin and userLogin['plan_id']:
					   del(userLogin['password'])
					   userPlan = planTbl.find_one({"_id":ObjectId(userLogin['plan_id'])})
					   userLogin['userPlan'] = userPlan
				else :
					   userLogin['userPlan'] = ""
				return Response(dumps({"response": { 
			  	                     "status": "success",
			  	                     "message": "login success", 
			  	                     "data":userLogin }}), mimetype='application/json') 
			  
			else :
			  return Response(dumps({"response": { 
			  	                     "status": "failed",
			  	                     "message": "Invalid email or password",
			  	                     "data":"" }}), mimetype='application/json')
		else :
				return Response(dumps({"response": {
					                     "status": "failed",
					                     "message": "Missing email or password",
					                     "data":""  } }), mimetype='application/json')		 	             
	else:
		  return Response(dumps({"response":{ 
		  	                     "status": "failed", 
		  	                     "message": " Missing required param",
		  	                     "data":""  }  }), mimetype='application/json')


def pwd_hash():
	#generate
	password = sha256_crypt.encrypt("12345678")
	#verify
	#sha256_crypt.verify('123',password)
	return dumps(password)