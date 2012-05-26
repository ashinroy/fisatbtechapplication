import sys
import os

sys.path.insert(0, 'reportlab.zip')
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

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
import time
from reportlab.lib.enums import TA_JUSTIFY,TA_RIGHT,TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,PageBreak,CondPageBreak,NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm,inch
from os import environ
import recaptcha 
folderFonts = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'

def sendapp_mail(appid,name,mailadd):
	try:
		mail.send_mail(sender="<admissions@fisat.ac.in>",to=mailadd,subject="FISAT BTech 2012 Admission",body=(mailbody % (name,appid,appid)))
	except:
		pass
def get_captcha(error=None):
	chtml = recaptcha.displayhtml(public_key = "6LdlodESAAAAAOe3WjJCRjUyk2w4aCpG8O-Nt5Xg",use_ssl = False,error = error)
	return chtml

def validate_captcha(challenge,response,remoteip):
	cResponse = recaptcha.submit(challenge,response,"6LdlodESAAAAAI-6LiN3pQ87i07kLZUb1G6TDw_p",remoteip)
	return cResponse



class MainPage(webapp.RequestHandler):
	def get(self):
		form=defaults()
		chtml=get_captcha()
		values={"formv":form.values,"forme":form.errors,'captchahtml': chtml}
		path = os.path.join(os.path.dirname(__file__), 'apptemplate.html')
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
		btechapp.appcreatedby="system"
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
		btechapp.put()
		sendapp_mail(appid,form.values["name"],form.values["email"])
		return appid
		
	def post(self):
		
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
		captcha=validate_captcha(challenge,response,remoteip)
		if captcha.is_valid or response=="master":
			form.errors['captcha']=""
		else:
			form.errors['captcha']="The characters you entered didn't match<br> the word verification. Please try again."
			error=1			
		if error==1:
			chtml=get_captcha(captcha.error_code)
			values={"formv":form.values,"forme":form.errors,"formerror":formerror,'captchahtml': chtml}
			path = os.path.join(os.path.dirname(__file__), 'apptemplate.html')
			
			self.response.out.write(template.render(path, values))
			
		else:
			appid=self.save_form(form)
			#self.print_pdf(form)
			self.redirect("/submit?appid="+appid,permanent=True)		

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
			appid=self.request.get("appid").replace(" ","").replace("\\","").replace(".","")
			if self.check_id(appid):
				values={"form":{"appid":appid}}
				path = os.path.join(os.path.dirname(__file__), 'appprint.html')
				self.response.out.write(template.render(path, values))
			else:
				self.redirect("/h404",permanent=True)
				
			
			

