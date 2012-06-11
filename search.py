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

table_html="""<tr><td><b>%s</b></td><td><b>%s</b></td><td>P:<b>%s/%s</b><br>C:<b>%s/%s</b><br>M:<b>%s/%s</b></td><td>PC:<b>%s/%s</b><br>M:<b>%s/%s</b></td><td>Phone:%s</td>
<td><button type=button onclick='changestatus("/editstatus?appid=%s");'>status</button></td><td><button type="button" onclick='changemarks("/editmarks?appid=%s");'>Editmark</button></td><td><button type="button" onclick='addserial("/map?appid=%s");'>SNo:%s</button></td></tr>"""


def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips



class Search(webapp.RequestHandler):
	def getSNo(self,erollno):
		try:
			smap=serialNoMap.all()
			smap.filter("erollno =",erollno)
			serialno=smap.fetch(1)[0]
			return serialno.sno
		except:
			return dsno
	def addSNo(self,erollno,sno):
			smap=serialNoMap()
			smap.erollno=erollno
			smap.sno=so
			smap.put()	
	
	
	def get(self):
		if check_access()==False:
			return
		results={"result":""}
		values={"results":results}
		path = os.path.join(os.path.dirname(__file__), 'search.html')
		self.response.out.write(template.render(path, values))
	def post(self):
		search_html=""
		
		if check_access()==False:
			return
		erollno=self.request.get("query").strip()
		btechapp=btechApp.all()
		btechapp.filter("erollno =",erollno)
		apps=btechapp.fetch(max_apps)
		sno=self.getSNo(erollno)
		if sno==str(dsno):
			sno="NA"
		for app in apps:
			search_html=search_html+table_html %(app.appid,app.name,				app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,app.epcmark,app.epcmaxmark,app.emmark,app.emmaxmark,app.resphone,app.appid,app.appid,app.appid,sno)
		results={"result":search_html}
		values={"results":results}
		path = os.path.join(os.path.dirname(__file__), 'search.html')
		self.response.out.write(template.render(path, values))
		
application = webapp.WSGIApplication(
                                     [('/search', Search)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

