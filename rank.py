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

ranktabletitle="""<tr bgcolor="white"><td>Name</td><td>PCM %(A)</td><td>Entrance %(B)</td><td>Index Mark(A+B)</td><td>FISAT Rank</td><tr>"""

def check_access():
	ip=environ['REMOTE_ADDR']
	return ip in adminips




class ShowRank(webapp.RequestHandler):
	def get(self):
		if publish_rank==0  and check_access()==False:
			return 
		rank={"error":"","ranktable":""}
		values={"rank":rank}
		path = os.path.join(os.path.dirname(__file__), 'rank.html')
		self.response.out.write(template.render(path, values))
	def post(self):
		if publish_rank==0 and check_access()==False:
			return
		rank={"error":"","ranktable":""}
		values={"rank":rank}
		appid=self.request.get("appid").strip()
		if appid.find('F')>-1:
			erollno=appid[5:]
		else:
			erollno=appid
		try:
			rankdtls=rankList.all()
			rankdtls.filter("erollno =",erollno)
			rankdtl=rankdtls.fetch(1)[0]
			rank['ranktable']=ranktabletitle+"<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (rankdtl.name,rankdtl.pcm,rankdtl.entmark,rankdtl.score,rankdtl.rank)
		except:
			rank['ranktable']="""<tr><td colspan="5" >Rank details not avialable. Please contact college for more information</td></tr>"""	

		path = os.path.join(os.path.dirname(__file__), 'rank.html')
		self.response.out.write(template.render(path, values))

	
			
#I know this is vulnerable, I have to add a better authentication and ssl. 	
class RankCmd(webapp.RequestHandler):
		def write_status(self,msg):
			print 'Content-Type: text/plain'
			print ''
			print msg		
		def post(self):
			if check_access()==False:
				return 
			if lock_rank==1:
				return 
			cmd=self.request.get("cmd")
			rank=self.request.get("rank")
			erollno=self.request.get("erollno")
			sno=self.request.get("sno")
			rank=self.request.get("rank")	
			pcm=self.request.get("pcm")
			entmark=self.request.get("entmark")	
			score=self.request.get("score")
			qualboard=self.request.get("qualboard")
			name=self.request.get("name")
			if cmd=='E':
				try:
					rankdtls=rankList.all()
					rankdtls.filter("erollno =",erollno)
					rankdtl=rankdtls.fetch(1)[0]
					rankdtl.sno=sno
					rankdtl.rank=rank
					rankdtl.pcm=pcm
					rankdtl.entmark=entmark
					rankdtl.score=score
					rankdtl.qualboard=qualboard
					rankdtl.name=name
					rankdtl.put()
					self.write_status("EDIT ENTRY")
				except:
					rankdtl=rankList()
					rankdtl.sno=sno
					rankdtl.rank=rank
					rankdtl.pcm=pcm
					rankdtl.entmark=entmark
					rankdtl.score=score
					rankdtl.erollno=erollno
					rankdtl.qualboard=qualboard
					rankdtl.name=name
					rankdtl.put()
					self.write_status("NEW ENTRY")
			elif cmd=='D':
					try:
						rankdtls=rankList.all()
						rankdtls.filter("erollno =",erollno)
						rankdtl=rankdtls.fetch(1)[0]
						rankdtl.delete()	
						self.write_status("DEL ENTRY")
					except:
						self.write_status("UNABLE DEL")
			elif cmd=="DA":
					rankdtls=rankList.all()
					rankdtl=rankdtls.fetch(max_apps)
					db.delete(rankdtl)
					self.write_status("DEL ALL")









			


			
				






application = webapp.WSGIApplication(
                                     [('/rank',ShowRank),('/rankcmd',RankCmd)
									 ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
