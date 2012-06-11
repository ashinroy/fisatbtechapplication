import sys
import os


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

def getSNo(erollno):
	try:
		smap=serialNoMap.all()
		smap.filter("erollno =",erollno)
		serialno=smap.fetch(1)[0]
		return serialno.sno
	except:
		return dsno


def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips

class Download(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=application.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.order('applieddtime')
			apps=btechapp.fetch(max_apps)
			stream.writerow(['SNo','AppID','Name','ResPh','MobPh','Panchayath','PAddress','Caddress','DOB','Gender','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax',
							'Choice1','Choice2','Choice3','Choice4','Choice5','Choice6','DDNo','DDBank','CreatedBy'])
			for app in apps:
				sno=getSNo(app.erollno)				
				stream.writerow([sno,app.appid,app.name,app.resphone,app.mobphone,
				app.panchayath,app.paddress,app.caddress,app.dob,app.gender,
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
				app.bp1,app.bp2,app.bp3,app.bp4,app.bp5,app.bp6,app.ddno,app.ddbank,app.appcreatedby])

class VDownload(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=application.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.order('name')
			apps=btechapp.fetch(max_apps)
			
			stream.writerow(['No','SNo','AppID','Name','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax',
							])
			i=1
			for app in apps:
				sno=getSNo(app.erollno)
				stream.writerow([str(i),sno,app.appid,app.name.upper(),
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
				])
				i=i+1
class RLDownload(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=applicationforranklist.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.order('name')
			apps=btechapp.fetch(max_apps)
			
			stream.writerow(['No','SNo','AppID','Name','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax','AppStatus'
							])
			i=1
			for app in apps:
				sno=getSNo(app.erollno)
				stream.writerow([str(i),sno,app.appid,app.name.upper(),
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
				app.appstatus])
				i=i+1
class MKDownload(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=applicationmookannoor.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.filter('panchayath =','MKR')
			apps=btechapp.fetch(max_apps)
			stream.writerow(['No','SNo','AppID','Name','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax','PAddress','CAddress'
							])
			i=1
			for app in apps:
				sno=getSNo(app.erollno)
				stream.writerow([str(i),sno,app.appid,app.name.upper(),
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
				app.paddress,app.caddress
				])
				i=i+1
class FBPDownload(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=applicationfbspatron.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.filter('pfboaesmemno !=','NA')
			apps=btechapp.fetch(max_apps)
			stream.writerow(['No','SNo','AppID','Name','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax','MemNo','Fathername',
							'FatherDesig','Fatheroffice','Fatherphone','Mothername','MotheDesig','Motheroffice','Motherphone'])
			i=1
			for app in apps:
				sno=getSNo(app.erollno)
				stream.writerow([str(i),sno,app.appid,app.name.upper(),
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
			app.pfboaesmemno,app.fathername,app.fatherdesig,app.fatheraddress,app.fatherphone,app.mothername,app.motherdesig,app.motheraddress,app.motherphone])
				i=i+1
class FBMDownload(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			self.response.headers['Content-Type'] = 'text/csv'
			self.response.headers['Content-Disposition'] = 'attachment; filename=applicationfbsmember.csv'
			stream=csv.writer(self.response.out,delimiter='%',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			btechapp=btechApp.all()
			btechapp.filter('mfboaesmemno !=','NA')
			apps=btechapp.fetch(max_apps)
			stream.writerow(['No','SNo','AppID','Name','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax','MemNo','Fathername',
							'FatherDesig','Fatheroffice','Fatherphone','Mothername','MotheDesig','Motheroffice','Motherphone'])
			i=1
			for app in apps:
				sno=getSNo(app.erollno)
				stream.writerow([str(i),sno,app.appid,app.name.upper(),
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
			app.mfboaesmemno,app.fathername,app.fatherdesig,app.fatheraddress,app.fatherphone,app.mothername,app.motherdesig,app.motheraddress,app.motherphone])
				i=i+1
application = webapp.WSGIApplication(
                                     [('/download', Download),('/vdownload', VDownload),('/fbmdownload', FBMDownload),
									('/fbpdownload', FBPDownload),('/mkdownload', MKDownload),('/rldownload', RLDownload)
									],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

