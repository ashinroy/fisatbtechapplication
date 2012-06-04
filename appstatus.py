import os


from google.appengine.dist import use_library
use_library('django', '0.96')

from google.appengine.api import mail
from google.appengine.ext.webapp import template
import cgi
import csv
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from defaults import *
from models import * 

from os import environ

def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips

class FillDefaults(webapp.RequestHandler):
	def get(self):
		if check_access():
			btechapp=btechApp.all()
			btechapp.filter("appstatus =",None)
			apps=btechapp.fetch(limit=5000)
			for app in apps:
				app.appstatus=defstatus[0][0]
				app.put()
			for status in defstatus:
				statusentry=appStatus()
				statusentry.keyword=status[0]
				statusentry.status=status[1]
				statusentry.desc=status[2]
				statusentry.put()
			



class ShowStatus(webapp.RequestHandler):
	def get_status(self,rollno):
		btechapp=btechApp.all()
		btechapp.filter("erollno =",rollno)
		app=btechapp.fetch(1)[0]
		if app.appstatus==None:
			return appstatus_null % rollno
		else:
			try:
				status_keyword=app.appstatus
				status_dtl=appStatus.all()
				status_dtl.filter("keyword =",status_keyword)
				statusen=status_dtl.fetch(1)[0]
				statustable="""<tr><td>%s</td><td>%s</td><td>%s</td><tr>""" %(app.name,statusen.status,statusen.desc)
				return statustable
			except:
				return """<tr><td></td><td>Contact college</td><td></td><tr>"""
			

	def check_id(self,rollno):
		btechapp=btechApp.all()
		btechapp.filter("erollno =",rollno)
		try:		
			app=btechapp.fetch(1)[0]
			return True
		except:
			return False	
	def get(self):
		status={"error":"","appstatustable":""}
		values={"status":status}
		path = os.path.join(os.path.dirname(__file__), 'appstatus.html')
		self.response.out.write(template.render(path, values))
	def post(self):
		status={"error":"","appstatustable":""}
		values={"status":status}
		appid=self.request.get("appid").strip()
		if appid.find('F')>-1:
			rollno=appid[5:]
		else:
			rollno=appid
		if self.check_id(rollno):
			status["appstatustable"]=self.get_status(rollno)
			path = os.path.join(os.path.dirname(__file__), 'appstatus.html')
			self.response.out.write(template.render(path, values))
		else:
			status["error"]="Application ID does not exist. Please contact college."
			path = os.path.join(os.path.dirname(__file__), 'appstatus.html')
			self.response.out.write(template.render(path, values))
	



application = webapp.WSGIApplication(
                                     [('/status',ShowStatus),
									  ('/filldb',FillDefaults)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