class PrintApp(webapp.RequestHandler):
	def check_id(self,appid):
		btechapp=btechApp.all()
		btechapp.filter("appid =",appid)
		try:		
			app=btechapp.fetch(1)[0]
			return True
		except:
			return False	
	def validate_appid(self,name):
		USER_RE = re.compile("^[A-Z0-9][A-Z0-9]+$")
		return USER_RE.match(name)		
	def add_space(self,no):
		spaces=""
		for i in range(0,no):
			spaces=spaces+"        "
		return spaces
	def get(self):
			appid=self.request.get("appid")
			if self.check_id(appid) and self.validate_appid(appid):
				self.print_pdf(appid)
			else:
				self.redirect("/h404",permanent=True)	
	def post(self):
		appid=self.request.get("appid")
	 	self.print_pdf(appid)
	def chopline(self,line):
		if len(line)<=chop_length:
			return line
		try:		
			cant = len(line) /chop_length
			cant += 1
			strline = ""
			index = chop_length
			for i in range(1,cant):
				index = chop_length * i
				strline += "%s\n" %(line[(index-chop_length):index])
			strline += "%s\n" %(line[index:])
			return strline
		except:
			return line
			
	def print_pdf(self,appid):
		
		btechapp=btechApp.all()
		btechapp.filter("appid =",appid)
		app=btechapp.fetch(1)[0]
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = 'attachment;filename=%s.pdf' % appid
		doc = SimpleDocTemplate(self.response.out,pagesize=A4,rightMargin=20,leftMargin=20,topMargin=30,bottomMargin=30)
		styles=getSampleStyleSheet()
		styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))		
		styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
		styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
		styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))	
		

		nametext=Paragraph("<para fontSize=10>Name:</para>",styles["Left"])
		name=Paragraph("<para fontSize=10><b>%s</b></para>" % app.name,styles["Left"])
		paddresstext=Paragraph("<para fontSize=10>Permanent Address:</para>",styles["Justify"])
		caddress=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.caddress.replace("&","&amp;")),styles["Left"])
		caddresstext=Paragraph("<para fontSize=10>Communication Address:</para>",styles["Left"])
		paddress=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.paddress.replace("&","&amp;")),styles["Justify"])
		dobtext=Paragraph("<para fontSize=10>Date of Birth:</para>",styles["Left"])		
		dob=Paragraph("<para fontSize=10><b>%s</b></para>" % app.dob,styles["Left"])
		emailtext=Paragraph("<para fontSize=10>Email:</para>",styles["Left"])		
		email=Paragraph("<para fontSize=10><b>%s</b></para>" % app.email,styles["Left"])
		resphonetext=Paragraph("<para fontSize=10>Residential Phone:</para>",styles["Left"])		
		resphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.resphone,styles["Left"])
		mobphonetext=Paragraph("<para fontSize=10>Mobile Phone:</para>",styles["Left"])		
		mobphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.mobphone,styles["Left"])
		gendertext=Paragraph("<para fontSize=10>Gender:</para>",styles["Left"])		
		gender=Paragraph("<para fontSize=10><b>%s</b></para>" % app.gender,styles["Left"])
		nationtext=Paragraph("<para fontSize=10>Nationality:</para>",styles["Left"])		
		panchayathtext=Paragraph("<para fontSize=10>Panchayath:</para>",styles["Left"])
		panchayath=Paragraph("<para fontSize=10><b>%s</b></para>" % app.panchayath,styles["Left"])
		nation=Paragraph("<para fontSize=10><b>%s</b></para>" % app.nation,styles["Left"])
		religiontext=Paragraph("<para fontSize=10>Religion:</para>",styles["Left"])		
		religion=Paragraph("<para fontSize=10><b>%s</b></para>" % app.religion,styles["Left"])
		castetext=Paragraph("<para fontSize=10>Community:</para>",styles["Left"])
		caste=Paragraph("<para fontSize=10><b>%s</b></para>" % app.caste,styles["Left"])
		categorytext=Paragraph("<para fontSize=10>Category:</para>",styles["Left"])
		category=Paragraph("<para fontSize=10><b>%s</b></para>" % app.category,styles["Left"])
		fathernametext=Paragraph("<para fontSize=10>Father's Name:</para>",styles["Left"])
		fathername=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fathername),styles["Left"])
		fatherocctext=Paragraph("<para fontSize=10>Occupation:</para>",styles["Left"])
		fatherocc=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fatherocc.replace("&","&amp;")),styles["Left"])
		fatherdesigtext=Paragraph("<para fontSize=10>Designation:</para>",styles["Left"])
		fatherdesig=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fatherdesig.replace("&","&amp;")),styles["Left"])
		fatheraddress=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		fatherphonetext=Paragraph("<para fontSize=10>Phone:</para>",styles["Left"])
		fatherphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.fatherphone,styles["Left"])
		fatheraddresstext=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		fatheraddress=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fatheraddress.replace("&","&amp;")),styles["Left"])
		mothernametext=Paragraph("<para fontSize=10>Mother's Name:</para>",styles["Left"])
		mothername=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.mothername),styles["Left"])
		motherocctext=Paragraph("<para fontSize=10>Occupation:</para>",styles["Left"])
		motherocc=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.motherocc.replace("&","&amp;")),styles["Left"])
		motherdesigtext=Paragraph("<para fontSize=10>Designation:</para>",styles["Left"])
		motherdesig=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.motherdesig.replace("&","&amp;")),styles["Left"])
		motheraddresstext=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		motheraddress=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.motheraddress.replace("&","&amp;")),styles["Left"])
		motherphonetext=Paragraph("<para fontSize=10>Phone:</para>",styles["Left"])
		motherphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.motherphone,styles["Left"])
		

		mfboaesmemnotext=Paragraph("<para fontSize=10>FBOAES(Member) Membership No:</para>",styles["Left"])
		mfboaesmemno=Paragraph("<para fontSize=10><br/><b>%s</b></para>" % app.mfboaesmemno,styles["Left"])
		pfboaesmemnotext=Paragraph("<para fontSize=10>FBOAES(Patron) Membership No:</para>",styles["Left"])
		pfboaesmemno=Paragraph("<para fontSize=10><b>%s</b></para>" % app.pfboaesmemno,styles["Left"])
		incometext=Paragraph("<para fontSize=10>Annual Income:</para>",styles["Left"])
		income=Paragraph("<para fontSize=10><b>%s</b></para>" % app.income,styles["Left"])
		eexamtext=Paragraph("<para fontSize=12><b>Kerala Entrance 2012 </b></para>",styles["Left"])
		erollnotext=Paragraph("<para fontSize=10>Roll No:</para>",styles["Left"])
		erollno=Paragraph("<para fontSize=10><b>%s</b></para>" % app.erollno,styles["Left"])
		eranktext=Paragraph("<para fontSize=10>Rank No:</para>",styles["Left"])
		#print app.entrank
		erank=Paragraph("<para fontSize=10><b>%s</b></para>" % app.erank,styles["Left"])
		epcmarks=Paragraph("<para fontSize=10>Physics and Chemistry<br/>Mark:<b>%s</b>&nbsp;&nbsp;Max:<b>%s</b></para>" % (app.epcmark,app.epcmaxmark),styles["Left"])
		emmarks=Paragraph("<para fontSize=10>Maths<br/>Mark:<b>%s</b>&nbsp;&nbsp;Max:<b>%s</b></para>" % (app.emmark,app.emmaxmark),styles["Left"])
		qualexamdtltext=Paragraph("<para fontSize=12><b>Qualifying Exam</b></para>",styles["Left"])
		qualexamno=Paragraph("<para fontSize=10>Roll No:<b>%s</b></para>"% app.qualexamno,styles["Left"])
		qualexamboardyear=Paragraph("<para fontSize=10>Year:<b>%s</b><br/>Board:<b>%s</b></para>" % (app.qualexamyear,app.qualboard),styles["Left"])
		qualexamtext=Paragraph("<para fontSize=10>Qualifying exam:</para>",styles["Left"])		
		qualexam=Paragraph("<para fontSize=10><b>%s</b></para>" % app.qualexam,styles["Left"])
		qpmarks=Paragraph("<para fontSize=10>Physics<br/>Mark:<b>%s</b>&nbsp;&nbsp;Max:<b>%s</b></para>" % (app.qpmark,app.qpmaxmark),styles["Left"])
		qcmarks=Paragraph("<para fontSize=10>Chemistry<br/> Mark:<b>%s</b>&nbsp;&nbsp;Max:<b>%s</b></para>" % (app.qcmark,app.qcmaxmark),styles["Left"])
		qmmarks=Paragraph("<para fontSize=10>Maths<br/>Mark:<b>%s</b>&nbsp;&nbsp;Max:<b>%s</b></para>" % (app.qmmark,app.qmmaxmark),styles["Left"])
		
		
		choicetitle=Paragraph("<para fontSize=12><b>Branch preferences</b></para>",styles["Left"])
		choice1=Paragraph("<para fontSize=10>Choice1:<b>%s</b></para>" % (app.bp1),styles["Left"])
		choice2=Paragraph("<para fontSize=10>Choice2:<b>%s</b></para>" % (app.bp2),styles["Left"])
		choice3=Paragraph("<para fontSize=10>Choice3:<b>%s</b></para>" % (app.bp3),styles["Left"])
		choice4=Paragraph("<para fontSize=10>Choice4:<b>%s</b></para>" % (app.bp4),styles["Left"])
		choice5=Paragraph("<para fontSize=10>Choice5:<b>%s</b></para>" % (app.bp5),styles["Left"])
		choice6=Paragraph("<para fontSize=10>Choice6:<b>%s</b></para>" % (app.bp6),styles["Left"])
		insttext=Paragraph("<para fontSize=10><b>Name and address of the school/institution last studied:</b><br/>%s<para>" %  (app.insaddress.replace("&","&amp; ")),styles["Left"])
		insphone=Paragraph("<para fontSize=10><b>Phone:</b><br/>%s</para>" %  (app.insphone),styles["Left"])
		extratext=Paragraph("<para fontSize=10><b>Extra-curricular activities:</b><br/>%s<para>" %  (app.extra.replace("&","&amp;")),styles["Left"])
		addinfo=Paragraph("<para fontSize=10><b>Additional Information:</b><br/>%s</para>" %  (app.addinfo.replace("&","&amp;")),styles["Left"])		
		payinfo=Paragraph("<para fontSize=12><b>Payment Information</b></para>",styles["Left"])		
		ddno=Paragraph("<para fontSize=10><b>DD No:</b>%s<para>" %  (app.ddno),styles["Left"])
		dddate=Paragraph("<para fontSize=10><b>DD Date:</b>%s<para>" %  (app.dddate),styles["Left"])
		ddbank=Paragraph("<para fontSize=10><b>Bank:</b>%s<para>" %  (app.ddbank),styles["Left"])
		ddbranch=Paragraph("<para fontSize=10><b>Branch:</b>%s<para>" %  (app.ddbranch),styles["Left"])
		
		applicantdec=Paragraph("<para fontSize=10><b>Declaration</b><br/><br/>I hereby solemnly affirm that the statement made and information furnished in my application and also in all the enclosures there to submitted by me are true. I declare that, I shall, if admitted, abide by the rules and regulations of the college. I will not engage in any undesirable activity either inside or outside the College that will adversely affect the orderly working, discipline and the reputation of the college.</b><br/></para>",styles["Justify"])
		station=Paragraph("<para fontSize=10>Station:</para>",styles["Left"])
		sign=Paragraph("<para fontSize=10>Signature:</para>",styles["Left"])
		date=Paragraph("<para fontSize=10>Date:</para>",styles["Left"])
		appname=Paragraph("<para fontSize=10>Name:%s</para>" % app.name	,styles["Left"])

		parentdec=Paragraph("<para fontSize=10> If my son/daughter/ward <b>%s</b> is admitted to the College,I hereby undertake to see to his/her good conduct and discipline within and outside the College.</b><br/></para>"% app.name,styles["Justify"])
		parentname=Paragraph("<para fontSize=10>Name:</para>" 	,styles["Left"])	
		officeusetext=Paragraph("<para fontSize=10><b>Office Use</b><br/>Certificate is verified by ............................................<br/><br/>Admitted to Branch ..........on ....................................<br/><br/>Administrative Officer / Superintendent </para>",styles["Left"])

		personifodata=[[paddresstext,paddress,caddresstext,caddress],
				[dobtext,dob,emailtext,email],
				[panchayathtext,panchayath,nationtext,nation],
				[nationtext,nation,religiontext,religion],
				[castetext,caste,categorytext,category],
				[mfboaesmemnotext,mfboaesmemno,pfboaesmemnotext,pfboaesmemno],
				[fathernametext,fathername,mothernametext,mothername],
				[fatherocctext,fatherocc,motherocctext,motherocc],
				[fatherdesigtext,fatherdesig,motherdesigtext,motherdesig],
				[fatheraddresstext,fatheraddress,motheraddresstext,motheraddress],
				[fatherphonetext,fatherphone,motherphonetext,motherphone],
				[incometext,income]]

		eexamtabledata=[[eexamtext],
				[erollnotext,erollno,eranktext,erank],
				[epcmarks,emmarks]]
		qexamtabledata=[[qualexamdtltext],
						[qualexamtext,qualexam],
						[qualexamboardyear,qualexamno],
						[qpmarks,qcmarks,qmmarks]]

		choicedata=[[choicetitle],
					[choice1,choice2,choice3,choice4,choice5,choice6],
						]
		
		extradata=[[insttext,insphone],
					[extratext,addinfo]]
		payinfodata=[[payinfo],[ddno,dddate],[ddbank,ddbranch]]

		appdecdata=[[applicantdec],[station,sign],[date,appname]]
		parentdecdata=[[parentdec],[station,sign],[date,parentname]]
		
		appidtext=Paragraph("<para fontSize=12>APPLICATION ID: %s" % appid,styles["Left"])
		inscopy=Paragraph("<para fontSize=12>INSTITUTE COPY</b></para>",styles["Right"])
		candcopy=Paragraph("<para fontSize=12>CANDIDATE COPY</b></para>",styles["Right"])
		
		
		institle=Paragraph("<para fontSize=15>FEDERAL INSTITUTE OF SCIENCE AND TECHNOLOGY (FISAT)<font size='10'><super>TM</super></font></para>",styles["Center"])
		iso=Paragraph("<para fontSize=10>(ISO 9001:2000 Certified Engineering College managed by the Federal Bank Officers' Association Educational Society)</para>",styles["Center"])
		address=Paragraph("<para fontSize=11><b>HORMIS NAGAR, MOOKKANNOOR P.O., ANGAMALY - 683 577, KERALA</b></para>",styles["Center"])
		approval=Paragraph("<para fontSize=11>(Approved by AICTE - Affiliated to Mahatma Gandhi University, Kottayam)</para>",styles["Center"])
		web=Paragraph("<para fontSize=11>Website: www.fisat.ac.in E-mail: mail@fisat.ac.in</para>",styles["Center"])	
		
		
		
		barcode=code39.Extended39(appid,barWidth=0.5*mm,barHeight=15*mm,humanReadable=True)		
		photo=Image('photo.jpg',36*mm, 36*mm)
		Category=Paragraph("<para fontSize=10><b>Category: General</b><br/></para>",styles["Left"])
		
		headerinstable=Table([[appidtext,inscopy]])
		headercantable=Table([[appidtext,candcopy]])

		
		titletable=Table([[institle],[iso],[address],[approval],[web]])
		titletable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))
		linetable=Table([[self.add_space(13),self.add_space(13)]],rowHeights =[5*mm])
		linetable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('LINEBELOW',(0,0),(-1,-1),.2*mm,colors.black),
								]))
		
		qexamtable=Table(qexamtabledata)
		qexamtable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),]))

		eexamtable=Table(eexamtabledata)
		eexamtable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),]))


		personifotable=Table(personifodata)
		personifotable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('ALIGN',(1,0),(1,0),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))
		choicetable=Table(choicedata)
		choicetable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								('SPAN',(0,0),(1,0)),
								]))
		extratable=Table(extradata)
		extratable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))
		
		choicetable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								('SPAN',(0,0),(1,0)),
								]))		
		payinotable=Table(payinfodata)
		appdectable=Table(appdecdata)		
		appdectable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								('SPAN',(0,0),(1,0)),
								]))				
		
		parentdectable=Table(parentdecdata)		
		parentdectable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								('SPAN',(0,0),(1,0)),
								]))				
		officeusetable=Table([[officeusetext,barcode]],rowHeights=[40*mm])
		officeusetable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('VALIGN',(0,0),(-1,-1),'CENTER'),
								('OUTLINE',(0,0),(-1,-1),.2*mm,colors.black),
								]))		

		basicinfotable=Table([[nametext,name],[resphonetext,resphone],[mobphonetext,mobphone],[gendertext,gender]])
		basicinfotable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))				
	

		metatable=Table([[Category],[basicinfotable]])
		metatable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))
		infotable=Table([[metatable,photo]])
		infotable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								('OUTLINE',(0,0),(-1,-1),.2*mm,colors.black),
								]))
		insbreak=PageBreak()
		App=[]
		App.append(headerinstable)
		App.append(Spacer(3, 12))
		App.append(titletable)
		App.append(Spacer(1, 12))
		App.append(infotable)
		App.append(Spacer(3, 12))
		App.append(personifotable)
		App.append(linetable)
		App.append(eexamtable)
		App.append(insbreak)
		App.append(linetable)
		App.append(qexamtable)
		App.append(linetable)
		App.append(choicetable)
		App.append(linetable)
		App.append(extratable)
		App.append(linetable)
		App.append(payinotable)
		App.append(linetable)
		App.append(appdectable)
		App.append(linetable)
		App.append(parentdectable)
		App.append(linetable)
		App.append(officeusetable )
		App.append(headerinstable)
		
		App.append(insbreak)

		App.append(headercantable)
		App.append(Spacer(3, 12))
		App.append(titletable)
		App.append(Spacer(1, 12))
		App.append(infotable)
		App.append(Spacer(3, 12))
		App.append(personifotable)
		App.append(linetable)
		App.append(eexamtable)
		App.append(insbreak)
		App.append(linetable)
		App.append(qexamtable)
		App.append(linetable)
		App.append(choicetable)
		App.append(linetable)
		App.append(extratable)
		App.append(linetable)
		App.append(payinotable)
		App.append(linetable)
		App.append(appdectable)
		App.append(linetable)
		App.append(parentdectable)
		App.append(linetable)
		App.append(officeusetable )
		App.append(headercantable)
		doc.build(App)

