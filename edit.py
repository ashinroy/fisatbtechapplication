import sys
import os


from google.appengine.dist import use_library
use_library('django', '0.96')


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


class EditStatus(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			allstatus={"status":""}
			canid={"appid":""}
			values={"allstatus":allstatus,"canid":canid}
			appid=self.request.get("appid")			
			canid['appid']=appid
			appstatus=appStatus.all()
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			app=btechapp.fetch(1)[0]
			statusall=appstatus.fetch(10)
			statusbuttons=""
			for status in statusall:
				if status.keyword==app.appstatus:
					 button="""<input type="radio" name="status" value="%s" checked>%s(%s)<br>""" % (status.keyword,status.status,status.desc) 
					 statusbuttons=statusbuttons+button
				else:
					 button="""<input type="radio" name="status" value="%s" >%s(%s)<br>""" % (status.keyword,status.status,status.desc) 
					 statusbuttons=statusbuttons+button
			allstatus['status']=statusbuttons
			path = os.path.join(os.path.dirname(__file__), 'editstatus.html')
			self.response.out.write(template.render(path, values))
		def post(self):
			if check_access()==False:
				return
			appid=self.request.get("appid")
			status=self.request.get("status")
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			app=btechapp.fetch(1)[0]
			app.appstatus=status
			app.put()
			self.redirect("/editstatus?appid="+appid,permanent=True)

class EditMarks(webapp.RequestHandler):
		def get(self):
			if check_access()==False:
				return
			allmarks={"marks":""}
			canid={"appid":""}
			values={"allmarks":allmarks,"canid":canid}
			appid=self.request.get("appid")			
			canid['appid']=appid
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			app=btechapp.fetch(1)[0]
			inputs="""Ent PC<input type="text" value="%s" name="epcmark" id="epcmark">&nbsp;Max<input type="text" value="%s" name="epcmaxmark" id="epcmaxmark"><br>
					  Ent M&nbsp;<input type="text" value="%s" name="emmark" id="emmark">&nbsp;Max<input type="text" value="%s" name="emmaxmark" id="emmaxmark"><br>
					  +2 P&nbsp;&nbsp;&nbsp;<input type="text" value="%s" name="qpmark" id="qpmark">&nbsp;Max<input type="text" value="%s" name="qpmaxmark" id="qpmaxmark"><br>
					+2 C&nbsp;&nbsp;&nbsp;<input type="text" value="%s" name="qcmark" id="qcmark">&nbsp;Max<input type="text" value="%s" name="qcmaxmark" id="qccmaxmark"><br>
					+2 M&nbsp;&nbsp;<input type="text" value="%s" name="qmmark" id="qmmark">&nbsp;Max<input type="text" value="%s" name="qmmaxmark" id="qmmaxmark"><br>""" % (app.epcmark,app.epcmaxmark,app.emmark,app.emmaxmark,app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark)
			allmarks['marks']=inputs
			path = os.path.join(os.path.dirname(__file__), 'editmarks.html')
			self.response.out.write(template.render(path, values))
		def post(self):
			if check_access()==False:
				return
			appid=self.request.get("appid")
			epcmark=self.request.get("epcmark")
			emmark=self.request.get("emmark")
			qpmark=self.request.get("qpmark")
			qcmark=self.request.get("qcmark")
			qmmark=self.request.get("qmmark")
	
			epcmaxmark=self.request.get("epcmaxmark")
			emmaxmark=self.request.get("emmaxmark")
			qpmaxmark=self.request.get("qpmaxmark")
			qcmaxmark=self.request.get("qcmaxmark")
			qmmaxmark=self.request.get("qmmaxmark")
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			app=btechapp.fetch(1)[0]
			app.epcmark=epcmark
			app.emmark=emmark
			app.qpmark=qpmark
			app.qcmark=qcmark
			app.qmmark=qmmark
			
			app.epcmaxmark=epcmaxmark
			app.emmaxmark=emmaxmark
			app.qpmaxmark=qpmaxmark
			app.qcmaxmark=qcmaxmark
			app.qmmaxmark=qmmaxmark
			app.put()
			print 'Content-Type: text/plain'
			print ''
			print 'Saved'
	
application = webapp.WSGIApplication(
                                     [('/editstatus', EditStatus),('/editmarks', EditMarks)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

