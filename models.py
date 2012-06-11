"""Models"""
from google.appengine.ext import db

class serialNoMap(db.Model):
	sno=db.StringProperty()
	erollno=db.StringProperty()
	

class rankList(db.Model):
	rank=db.StringProperty()
	score=db.StringProperty()
	erollno=db.StringProperty()
	qualboard=db.StringProperty()
	pcm=db.StringProperty()
	entmark=db.StringProperty()
	sno=db.StringProperty()
	name=db.StringProperty()

class appStatus(db.Model):
	keyword=db.StringProperty()
	status=db.StringProperty()
	desc=db.StringProperty()

class btechApp(db.Model):
	appid=db.StringProperty()
	apptype=db.StringProperty()
	appcreatedby=db.StringProperty()
	appstatus=db.StringProperty()
	applieddtime=db.DateTimeProperty(auto_now_add=True)
	apprank=db.StringProperty
	name=db.StringProperty()
	paddress=db.TextProperty()
	resphone=db.StringProperty()
	mobphone=db.StringProperty()
	panchayath=db.StringProperty()
	samepaddress=db.TextProperty()
	caddress=db.TextProperty()
	email=db.EmailProperty()
	dob=db.DateProperty()
	gender=db.StringProperty()
	nation=db.StringProperty()
	religion=db.StringProperty()
	caste=db.StringProperty()
	category=db.StringProperty()
	fathername=db.StringProperty()
	fatheremployed=db.StringProperty()
	fatherocc=db.StringProperty()
	fatherdesig=db.StringProperty()
	fatheraddress=db.TextProperty()
	fatherphone=db.StringProperty()
	mothername=db.StringProperty()
	motheremployed=db.StringProperty()
	motherocc=db.StringProperty()
	motherdesig=db.StringProperty()
	motheraddress=db.TextProperty()
	motherphone=db.StringProperty()
	mfboaesmemno=db.StringProperty()
	pfboaesmemno=db.StringProperty()
	income=db.StringProperty()
	erollno=db.StringProperty()
	erank=db.StringProperty()
	epcmark=db.StringProperty()
	epcmaxmark=db.StringProperty()
	emmark=db.StringProperty()
	emmaxmark=db.StringProperty()
	insaddress=db.TextProperty()
	insphone=db.StringProperty()
	qualboard=db.StringProperty()
	qualexamyear=db.StringProperty()
	qualexamno=db.StringProperty()
	qualexam=db.StringProperty()
	qpmark=db.StringProperty()
	qpmaxmark=db.StringProperty()
	qcmark=db.StringProperty()
	qcmaxmark=db.StringProperty()
	qmmark=db.StringProperty()
	qmmaxmark=db.StringProperty()
	bp1=db.StringProperty()
	bp2=db.StringProperty()
	bp3=db.StringProperty()
	bp4=db.StringProperty()
	bp5=db.StringProperty()
	bp6=db.StringProperty()
	extra=db.TextProperty()
	addinfo=db.TextProperty()
	ddno=db.StringProperty()
	dddate=db.StringProperty()
	ddbank=db.StringProperty()
	ddbranch=db.StringProperty()
	clientip=db.StringProperty()


	
