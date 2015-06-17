import csv 
#import variables as v
import datetime
import os

def create_database():
	global date,database_file
	date = str(datetime.datetime.now().day)+str(".")+str(datetime.datetime.now().hour)+str(".")+str(datetime.datetime.now().minute)
	database_file =str("db_"+date+str(".csv"))
	#os.system("sudo nano database/"+database_file)
	return database_file

def write_database(cible,event,score):
	pass

def read_databse():
	pass

def change_event(cible,event_type):
	pass 

print (create_database())