address_length=10
phoneno_length=9
nation_length=1
fboaes_length=2
erollno_length=3
qualexamno_length=2
qualexam_length=2
qualboard_length=2
ddno_length=3
ddbranch_length=3
dddate_length=9
ddbank_length=2
chop_length=25
mailbody="""Dear %s 
You application for B.Tech under management quota at Federal Insitute of Science and Technology (FISAT) has been submitted. 
Your Application ID is %s. This ID will be used to track you application at every stage. 
The application form can be downloaded from http://fisatbtechapplication.appspot.com/print?appid=%s
You can reprint the application from http://fisatbtechapplication.appspot.com/reprint

List of documents to be enclosed with printout
1. Attested copy of 10th Standard mark list/ Certificate
2. Attested copy of Standard Mark list
3. Attested copyof Entrance Admit Card
4. Attested copy of Entrance Mark List

The printed application need to be sent to the following address.

The Principal
Federal Institute of Science And Technology (FISAT)
Hormis Nagar, Mookkannoor P O,
Angamaly, Ernakulam Dt.
Kerala, India, Pin - 683 577
Visit http://admission.fisat.ac.in for any information regarding admissions.
This is a system generated mail. Do not reply to this mail.
All the best."""
class defaults():
	def __init__(self):
		self.values={
			"name":"",
			"paddress":"",
			"resphone":"",
			"mobphone":"",
			"panchayath":"0",
			"inpanchayath":"",
			"samepaddress":"",
			"caddress":"",
			"email":"",
			"dobdate":"01",
			"dobmonth":"01",
			"dobyear":"1994",
			"gender":"M",
			"nation":"",
			"religion":"Hindu",
			"caste":"",
			"category":"General",
			"fathername":"",
			"fatheremployed":"",
			"fatherocc":"",
			"fatherdesig":"",
			"fatheraddress":"",
			"fatherphone":"",
			"mothername":"",
			"motheremployed":"",
			"motherocc":"",
			"motherdesig":"",
			"motheraddress":"",
			"motherphone":"",
			"enablemfboaes":"",
			"mfboaesmemno":"",
			"enablepfboaes":"",
			"pfboaesmemno":"",
			"income":"",
			"erollno":"",
			"erank":"",
			"epcmark":"",
			"epcmaxmark":"",
			"emmark":"",
			"emmaxmark":"",
			"insaddress":"",
			"insphone":"",
			"qualboard":"",
			"qualexamyear":"",
			"qualexamno":"",
			"qualexam":"",
			"inqualexam":"",
			"qpmark":"",
			"qpmaxmark":"",
			"qcmark":"","":"",
			"qcmaxmark":"",
			"qmmark":"",
			"qmmaxmark":"",
			"bp1":"0",
			"bp2":"0",
			"bp3":"0",
			"bp4":"0",
			"bp5":"0",
			"bp6":"0",
			"ddno":"",
			"dddate":"",
			"ddbank":"",
			"ddbranch":""}
		self.errors={
			"name":"",
			"paddress":"",
			"resphone":"",
			"mobphone":"",
			"panchayath":"",
			"inpanchayath":"",
			"samepaddress":"",
			"caddress":"",
			"email":"",
			"dobdate":"",
			"dobmonth":"",
			"dobyear":"",
			"gender":"",
			"nation":"",
			"religion":"",
			"caste":"",
			"category":"",
			"fathername":"",
			"fatheremployed":"",
			"fatherocc":"",
			"fatherdesig":"",
			"fatheraddress":"",
			"fatherphone":"",
			"mothername":"",
			"motheremployed":"",
			"motherocc":"",
			"motherdesig":"",
			"motheraddress":"",
			"motherphone":"",
			"enablemfboaes":"",
			"mfboaesmemno":"",
			"enablepfboaes":"",
			"pfboaesmemno":"",
			"income":"",
			"erollno":"",
			"erank":"",
			"epcmark":"",
			"epcmaxmark":"",
			"emmark":"",
			"emmaxmark":"",
			"insaddress":"",
			"insphone":"",
			"qualboard":"",
			"qualexamyear":"",
			"qualexamno":"",
			"qualexam":"",
			"inqualexam":"",
			"qpmark":"",
			"qpmaxmark":"",
			"qcmark":"","":"",
			"qcmaxmark":"",
			"qmmark":"",
			"qmmaxmark":"",
			"bp1":"",
			"bp2":"",
			"bp3":"",
			"bp4":"",
			"bp5":"",
			"bp6":"",
			"extra":"",
			"addinfo":"",
			"ddno":"",
			"dddate":"",
			"ddbank":"",
			"ddbranch":"",
			"captcha":""}
