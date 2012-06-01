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
			apps=btechapp.fetch(max_apps)
			stream.writerow(['AppID','Name','ResPh','MobPh','Panchayath','PAddress','Caddress','DOB','Gender','EntROllNo','EntPCMark','EntMMarks',
							'QualBoard','QualYear','QualExamNo','QualExam','QualPmark','QualPMax','QualCMark','QualCMax','QualMMark','QualMMax',
							'Choice1','Choice2','Choice3','Choice4','Choice5','Choice6','DDNo','DDBank'])
			for app in apps:
				stream.writerow([app.appid,app.name,app.resphone,app.mobphone,
				app.panchayath,app.paddress,app.caddress,app.dob,app.gender,
				app.erollno,app.epcmark,app.emmark,
				app.qualboard,app.qualexamyear,app.qualexamno,app.qualexam,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,
				app.bp1,app.bp2,app.bp3,app.bp4,app.bp5,app.bp6,app.ddno,app.ddbank])
		
class Search(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
		results={"result":""}
		values={"results":results}
		path = os.path.join(os.path.dirname(__file__), 'search.html')
		self.response.out.write(template.render(path, values))

		
application = webapp.WSGIApplication(
                                     [('/download', Download),
									 ('/search', Search)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

