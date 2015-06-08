import variables as v

import com as c
from read_freq import *
from wconf import *
from moteur import *
from laser import *
from read_freq import *

import commands

def associate_devices():
	for key in v.dict_connected_devices:
		if v.dict_connected_devices[key]['role'] == "true_master" and v.dict_connected_devices[key]['is_linked'] == False :
			v.dict_connected_devices[key]['associated_device_ip'] = v.HOST
		    v.dict_connected_devices[v.HOST]['associated_device_ip'] = key
			v.dict_connected_devices[key]['is_linked'] = True
			v.dict_connected_devices[v.HOST]['is_linked'] = True
		
		elif v.dict_connected_devices[key]['role'] == "master" :
			for second_key in v.dict_connected_devices:
				if v.dict_connected_devices[second_key]['role'] == "slave" and v.dict_connected_devices[second_key]['is_linked'] == False : 
					v.dict_connected_devices[key]['associated_device_ip'] = second_key
					v.dict_connected_devices[second_key]['associated_device_ip'] = key
					v.dict_connected_devices[key]['is_linked'] = True
					v.dict_connected_devices[second_key]['is_linked'] = True
					c.send(key,"request_feedback","please")
					c.send(second_key,"request_feedback","please")
					
	
		elif v.dict_connected_devices[key]['role'] == "slave" :
			for second_key in v.dict_connected_devices:
				if v.dict_connected_devices[second_key]['role'] == "master" and v.dict_connected_devices[second_key]['is_linked'] == False :
					v.dict_connected_devices[key]['associated_device_ip'] = second_key
					v.dict_connected_devices[second_key]['associated_device_ip'] = key
					v.dict_connected_devices[key]['is_linked'] = True
					v.dict_connected_devices[second_key]['is_linked'] = True
					c.send(key,"request_feedback","please")
					c.send(second_key,"request_feedback","please")

def get_self_ip():
	return str(commands.getoutput("hostname -I"))
	
def init_timer(duration):
	final_duration=int(60*duration)
	v.start_time = v.datetime.datetime.now()
	v.end_timer = v.start_time + v.datetime.timedelta(seconds=final_duration)

def timer_playable(): 
	v.now_timer = v.datetime.datetime.now()
	if v.end_timer > v.now_timer:
		return True
	else :
		print("Date de debut: "+str(v.now_timer))
		print("Date de Fin :"+str(v.end_timer))
		return False

def watchdog_timer():
	v.is_playable = timer_playable()
	print("Watched "+ str(v.is_playable))
	if v.is_playable == False :
		v.threading.Timer(1,watchdog_timer).cancel()
	else :	
		v.threading.Timer(1,watchdog_timer).start()	
def pause():
	pass

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
	
def set_game(data):
	v.n_player=int(data.split('*')[0])
	v.duration=int(data.split('*')[-1])
	print("Set game, nb player = ", v.n_player) 

def configuration():
	enable_detection("configuration",True)
	v.time.sleep(45)
	set_configuration(v.configuration)
	return True

def set_profil(cible,data):
	global splited_data
	splited_data = str(data).split('*')
	len_data=len(splited_data)
	cursor = 0
	if cible == str('10.5.5.1'):
		cible = get_self_ip()
	while cursor != len_data :
		v.dict_connected_devices[cible][splited_data[cursor]] =splited_data[cursor+1]
		cursor+=2
	print_dict()



def start_game():
	n_feedback =0
	for key in v.dict_connected_devices :
		if v.dict_connected_devices[key]['feedback']==str(True) :
			n_feedback += 1
	if n_feedback==(v.n_player) and n_feedback!=0 :
		init_timer(v.duration)
		watchdog_timer()
		v.current_phase = "in_game"
		return True

	else : 
		return False

def start_game_slave():
	v.current_phase = "in_game"

def process_command_pre_game(emetteur,commande,data):
	if v.dict_connected_devices[emetteur][associated_device_ip]==commands.getoutput("hostname -I") and commande == "setgame" and v.configuration=="HOST":
		set_game(data)
	elif commande =="setprofil":
		set_profil(emetteur,data)
		if v.configuration=="HOST":
			associate_devices()
	elif commande == "stop" :	
		quit_game(emetteur)
	elif commande == "start_game_slave":
		start_game_slave()
	else 
		pass

def process_command_in_game(emetteur,commande,data):
	if  v.dict_connected_devices[get_self_ip()]['associated_device_ip'] == emetteur :
		if commande == "moteur" :
			moteur(data)	
		elif commande == "laser":
			laser(data)
		elif commande == "pause" 
			pause()
		else :
			pass