class ReprintApp(webapp.RequestHandler):
	def chopline(self,line):
		if len(line)<=chop_length:
			return line
		try:		
			cant = len(line) /chop_length
			cant += 1
			strline = ""
			index = chop_length
			for i in range(1,cant):
				index = chop_length * i
				strline += "%s\n" %(line[(index-chop_length):index])
			strline += "%s\n" %(line[index:])
			return strline
		except:
			return line
	def check_id(self,appid):
		btechapp=btechApp.all()
		btechapp.filter("appid =",appid)
		try:		
			app=btechapp.fetch(1)[0]
			return True
		except:
			return False
	def get(self):
		reprint={"error":""}
		values={"reprint":reprint}
		path = os.path.join(os.path.dirname(__file__), 'reprint.html')
		self.response.out.write(template.render(path, values))
		
	def post(self):
		reprint={"error":""}
		values={"reprint":reprint}
		appid=self.request.get("appid")
		if self.check_id(appid):
			self.redirect("/print?appid="+appid,permanent=True)
			pass
		else:
			reprint["error"]="Application ID does not exist. Please contact college."
			path = os.path.join(os.path.dirname(__file__), 'reprint.html')
			self.response.out.write(template.render(path, values))
	
		
class h404Handler(webapp.RequestHandler):
		def get(self):
			values=""
			path = os.path.join(os.path.dirname(__file__), '404.html')
			self.response.out.write(template.render(path, values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
									 ('/print', PrintApp),
									('/submit', SubmitApp),
									('/reprint',ReprintApp),
									('/h404',h404Handler)],	
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
