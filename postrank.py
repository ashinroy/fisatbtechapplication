import httplib, urllib
import csv

apprange=3000

def send_to_server(rankdtl,cmd):
	if cmd=='E':
		print rankdtl
		params = urllib.urlencode({'cmd':cmd,'rank':rankdtl[0],'score': rankdtl[1],'pcm':rankdtl[2],'entmark':rankdtl[3],'sno':rankdtl[4],'erollno':rankdtl[5][5:],'name':rankdtl[6],'qualboard':rankdtl[7]})
		
	elif cmd=='D':
		params = urllib.urlencode({'cmd':cmd,'erollno':rankdtl})
	elif cmd=="DA":
		params = urllib.urlencode({'cmd':cmd,'erollno':rankdtl})
	else:
		return False	
	
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("localhost:8080")
	conn.request("POST", "/rankcmd", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	print data

while 1:
	cmd=raw_input("Enter command->")
	if cmd=="exit":
		break
	if cmd=="update":
		with open('ranklist.csv', 'rb') as f:
			reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
			for row in reader:
				send_to_server(row,'E')
	if cmd=="delete":
		erollno=raw_input("Enter erollno->")
		send_to_server(erollno,'D')
	if cmd=="deleteall":
			send_to_server("0000000000",'DA')



