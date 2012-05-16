import sys
import os

sys.path.insert(0, 'reportlab.zip')

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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm,inch

folderFonts = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'

class MainPage(webapp.RequestHandler):
	def get(self):
		form=defaults()
		values={"formv":form.values,"forme":form.errors}
		path = os.path.join(os.path.dirname(__file__), 'apptemplate.html')
		self.response.out.write(template.render(path, values))
	def validate_name(self,name):
		USER_RE = re.compile("^[a-zA-Z][a-zA-Z ]+$")
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
		RE = re.compile("^[0-9]+$")
		return (RE.match(rollno)and(len(rollno)>erollno_length))
	def validate_erank(self,rank):
		RE = re.compile("^[0-9]+$")
		return (RE.match(rank))
	def validate_mark(self,mark):
		RE = re.compile("^[0-9-]+$")
		return (RE.match(mark))
	def validate_year(self,year):
		RE = re.compile("^[0-9-]+$")
		return (RE.match(year) and len(year)==4)
	
	def print_pdf(self,form):
		bulk="hi"
		self.response.headers['Content-Type'] = 'application/pdf'
		self.response.headers['Content-Disposition'] = 'attachment; filename=my.pdf'
		doc = SimpleDocTemplate(self.response.out,pagesize=letter,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)
		styles=getSampleStyleSheet()
		styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))		
		Story=[]
		Story.append(Paragraph(bulk, styles["Justify"]))
		Story.append(Spacer(1, 12))
		doc.build(Story)
	
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


	def save_form(self,form):
		btechapp=btechApp()
		btechapp.appcreatedby="system"
		appid=self.generate_id(form.values['erollno'],form.values['name'])
		btechapp.appid=appid
		btechapp.name=form.values["name"]
		btechapp.paddress=form.values["paddress"]
		btechapp.resphone=form.values["resphone"]
		btechapp.mobphone=form.values["mobphone"]
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
		btechapp.dddate=form.values["dddate"]
		btechapp.ddbank=form.values["ddbank"]
		btechapp.ddbranch=form.values["ddbranch"]
		btechapp.put()
		return appid

		
	def post(self):
		form=defaults()
		form.values["name"]=self.request.get("name").strip()
		form.values["paddress"]=self.request.get("paddress").strip().replace("\n"," ").replace("\r"," ")
		form.values["resphone"]=self.request.get("resphone").strip()
		form.values["mobphone"]=self.request.get("mobphone").strip()
		form.values["panchayath"]=self.request.get("panchayath").strip()
		form.values["inpanchayath"]=self.request.get("inpanchayath").strip()
		form.values["samepaddress"]=self.request.get("samepaddress").strip()
		form.values["caddress"]=self.request.get("caddress").strip().replace("\n"," ").replace("\r"," ")
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
		form.values["fatheraddress"]=self.request.get("fatheraddress").strip().replace("\n"," ").replace("\r"," ")
		form.values["fatherphone"]=self.request.get("fatherphone").strip()
		form.values["mothername"]=self.request.get("mothername").strip()
		form.values["motheremployed"]=self.request.get("motheremployed").strip()
		form.values["motherocc"]=self.request.get("motherocc").strip()
		form.values["motherdesig"]=self.request.get("motherdesig").strip()
		form.values["motheraddress"]=self.request.get("motheraddress").strip().replace("\n"," ").replace("\r"," ")
		form.values["motherphone"]=self.request.get("motherphone").strip()
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
		form.values["insaddress"]=self.request.get("insaddress").strip().replace("\n"," ").replace("\r"," ")
		form.values["insphone"]=self.request.get("insphone").strip()
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
		form.values["extra"]=self.request.get("extra").strip().replace("\n"," ").replace("\r"," ")
		form.values["addinfo"]=self.request.get("addinfo").strip().replace("\n"," ").replace("\r"," ")
		form.values["ddno"]=self.request.get("ddno").strip()
		form.values["dddate"]=self.request.get("dddate").strip()
		form.values["ddbank"]=self.request.get("ddbank").strip()
		form.values["ddbranch"]=self.request.get("ddbranch").strip()
		
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
		if form.values['panchayath']=="Others":
			form.values['panchayath']=form.values['inpanchayath']
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
			form.errors['erollno']="&nbsp;Invalid Roll No"
			error=1
		if self.validate_erank(form.values['erank']):
			form.errors['erank']=""
			
		else: 		
			form.errors['erank']="&nbsp;Invalid Rank"
			error=1 

		if self.validate_mark(form.values['epcmark']):
			form.errors['epcmark']=""
			
		else: 		
			form.errors['epcmark']="&nbsp;Invalid  Mark"
			error=1 

		if self.validate_mark(form.values['epcmaxmark']):
			form.errors['epcmaxmark']=""
			
		else: 		
			form.errors['epcmaxmark']="&nbsp;Invalid Mark"
			error=1 
		
		if self.validate_mark(form.values['emmark']):
			form.errors['emmark']=""
			
		else: 		
			form.errors['emmark']="&nbsp;Invalid  Mark"
			error=1 

		if self.validate_mark(form.values['emmaxmark']):
			form.errors['emmaxmark']=""
			
		else: 		
			form.errors['emmaxmark']="&nbsp;Invalid Mark"
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
			form.errors['qualexamyear']="&nbsp;Invalid Year"
			error=1
		if len(form.values['qualexamno'])>qualexamno_length:
			form.errors['nation']=""
			
		else: 		
			form.errors['qualexamno']="&nbsp;Invalid Roll No"
			error=1 		
		if	form.values['qualexam']=='Others':
			if len(form.values['inqualexam'])>qualexam_length:
				form.errors['inqualexam']=""
			else:
				form.errors['inqualexam']="Invalid Exam Name"
		if len(form.values['qualboard'])>qualboard_length:
			form.errors['qualboard']=""
		else:
			form.errors['qualboard']="Invalid Board Name"
		
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
		if error==1:
			values={"formv":form.values,"forme":form.errors}
			path = os.path.join(os.path.dirname(__file__), 'apptemplate.html')
			self.response.out.write(template.render(path, values))
			
		else:
			appid=self.save_form(form)
			#self.print_pdf(form)
			self.redirect("/submit?appid="+appid,permanent=True)		

