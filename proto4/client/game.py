import variables as v

import com as c
#import database as d
from read_freq import *
from wconf import *
from moteur import *
from laser import *
from read_freq import *

import commands

def off() :
	pass

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]


def pause():
	enable_detection("all",False)

def set_configuration(config):
	v.HOST = get_self_ip()


def enable_detection(phase,state):
	if phase == "configuration" :
		if state == True :
			v.board.add_event_detect(v.IN_START, v.board.RISING,callback=off,bouncetime=300)
			v.board.add_event_detect(v.IN_SELECT,v.board.RISING,callback=switch,bouncetime=1)
		else :
			v.board.remove_event_detect(v.IN_SELECT)
			v.board.remove_event_detect(v.IN_START)
	
	elif phase == "pre_game" :
		if state == True :
			pass	
		
		else : 
			pass

	elif phase == "in_game" :
		if state == True :
			v.board.add_event_detect(v.IN_L, v.board.RISING, callback=count_left)
			v.board.add_event_detect(v.IN_R, v.board.RISING, callback=count_right)
			v.board.add_event_detect(v.IN_B, v.board.RISING, callback=count_back)
		else :
			v.board.remove_event_detect(v.IN_L)
			v.board.remove_event_detect(v.IN_R)
			v.board.remove_event_detect(v.IN_B)
	elif phase =="all":
			if state == True : 
				v.board.add_event_detect(v.IN_L, v.board.RISING, callback=count_left)
				v.board.add_event_detect(v.IN_R, v.board.RISING, callback=count_right)
				v.board.add_event_detect(v.IN_B, v.board.RISING, callback=count_back)
				#leds
			else :
				v.board.remove_event_detect(v.IN_L)
				v.board.remove_event_detect(v.IN_R)
				v.board.remove_event_detect(v.IN_B)
				#leds
	else :
		pass
	
def configuration():
	enable_detection("configuration",True)
	set_configuration(v.configuration)
	return True

def set_profil(cible,data):
	global splited_data
	splited_data = str(data).split('*')
	len_data=len(splited_data)
	cursor = 0
	while cursor != len_data :
		v.dict_connected_devices[cible][splited_data[cursor]] =splited_data[cursor+1]
		cursor+=2
	c.print_dict()

def set_mate(data):
	set_profil(get_self_ip(),data)
	c.send(get_self_ip(),"setprofil",v.dict_connected_devices[get_self_ip()]['feedback'])

def start_game_slave():
	v.current_phase = "in_game"
	enable_detection("configuration",False)
	enable_detection("in_game",True)
	v.is_playable = True 

	
def process_command_pre_game(emetteur,commande,data):
	print emetteur
	print commande
	print data
	if commande =="setprofil":
		set_profil(emetteur,data)
	elif commande == "stop":	
		quit_game(emetteur)
	elif commande=="request_feedback":
		c.send(get_self_ip(),"setprofil",v.dict_connected_devices[get_self_ip()]['feedback'])
	elif commande =="setmate" :
		set_mate(data)
		print("set_mate")
	elif commande == "start":
		start_game_slave()
	else :
		pass

def process_command_in_game(emetteur,commande,data):
	if  v.dict_connected_devices[get_self_ip()]['associated_device_ip'] == emetteur :
		if commande == "moteur" :
			moteur(data)	
		elif commande == "laser":
			laser(data)
		elif commande == "pause" :
			pause()
	elif emetteur =="10.5.5.1" and commande == "pause":
		v.is_playable=False
	else :
		pass
	
