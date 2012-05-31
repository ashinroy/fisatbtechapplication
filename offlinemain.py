import sys
import os


from google.appengine.api import mail
from google.appengine.ext.webapp import template
import cgi
import csv
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from defaults import *
from models import * 
import re
import time
from datetime import date


from os import environ


def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips

def sendapp_mail(appid,name,mailadd):
	try:
		mail.send_mail(sender="<admissions@fisat.ac.in>",to=mailadd,subject="FISAT BTech 2012 Admission",body=(offlinemailbody % (name,appid)))
	except:
		pass

class MainPage(webapp.RequestHandler):
	def get(self):
		if check_access()==False:
			self.redirect("/h404",permanent=True)
		else:
			form=defaults()
			values={"formv":form.values,"forme":form.errors}
			path = os.path.join(os.path.dirname(__file__), 'offlineapptemplate.html')
			self.response.out.write(template.render(path, values))
	def validate_name(self,name):
		USER_RE = re.compile("^[a-zA-Z. ][a-zA-Z. ]+$")
		return USER_RE.match(name)	
	def validate_phno(self,phone):
		RE = re.compile("^[0-9-]+$")
		return (RE.match(phone)and(len(phone)>phoneno_length))
	def validate_income(self,income):
		RE = re.compile("^[0-9]+$")
		return (RE.match(income))
	def validate_email(self,email):
		EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
		return EMAIL_RE.match(email)
	def validate_erollno(self,rollno):
		RE = re.compile("^[0-9A-Za-z-/]+$")
		return (RE.match(rollno)and(len(rollno)>erollno_length))
	def validate_erank(self,rank):
		RE = re.compile("^[0-9]+$")
		return (RE.match(rank))
	def validate_mark(self,mark):
		RE = re.compile("^[0-9-.]+$")
		return (RE.match(mark) and float(mark)!=0)
	def validate_year(self,year):
		RE = re.compile("^[0-9-]+$")
		return (RE.match(year) and len(year)==4)
	
	
	
	def rot13alg(self,letter):
		L="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		try:		
			index=L.find(letter)
			if index>-1:
				if index>=13:
					index=index-13
					return L[index]
				else:
					return L[index+13]
			else:
				return 'F'
		except:
				return 'F'

	def generate_id(self,rollno,name):
		a1="F"
		a2="T"		
		try:		
			a1=self.rot13alg(name[0].capitalize())
			a2=self.rot13alg(name[2].capitalize())
		except:
			pass
		appid="F12"+a1+a2+str(rollno)
		return appid
	def check_id(self,erollno):
		btechapp=btechApp.all()
		btechapp.filter("erollno =",erollno)
		try:		
			app=btechapp.fetch(1)[0]
			return True
		except:
			return False
		

	def save_form(self,form):
		btechapp=btechApp()
		btechapp.appcreatedby="college"
		appid=self.generate_id(form.values['erollno'],form.values['name'])
		btechapp.appid=appid
		btechapp.name=form.values["name"]
		btechapp.paddress=form.values["paddress"]
		btechapp.resphone=form.values["resphone"]
		btechapp.mobphone=form.values["mobphone"]
		if form.values['panchayath']=="Others":
			btechapp.panchayath=form.values['inpanchayath']
		else:
			btechapp.panchayath=form.values["panchayath"]
		
		btechapp.caddress=form.values["caddress"]
		btechapp.email=form.values["email"]
		dob=date(int(form.values["dobyear"]),int(form.values["dobmonth"]),int(form.values["dobdate"]))
		btechapp.dob=dob		
		btechapp.gender=form.values["gender"]
		btechapp.nation=form.values["nation"]
		btechapp.religion=form.values["religion"]
		btechapp.caste=form.values["caste"]
		btechapp.category=form.values["category"]
		btechapp.fathername=form.values["fathername"]
		btechapp.fatheremployed=form.values["fatheremployed"]
		btechapp.fatherocc=form.values["fatherocc"]
		if 	form.values["fatheremployed"]=="YES":
			btechapp.fatheremployed="YES"
			btechapp.fatherdesig=form.values["fatherdesig"]
			btechapp.fatheraddress=form.values["fatheraddress"]
			btechapp.fatherphone=form.values["fatherphone"]
		else:
			btechapp.fatheremployed="NO"
			btechapp.fatherdesig="NA"
			btechapp.fatheraddress="NA"
			btechapp.fatherphone="NA"
		btechapp.mothername=form.values["mothername"]
		btechapp.motheremployed=form.values["motheremployed"]
		btechapp.motherocc=form.values["motherocc"]
		if form.values["motheremployed"]=="YES":
			btechapp.motheremployed="YES"
			btechapp.motherdesig=form.values["motherdesig"]
			btechapp.motheraddress=form.values["motheraddress"]
			btechapp.motherphone=form.values["motherphone"]
		else:
			btechapp.motheremployed="NO"
			btechapp.motherdesig="NA"
			btechapp.motheraddress="NA"
			btechapp.motherphone="NA"

		if form.values['enablemfboaes']=='ON':
			btechapp.mfboaesmemno=form.values["mfboaesmemno"]
		else:
			btechapp.mfboaesmemno="NA"
		if form.values['enablepfboaes']=='ON':
			btechapp.pfboaesmemno=form.values["pfboaesmemno"]
		else:
			btechapp.pfboaesmemno="NA"
		
		
		btechapp.income=(form.values["income"])
		btechapp.erollno=form.values["erollno"]
		btechapp.erank=form.values["erank"]
		btechapp.epcmark=(form.values["epcmark"])
		btechapp.epcmaxmark=(form.values["epcmaxmark"])
		btechapp.emmark=(form.values["emmark"])
		btechapp.emmaxmark=(form.values["emmaxmark"])
		btechapp.insaddress=form.values["insaddress"]
		btechapp.insphone=form.values["insphone"]
		btechapp.qualboard=form.values["qualboard"]
		btechapp.qualexamyear=form.values["qualexamyear"]
		btechapp.qualexamno=form.values["qualexamno"]
		btechapp.qualexam=form.values["qualexam"]
		btechapp.inqualexam=form.values["inqualexam"]
		btechapp.qpmark=(form.values["qpmark"])
		btechapp.qpmaxmark=(form.values["qpmaxmark"])
		btechapp.qcmark=(form.values["qcmark"])
		btechapp.qcmaxmark=(form.values["qcmaxmark"])
		btechapp.qmmark=(form.values["qmmark"])
		btechapp.qmmaxmark=(form.values["qmmaxmark"])
		btechapp.bp1=form.values["bp1"]
		btechapp.bp2=form.values["bp2"]
		btechapp.bp3=form.values["bp3"]
		btechapp.bp4=form.values["bp4"]
		btechapp.bp5=form.values["bp5"]
		btechapp.bp6=form.values["bp6"]
		btechapp.extra=form.values["extra"]
		btechapp.addinfo=form.values["addinfo"]
		btechapp.ddno=form.values["ddno"]
		btechapp.dddate=form.values["dddate"]
		btechapp.ddbank=form.values["ddbank"]
		btechapp.ddbranch=form.values["ddbranch"]
		btechapp.clientip=environ['REMOTE_ADDR']
		btechapp.appstatus=defstatus[2][0]
		btechapp.put()
		sendapp_mail(appid,form.values["name"],form.values["email"])
		return appid
		
	def post(self):
		if check_access()==False:
			self.redirect("/h404",permanent=True)
			return
		form=defaults()
		form.values["name"]=self.request.get("name").strip()
		form.values["paddress"]=self.request.get("paddress").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["resphone"]=self.request.get("resphone").strip().replace(" ","")
		form.values["mobphone"]=self.request.get("mobphone").strip().replace(" ","")
		form.values["panchayath"]=self.request.get("panchayath").strip()
		form.values["inpanchayath"]=self.request.get("inpanchayath").strip()
		form.values["samepaddress"]=self.request.get("samepaddress").strip()
		form.values["caddress"]=self.request.get("caddress").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["email"]=self.request.get("email").strip()
		form.values["dobdate"]=self.request.get("dobdate").strip()
		form.values["dobmonth"]=self.request.get("dobmonth").strip()
		form.values["dobyear"]=self.request.get("dobyear").strip()
		form.values["gender"]=self.request.get("gender").strip()
		form.values["nation"]=self.request.get("nation").strip()
		form.values["religion"]=self.request.get("religion").strip()
		form.values["caste"]=self.request.get("caste").strip()
		form.values["category"]=self.request.get("category").strip()
		form.values["fathername"]=self.request.get("fathername").strip()
		form.values["fatheremployed"]=self.request.get("fatheremployed").strip()
		form.values["fatherocc"]=self.request.get("fatherocc").strip()
		form.values["fatherdesig"]=self.request.get("fatherdesig").strip()
		form.values["fatheraddress"]=self.request.get("fatheraddress").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["fatherphone"]=self.request.get("fatherphone").strip()
		form.values["mothername"]=self.request.get("mothername").strip()
		form.values["motheremployed"]=self.request.get("motheremployed").strip()
		form.values["motherocc"]=self.request.get("motherocc").strip()
		form.values["motherdesig"]=self.request.get("motherdesig").strip()
		form.values["motheraddress"]=self.request.get("motheraddress").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["motherphone"]=self.request.get("motherphone").strip().replace(" ","")
		form.values["enablemfboaes"]=self.request.get("enablemfboaes").strip()
		form.values["mfboaesmemno"]=self.request.get("mfboaesmemno").strip()
		form.values["enablepfboaes"]=self.request.get("enablepfboaes").strip()
		form.values["pfboaesmemno"]=self.request.get("pfboaesmemno").strip()
		form.values["income"]=self.request.get("income").strip()
		form.values["erollno"]=self.request.get("erollno").strip()
		form.values["erank"]=self.request.get("erank").strip()
		form.values["epcmark"]=self.request.get("epcmark").strip()
		form.values["epcmaxmark"]=self.request.get("epcmaxmark").strip()
		form.values["emmark"]=self.request.get("emmark").strip()
		form.values["emmaxmark"]=self.request.get("emmaxmark").strip()
		form.values["insaddress"]=self.request.get("insaddress").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["insphone"]=self.request.get("insphone").strip().replace(" ","")
		form.values["qualboard"]=self.request.get("qualboard").strip()
		form.values["qualexamyear"]=self.request.get("qualexamyear").strip()
		form.values["qualexamno"]=self.request.get("qualexamno").strip()
		form.values["qualexam"]=self.request.get("qualexam").strip()
		form.values["inqualexam"]=self.request.get("inqualexam").strip()
		form.values["qpmark"]=self.request.get("qpmark").strip()
		form.values["qpmaxmark"]=self.request.get("qpmaxmark").strip()
		form.values["qcmark"]=self.request.get("qcmark").strip()
		form.values["qcmaxmark"]=self.request.get("qcmaxmark").strip()
		form.values["qmmark"]=self.request.get("qmmark").strip()
		form.values["qmmaxmark"]=self.request.get("qmmaxmark").strip()
		form.values["bp1"]=self.request.get("bp1").strip()
		form.values["bp2"]=self.request.get("bp2").strip()
		form.values["bp3"]=self.request.get("bp3").strip()
		form.values["bp4"]=self.request.get("bp4").strip()
		form.values["bp5"]=self.request.get("bp5").strip()
		form.values["bp6"]=self.request.get("bp6").strip()
		form.values["extra"]=self.request.get("extra").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["addinfo"]=self.request.get("addinfo").strip().replace("\n"," ").replace("\r"," ").replace("\""," ")
		form.values["ddno"]=self.request.get("ddno").strip()
		form.values["dddate"]=self.request.get("dddate").strip()
		form.values["ddbank"]=self.request.get("ddbank").strip()
		form.values["ddbranch"]=self.request.get("ddbranch").strip()
		challenge = self.request.get('recaptcha_challenge_field')
		response  = self.request.get('recaptcha_response_field')
		remoteip  = environ['REMOTE_ADDR']				
		error=0
		if self.validate_name(form.values['name']):
			form.errors['name']=""
			
		else:
			form.errors['name']="&nbsp;Invalid Name"
			error=1
		if len(form.values['paddress'])>address_length:
			form.errors['paddress']=""
			
		else: 		
			form.errors['paddress']="&nbsp;Invalid address"
			error=1
		if self.validate_phno(form.values['resphone']):
			form.errors['resphone']=""
			
		else:
			form.errors['resphone']="&nbsp;Invalid Phone NO"
			error=1
		if self.validate_phno(form.values['mobphone']):
			form.errors['mobphone']=""
			
		else:
			form.errors['mobphone']="&nbsp;Invalid Phone NO"
			error=1
		#if form.values['panchayath']=="Others":
		#	form.values['panchayath']=form.values['inpanchayath']
		if form.values['samepaddress']=='ON':
			form.values['caddress']=form.values['paddress']
		else:
			if len(form.values['caddress'])>address_length:
				form.errors['caddress']=""
			else:
				form.errors['caddress']="&nbsp;Invalid address"
				error=1 
		if self.validate_email(form.values['email']):
			form.errors['email']=""
			
		else:
			form.errors['email']="&nbsp;Invalid Email"
			error=1
		if len(form.values['nation'])>nation_length:
			form.errors['nation']=""
			
		else: 		
			form.errors['nation']="&nbsp;Invalid Nationality"
			error=1 

		if self.validate_name(form.values['fathername']):
			form.errors['fathername']=""
			
		else:
			form.errors['fathername']="&nbsp;Invalid Name"
			error=1
		if form.values['fatheremployed']=='YES':
			if len(form.values['fatheraddress'])>address_length:
				form.errors['fatheraddress']=""
				
			else:
				form.errors['fatheraddress']="&nbsp;Invalid Address"
		if self.validate_name(form.values['mothername']):
			form.errors['mothername']=""
			
		else:
			form.errors['mothername']="&nbsp;Invalid Name"
			error=1
		
		if form.values['motheremployed']=='YES':
			if len(form.values['motheraddress'])>address_length:
				form.errors['motheraddress']=""
				
			else:
				form.errors['motheraddress']="&nbsp;Invalid Address"
		if form.values['enablemfboaes']=='ON':
			if len(form.values['mfboaesmemno'])>fboaes_length:
				form.errors['mfboaesmemno']=""
				
			else:
				form.errors['mfboaesmemno']="&nbsp;Invalid Membership No"
		
		if form.values['enablepfboaes']=='ON':
			if len(form.values['pfboaesmemno'])>fboaes_length:
				form.errors['pfboaesmemno']=""
				
			else:
				form.errors['pfboaesmemno']="&nbsp;Invalid Membership No"
		if self.validate_income(form.values['income']):
			form.errors['income']=""
			
		else:
			form.errors['income']="&nbsp;Invalid Annual Income"
			error=1

		if self.validate_erollno(form.values['erollno']):
			form.errors['erollno']=""
			
		else:
			form.errors['erollno']="&nbsp;Invalid"
			error=1
		if self.validate_erank(form.values['erank']):
			form.errors['erank']=""
			
		else: 		
			form.errors['erank']=""#"&nbsp;Invalid Rank"
			form.values['erank']="NA"
			#error=1 

		if self.validate_mark(form.values['epcmark']):
			form.errors['epcmark']=""
			
		else: 		
			form.errors['epcmark']="&nbsp;Invalid"
			error=1 

		if self.validate_mark(form.values['epcmaxmark']):
			form.errors['epcmaxmark']=""
			
		else: 		
			form.errors['epcmaxmark']="&nbsp;Invalid"
			error=1 
		
		if self.validate_mark(form.values['emmark']):
			form.errors['emmark']=""
			
		else: 		
			form.errors['emmark']="&nbsp;Invalid"
			error=1 

		if self.validate_mark(form.values['emmaxmark']):
			form.errors['emmaxmark']=""
			
		else: 		
			form.errors['emmaxmark']="&nbsp;Invalid"
			error=1 
		if len(form.values['insaddress'])>address_length:
			form.errors['insaddress']=""
			
		else: 		
			form.errors['insaddress']="&nbsp;Invalid address"
			error=1
		if self.validate_phno(form.values['insphone']):
			form.errors['insphone']=""
			
		else:
			form.errors['insphone']="&nbsp;Invalid Phone NO"
			error=1

		if self.validate_year(form.values['qualexamyear']):
			form.errors['qualexamyear']=""
			
		else:
			form.errors['qualexamyear']="&nbsp;Invalid"
			error=1
		if len(form.values['qualexamno'])>qualexamno_length:
			form.errors['nation']=""
			
		else: 		
			form.errors['qualexamno']="&nbsp;Invalid"
			error=1 		
		if	form.values['qualexam']=='Others':
			if len(form.values['inqualexam'])>qualexam_length:
				form.errors['inqualexam']=""
			else:
				form.errors['inqualexam']="Invalid"
		if len(form.values['qualboard'])>qualboard_length:
			form.errors['qualboard']=""
		else:
			form.errors['qualboard']="Invalid"
		
		if self.validate_mark(form.values['qpmark']):
			form.errors['qpmark']=""
		else: 		
			form.errors['qpmark']="&nbsp;Invalid"
			error=1 
		if self.validate_mark(form.values['qpmaxmark']):
			form.errors['qpmaxmark']=""
		else: 		
			form.errors['qpmaxmark']="&nbsp;Invalid"
			error=1
		
		if self.validate_mark(form.values['qcmark']):
			form.errors['qcmark']=""
		else: 		
			form.errors['qcmark']="&nbsp;Invalid"
			error=1 
		if self.validate_mark(form.values['qcmaxmark']):
			form.errors['qcmaxmark']=""
		else: 		
			form.errors['qcmaxmark']="&nbsp;Invalid"
			error=1

		if self.validate_mark(form.values['qmmark']):
			form.errors['qmmark']=""
		else: 		
			form.errors['qmmark']="&nbsp;Invalid"
			error=1 
		if self.validate_mark(form.values['qmmaxmark']):
			form.errors['qmmaxmark']=""
		else: 		
			form.errors['qmmaxmark']="&nbsp;Invalid"
			error=1

		validate_bp= form.values['bp1']== form.values['bp2'] or form.values['bp1']== form.values['bp3'] or form.values['bp1']== form.values['bp4'] or form.values['bp1']== form.values['bp5'] or form.values['bp1']== form.values['bp6'] or form.values['bp2']== form.values['bp3'] or form.values['bp2']== form.values['bp4'] or form.values['bp2']== form.values['bp5'] or form.values['bp2']== form.values['bp6'] or form.values['bp3']== form.values['bp4'] or form.values['bp3']== form.values['bp5'] or form.values['bp3']== form.values['bp6'] or form.values['bp4']== form.values['bp5'] or form.values['bp4']== form.values['bp6'] or form.values['bp5']== form.values['bp6']
		if validate_bp==False:
			form.errors['bp1']=""
			if form.values['bp1']!='0':
				form.errors['bp1']=""
			else:
				form.errors['bp1']="Select a branch"
				error=1
			if form.values['bp2']!='0':
				form.errors['bp2']=""
			else:
				form.errors['bp2']="Select a branch"
				error=1
			if form.values['bp3']!='0':
				form.errors['bp3']=""
			else:
				form.errors['bp3']="Select a branch"
				error=1
			if form.values['bp4']!='0':
				form.errors['bp4']=""
			else:
				form.errors['bp4']="Select a branch"
				error=1
			if form.values['bp5']!='0':
				form.errors['bp5']=""
			else:
				form.errors['bp5']="Select a branch"
				error=1
			if form.values['bp6']!='0':
				form.errors['bp6']=""
			else:
				form.errors['bp6']="Select a branch"
				error=1
		else:
			form.errors['bp1']="&nbsp;&nbsp;&nbsp;All Choices must be different"
			error=1

		if len(form.values['ddno'])>ddno_length:
			form.errors['ddno']=""
		else:
			form.errors['ddno']="&nbsp;Invalid"
			error=1
		if len(form.values['ddbank'])>ddbank_length:
			form.errors['ddbank']=""
		else:
			form.errors['ddbank']="&nbsp;Invalid"
			error=1
		if len(form.values['dddate'])==10:
			form.errors['dddate']=""
		else:
			form.errors['dddate']="&nbsp;Invalid"
			error=1
		if len(form.values['ddbranch'])>ddno_length:
			form.errors['ddbranch']=""
		else:
			form.errors['ddbranch']="&nbsp;Invalid "
			error=1
		formerror={"error":""}
		if error==1:
			formerror['error']="Some of the fields are invalid. Please check. "	
		if self.check_id(form.values['erollno']):
			formerror['error']="Your application already exist.Try reprint application or send mail to admissions@fisat.ac.in."
			error=1
		
		if error==1:
			values={"formv":form.values,"forme":form.errors,"formerror":formerror}
			path = os.path.join(os.path.dirname(__file__), 'offlineapptemplate.html')
			
			self.response.out.write(template.render(path, values))
			
		else:
			appid=self.save_form(form)
			#self.print_pdf(form)
			self.redirect("/offsubmit?appid="+appid,permanent=True)		

class SubmitApp(webapp.RequestHandler):
		def check_id(self,appid):
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			try:		
				app=btechapp.fetch(1)[0]
				return True
			except:
				return False
		def get(self):
			if check_access()==False:
				self.redirect("/h404",permanent=True)
				return
			appid=self.request.get("appid").replace(" ","").replace("\\","").replace(".","")
			if self.check_id(appid):
				values={"form":{"appid":appid}}
				path = os.path.join(os.path.dirname(__file__), 'offappprint.html')
				self.response.out.write(template.render(path, values))
			else:
				self.redirect("/h404",permanent=True)
				
			
			




		


application = webapp.WSGIApplication(
                                     [('/offline', MainPage),
									 ('/offsubmit', SubmitApp),
									],	
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
