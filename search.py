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

table_html="""<tr><td><b>%s</b></td><td><b>%s</b></td><td>P:%s/%s<br>C:%s/%s<br>M:%s/%s</td><td>PC:%s<br>M:%s</td><td>Phone:%s</td>
<td><button type=button onclick='changestatus("/editstatus?appid=%s");'>status</button></td></tr>"""


def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips


class Search(webapp.RequestHandler):
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
			appid=self.request.get("query").strip()
			btechapp=btechApp.all()
			btechapp.filter("appid =",appid)
			apps=btechapp.fetch(max_apps)
			for app in apps:
				search_html=search_html+table_html %(app.appid,app.name,
				app.qpmark,app.qpmaxmark,app.qcmark,app.qcmaxmark,app.qmmark,app.qmmaxmark,app.epcmark,app.emmark,app.resphone,app.appid)
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

