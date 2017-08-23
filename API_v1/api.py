from flask import json, request, jsonify, Response
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.json_util import dumps
#latedt
import datetime


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
			  	                     "status": "200",
			  	                     "message": "Login success", 
			  	                     "data":userLogin }}), mimetype='application/json') 
			  
			else :
			  return Response(dumps({"response": { 
			  	                     "status": "0",
			  	                     "message": "Invalid email or password",
			  	                     "data":"" }}), mimetype='application/json')
		else :
				return Response(dumps({"response": {
					                     "status": "0",
					                     "message": "Missing email or password",
					                     "data":""  } }), mimetype='application/json')		 	             
	else:
		  return Response(dumps({"response":{ 
		  	                     "status": "0", 
		  	                     "message": " Missing required param",
		  	                     "data":""  }  }), mimetype='application/json')


#GET director information by DIN

def director_info(*args):
	request_param = request.args
	industryTbl = db.industry
	if request.method =='GET' and 'din' in request_param:
	  din =request_param['din']

	  directorInfo = industryTbl.find_one({"company.signatories.DIN/PAN": din},{"company.signatories.main_data":1,"company.signatories.pan_data":1})
	  return Response(dumps({"response":{ 
		  	                     "status": "200", 
		  	                     "message": "director information",
		  	                     "data":directorInfo  }  }), mimetype='application/json')
	else :
	  return Response(dumps({"response":{ 
		  	                     "status": "0", 
		  	                     "message": " Missing required param",
		  	                     "data":""  }  }), mimetype='application/json')

#GET director's Compan by DIN

def company_by_director(*args):
	request_param = request.args
	dcrTbl = db.industry
	if request.method =='GET' and 'din' in request_param:
	  din =request_param['din']
	  dcrInfo = dcrTbl.find({"company.signatories.DIN/PAN": din},{"company.signatories.director_data":1})
	  return Response(dumps({"response":{ 
		  	                     "status": "200", 
		  	                     "message": "Associated companies list of director",
		  	                     "data":dcrInfo  }  }), mimetype='application/json')
	else :
	  return Response(dumps({"response":{ 
		  	                     "status": "0", 
		  	                     "message": " Missing required param",
		  	                     "data":""  }  }), mimetype='application/json')

#GET director's Company by CIN

def director_by_company(*args):
	request_param = request.args
	dcrTbl = db.industry
	if request.method =='GET' and 'cin' in request_param:
	  cin =request_param['cin']
	  cmpInfo = dcrTbl.find({"company.cin_number": cin},{"company.signatories.main_data":1,"company.signatories.pan_data":1})
	  return Response(dumps({"response":{ 
		  	                     "status": "200", 
		  	                     "message": "Associated directors list of company",
		  	                     "data":cmpInfo  }  }), mimetype='application/json')
	else :
	  return Response(dumps({"response":{ 
		  	                     "status": "0", 
		  	                     "message": " Missing required param",
		  	                     "data":""  }  }), mimetype='application/json')

#GET News

def get_news(*args):
	request_param = request.args
	objTbl = db.news
	if request.method =='GET' and 'fromDate' in request_param and 'toDate' in request_param and 'userType' in request_param  and 'userId' in request_param and 'catType' in request_param and 'topic' in request_param:
	  
	  fromDate  = request_param['fromDate']
	  toDate    = request_param['toDate']
	  userType  = request_param['userType']
	  userId    = request_param['userId']
	  catType   = request_param['catType']
	  topic     = request_param['topic']
	  where = {'NewsDate':{'$gt':fromDate,'$lt':toDate}}

	  if catType=='social':
	  	objTbl = db.social
	  elif catType=='legal':
	  	objTbl = db.legal
	  else:
	  	objTbl= db.news

	  if userType !='' and userId!='':
	  	where = {userType:userId,'NewsDate':{'$gt':fromDate,'$lt':toDate}}
	  if topic !='':
	  	where +="'Topic':'"+topic+"',"

	  #where = where.rstrip(",")
	  #where = unicode(where, 'utf-8')

	  #return Response(where)

	  #UserType(Key) =>Industry/CIN/DIN & UserId(Val)

	  #getMonth  = datetime.datetime.now().strftime('%B')
	  
	  fromDate  = datetime.datetime.strptime(fromDate,'%d-%m-%Y')
	  toDate    = datetime.datetime.strptime(toDate,'%d-%m-%Y')
    
	  key       = 'function(doc) { return { month_of_year:doc.NewsDate.getMonth()}}'
	  condition = {where}
	  initial   = { 'total' : 0, 'count': 0 }
	  reducer   = 'function(curr,result){result.total += 1 ; result.count++; }'
	  finalize  = "function(result){ yearmonths=[\"January\",\"February\",\"March\", \"April\",\"May\",\"June\",\"August\",\"September\", \"October\",\"November\", \"December\"];result.month_of_year= yearmonths[result.month_of_year];result.avg = Math.round(result.total / result.count);}"


	  newsData=objTbl.group(key, condition, initial, reducer,finalize)


	  return Response(dumps({"response":{ 
		  	                     "status": "200", 
		  	                     "message": "News List",
		  	                     "data":newsData  }  }), mimetype='application/json')
	else :
		return Response(dumps({"response":{ 
		  	                     "status": "0", 
		  	                     "message": "Missing required param",
		  	                     }  }), mimetype='application/json')
	

#for password hashing--
def pwd_hash():
	#generate
	password = sha256_crypt.encrypt("12345678")
	#verify
	#sha256_crypt.verify('123',password)
	return dumps(password)