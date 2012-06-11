import csv
import operator


def calculateTotalMark(emmark,epcmark,qpmark,qpmaxmark,qcmark,qcmaxmark,qmmark,qmmaxmark):
	#print emmark,epcmark,qpmark,qpmaxmark,qcmark,qcmaxmark,qmmark,qmmaxmark
	emmark=float(emmark)
	epcmark=float(epcmark)
	qpmark=float(qpmark)
	qpmaxmark=float(qpmaxmark)
	qcmark=float(qcmark)
	qcmaxmark=float(qcmaxmark)
	qmmark=float(qmmark)
	qmmaxmark=float(qmmaxmark)
	pcmplus2=qpmark+qcmark+qmmark
	pcmplus2max=qpmaxmark+qcmaxmark+qmmaxmark
	pcment=emmark+epcmark
	pcmentmax=960.0
	plus2perc=((pcmplus2/pcmplus2max)*100)
	pcmentperc=((pcment/pcmentmax)*100)
	return [round(plus2perc+pcmentperc,4),plus2perc,pcmentperc]

#add code to reject any negative marks
def check_rejection(marks,sno):
	return [False,"No reason"]



writer=csv.writer(open("ranklist.csv", 'w'),delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
rjwriter=csv.writer(open("rjctdapps.csv", 'w'),delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
totallist=[]
rjctdlist=[]




with open('applicationforranklist.csv', 'rb') as f:
	reader = csv.reader(f, delimiter='%', quoting=csv.QUOTE_NONE)
	for row in reader:
		if row[0][0]=='N':
			continue
		
		marks=calculateTotalMark(row[5],row[6],row[11],row[12],row[13],row[14],row[15],row[16])
		if check_rejection(marks,row[1])[0]==True:
			rjctdlist.append([marks[0],marks[1],marks[2],row[1],row[2],row[3],row[10]])
			continue
		totallist.append([marks[0],marks[1],marks[2],row[1],row[2],row[3],row[10]])
totallist.sort(reverse=True,key=operator.itemgetter(0))
i=1
for row in totallist:
	row=[i,row[0],row[1],row[2],row[3],row[4],row[5],row[6]]
	writer.writerow(row)
	print row	
	i=i+1
for row in rjctdlist:
	rjwriter.writerow(row)
	i=i+1


	