class SubmitApp(webapp.RequestHandler):
		def get(self):
			appid=self.request.get("appid")
			values={"form":{"appid":appid}}
			path = os.path.join(os.path.dirname(__file__), 'appprint.html')
			self.response.out.write(template.render(path, values))

class PrintApp(webapp.RequestHandler):
	def add_space(self,no):
		spaces=""
		for i in range(0,no):
			spaces=spaces+"&nbsp;"
		return spaces

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
		doc = SimpleDocTemplate(self.response.out,pagesize=A4,rightMargin=40,leftMargin=10,topMargin=10,bottomMargin=10)
		styles=getSampleStyleSheet()
		styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))		
		styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
		styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
		styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))	
		

		nametext=Paragraph("<para fontSize=10>Name:</para>",styles["Left"])
		name=Paragraph("<para fontSize=10><b>%s</b></para>" % app.name,styles["Left"])
		paddresstext=Paragraph("<para fontSize=10>Permanent Address:</para>",styles["Left"])
		caddress=Paragraph("<para fontSize=10><b>%s</b></para>" % app.caddress,styles["Left"])
		caddresstext=Paragraph("<para fontSize=10>Communication Address:</para>",styles["Left"])
		paddress=Paragraph("<para fontSize=10><b>%s</b></para>" % app.paddress,styles["Left"])
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
		fatherocc=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fatherocc),styles["Left"])
		fatherdesigtext=Paragraph("<para fontSize=10>Designation:</para>",styles["Left"])
		fatherdesig=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.fatherdesig),styles["Left"])
		fatheraddress=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		fatherphonetext=Paragraph("<para fontSize=10>Phone:</para>",styles["Left"])
		fatherphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.fatherphone,styles["Left"])
		fatheraddresstext=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		fatheraddress=Paragraph("<para fontSize=10><b>%s</b></para>" % app.fatheraddress,styles["Left"])
		mothernametext=Paragraph("<para fontSize=10>Mother's Name:</para>",styles["Left"])
		mothername=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.mothername),styles["Left"])
		motherocctext=Paragraph("<para fontSize=10>Occupation:</para>",styles["Left"])
		motherocc=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.motherocc),styles["Left"])
		motherdesigtext=Paragraph("<para fontSize=10>Designation:</para>",styles["Left"])
		motherdesig=Paragraph("<para fontSize=10><b>%s</b></para>" % self.chopline(app.motherdesig),styles["Left"])
		motheraddresstext=Paragraph("<para fontSize=10>Address:</para>",styles["Left"])
		motheraddress=Paragraph("<para fontSize=10><b>%s</b></para>" % app.motheraddress,styles["Left"])
		motherphonetext=Paragraph("<para fontSize=10>Phone:</para>",styles["Left"])
		motherphone=Paragraph("<para fontSize=10><b>%s</b></para>" % app.motherphone,styles["Left"])
		

		mfboaesmemnotext=Paragraph("<para fontSize=10>FBOAES(Member) Membership No:</para>",styles["Left"])
		mfboaesmemno=Paragraph("<para fontSize=10><b>%s</b></para>" % app.mfboaesmemno,styles["Left"])
		pfboaesmemnotext=Paragraph("<para fontSize=10>FBOAES(Patron) Membership No:</para>",styles["Left"])
		pfboaesmemno=Paragraph("<para fontSize=10><b>%s</b></para>" % app.pfboaesmemno,styles["Left"])
		incometext=Paragraph("<para fontSize=10>Annual Income</para>",styles["Left"])
		income=Paragraph("<para fontSize=10><b>%s</b></para>" % app.income,styles["Left"])
		eexamtext=Paragraph("<para fontSize=12><b>Kerala Entrance 2012 </b></para>",styles["Left"])
		erollnotext=Paragraph("<para fontSize=10>Roll No</para>",styles["Left"])
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
		
		

		data=[[paddresstext,paddress,caddresstext,caddress],
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
				[incometext,income],
				[eexamtext,"",qualexamdtltext,""],
				[erollnotext,erollno,qualexamtext,qualexam],
				[eranktext,erank,qualexamboardyear,qualexamno],
				[epcmarks,emmarks,qpmarks,qcmarks,qmmarks],
				[PageBreak()]	]
		
		appidtext='<para fontSize=12>APPLICATION ID:%s %sINSTITUTE COPY</b></para>' %(appid,self.add_space(50))
		institle=Paragraph("<para fontSize=15>FEDERAL INSTITUTE OF SCIENCE AND TECHNOLOGY (FISAT)<font size='10'><super>TM</super></font></para>",styles["Center"])
		iso=Paragraph("<para fontSize=10>(ISO 9001 :2000 Certitied Engineering College managed by the Federal Bank Officer's Association Educational Society)</para>",styles["Center"])
		address=Paragraph("<para fontSize=11><b>HORMIS NAGAR, MOOKANNOOR P.O., ANGAMALY - 683 577, KERALA</b></para>",styles["Center"])
		approval=Paragraph("<para fontSize=11>(Approved by AICTE - Affiliated to Mahatma Gandhi University, Kottayam)</para>",styles["Center"])
		web=Paragraph("<para fontSize=11>Website: www.fisat.ac.in E-mail: mai@fisat.ac.in</para>",styles["Center"])	
		
		titletable=Table([[institle],[iso],[address],[approval],[web]])
		titletable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
								]))
		
		barcode=code39.Extended39(appid,barWidth=0.5*mm,barHeight=15*mm,humanReadable=True)		
		photo=Image('photo.jpg',2.1*inch, 2.1*inch)
		Category=Paragraph("<para fontSize=10><b>Category:General</b><br/><br/><br/></para>",styles["Left"])
		datatable=Table(data)
		datatable.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
								('VALIGN',(0,0),(-1,-1),'TOP'),
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
								]))
		App=[]
		App.append(Paragraph(appidtext, styles["Justify"]))
		App.append(Spacer(3, 12))
		App.append(titletable)
		App.append(Spacer(1, 12))
		App.append(infotable)
		App.append(Spacer(3, 12))
		App.append(datatable)
		doc.build(App)
		

application = webapp.WSGIApplication(
                                     [('/', MainPage),
									 ('/print', PrintApp),
									('/submit', SubmitApp)],	
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
