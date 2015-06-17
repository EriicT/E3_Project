
import csv 
import variables as v
import datetime
import os



def format(acteur1,acteur2,list_score):
	del v.write_message[:]
	del v.write_final[:]
	v.string_message = str(acteur1)+str("-")+str(list_score[0])+str("-")+str(list_score[-1])+str("-")+str(acteur2)
	v.write_message.append(v.string_message)
	return (v.write_message)

def create_database():
	global date,database_file,p
	date = str(datetime.datetime.now().day)+str(".")+str(datetime.datetime.now().hour)+str(".")+str(datetime.datetime.now().minute)
	database_file =str("db_"+date+str(".csv"))
	os.system("sudo cp database/example database/"+database_file)
	v.csvf=database_file
	return v.csvf

def write_database(data,file):
	with open(v.csvf, 'a') as p :
		csv_ecriture = csv.writer(p,delimiter=';',lineterminator='\n')
		csv_ecriture.writerows(data)
	p.close()	
def read_databse():
	pass

def new_event(acteur1,acteur2, event_type,file):
	if event_type== "touched" :
		v.write_column.append("0")
		v.write_column.append("1")
		v.write_final.append(format(acteur1,acteur2,v.write_column))	
		write_database(v.write_final,file)
		print v.write_final
	elif event_tupe =="touch" :
		pass
	else : 
		pass		 

print (create_database())
file = create_database()
for i in range (0,5) :
	new_event("Eric","Kikoo","touched",file)

print v.csvf
