
import csv 
import variables as v
import datetime
import os

v.dict_player["Eric"]=dict({
				'has_touch':0,
				'has_been_touched':0,
				'score':0,
			})
v.dict_player["Arnaud"]=dict({
				'has_touch':0,
				'has_been_touched':0,
				'score':0,
			})

def format(player):
	global db
	db =v.dict_player[player]
	del v.write_message[:]
	del v.write_final[:]

	v.string_message = str(player)+str(" | ")+str(db['has_touch'])+str(" | ")+str(db['has_been_touched'])+str(" | ")+str(db['score'])
	v.write_message.append(v.string_message)
	return (v.write_message)

def create_database():
	global date,database_file,p
	date = str(datetime.datetime.now().day)+str(".")+str(datetime.datetime.now().hour)+str(".")+str(datetime.datetime.now().minute)
	database_file =str("db_"+date+str(".csv"))
	os.system("sudo cp database/example database/"+database_file)
	v.csvf="database/"+database_file
	return v.csvf

def write_database(data,file):
	with open(v.csvf, 'a') as p :
		csv_ecriture = csv.writer(p,delimiter=';',lineterminator='\n')
		csv_ecriture.writerows(data)
	p.close()	

def read_databse():
	pass

def score(player1,player2):
	v.dict_player[player1]['has_been_touched']+=1
	v.dict_player[player1]['score']+=-1
	v.dict_player[player2]['has_touch']+=1
	v.dict_player[player2]['score']+=2


def new_event(player1,player2, event_type,file):
	if event_type== "touched" :
		score(player1,player2)
		v.write_final.append(format(player1))
		write_database(v.write_final,file)
		v.write_final.append(format(player2))
		write_database(v.write_final,file)
		print v.write_final
	else : 
		pass		 


file = create_database()
print file
for i in range (0,5):
	new_event("Eric","Arnaud","touched",file)
for i in range (0,3):
	new_event("Arnaud","Eric","touched",file)
os.system("sudo nano "+file)
	 
