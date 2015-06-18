import variables as v

import com as c
from read_freq import *
from wconf import *
from moteur import *
from laser import *
from read_freq import *
from database import *

import commands

def off() :
	pass

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]

def associate_devices():
	for key in v.dict_connected_devices:
		if v.dict_connected_devices[key]['role'] == "true_master" :
			v.dict_connected_devices[key]['associated_device_ip'] = get_self_ip()
			v.dict_connected_devices[get_self_ip()]['associated_device_ip'] = key
			v.dict_connected_devices[key]['is_linked'] = True
			v.dict_connected_devices[get_self_ip()]['is_linked'] = True
			break
			c.print_dict()

		elif v.dict_connected_devices[key]['role'] == "master" :
			for second_key in v.dict_connected_devices:
				if v.dict_connected_devices[second_key]['role'] == "slave_slave" and v.dict_connected_devices[second_key]['is_linked'] == False : 
					v.dict_connected_devices[key]['associated_device_ip'] = second_key
					v.dict_connected_devices[second_key]['associated_device_ip'] = key
					v.dict_connected_devices[key]['is_linked'] = True
					v.dict_connected_devices[second_key]['is_linked'] = True
					c.send(key,"setmate","associated_device_ip*"+str(second_key))
					c.send(second_key,"setmate","associated_device_ip*"+str(key))
			break		
		else :
			print("NON")

	
def init_timer(duration):
	final_duration=int(60*duration)
	v.start_time = v.datetime.datetime.now()
	v.end_timer = v.start_time + v.datetime.timedelta(seconds=final_duration)

def timer_playable(): 	
	v.now_timer = v.datetime.datetime.now()
	if v.end_timer > v.now_timer:
		return True
	else :
		for key in v.dict_connected_devices :
			c.send(key,"stop","game")

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
	enable_detection("all",False)

def set_configuration(config):
	v.HOST = get_self_ip()
	c.init_dict()
	init_laser("HOST")
	create_database()

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
			init_laser(v.configuration)
			v.board.add_event_detect(v.IN_L, v.board.RISING, callback=count_left)
			v.board.add_event_detect(v.IN_R, v.board.RISING, callback=count_right)
			#v.board.add_event_detect(v.IN_B, v.board.RISING, callback=count_back)
		else :
			v.board.remove_event_detect(v.IN_L)
			v.board.remove_event_detect(v.IN_R)
			#v.board.remove_event_detect(v.IN_B)
	elif phase =="all":
			if state == True : 
				v.board.add_event_detect(v.IN_L, v.board.RISING, callback=count_left)
				v.board.add_event_detect(v.IN_R, v.board.RISING, callback=count_right)
				#v.board.add_event_detect(v.IN_B, v.board.RISING, callback=count_back)
				#leds
			else :
				v.board.remove_event_detect(v.IN_L)
				v.board.remove_event_detect(v.IN_R)
				#v.board.remove_event_detect(v.IN_B)
				#leds
	
def recept_event(emetteur,data):
	global player1,player2, name_player1, name_player2
	for key in v.dict_player:
		if emetteur == v.dict_player[key]['ip'] :
			player1=v.dict_player[key]['ip']
			name_player=key
		else :
			player2=v.dict_player[key]['ip']
			name_player2=key
	try :
		new_event(player1,player2,data,v.csvf)
		c.send(emetteur,"lolol","beTouched&"+name_player2)
		c.send(v.dict_player[key]['ip'],"lolol","hitTarget&"+name_player1)
	except :
		pass
def set_game(data):
	v.n_player=int(data.split('*')[0])
	v.duration=int(data.split('*')[-1][0])
	print("Set game, nb player = ", v.n_player, v.duration) 

def configuration():
	enable_detection("configuration",True)
	set_configuration(v.configuration)
	return True

def set_profil(cible,data):
	global splited_data
	print("setprofil :" + cible)
	print("data :" +data)
	splited_data = str(data).split('*')
	len_data=len(splited_data)
	print("len_data :" , len_data)
	cursor = 0
	while cursor != len_data :
		print(cursor)
		v.dict_connected_devices[str(cible)][splited_data[cursor]] =splited_data[cursor+1]
		cursor+=2

	if (len(v.dict_connected_devices[str(cible)]['name'])>1) and v.dict_connected_devices[str(cible)]['type']=="android" :
		if  v.dict_player.get(v.dict_connected_devices[str(cible)]['name'])==None :
			v.dict_player[v.dict_connected_devices[str(cible)]['name']]=dict({
				'has_touch':0,
				'has_been_touched':0,
				'score':0,
				'ip':str(cible),
			})

	c.print_dict()

def set_mate(data):
	set_profil(get_self_ip(),data)
	c.send(get_self_ip(),"setprofil",v.dict_connected_devices[get_self_ip()]['feedback'])

def start_game():
	n_feedback =0
	for key in v.dict_connected_devices :
		if v.dict_connected_devices[key]['feedback'].startswith("True") : 
			n_feedback += 1
			print(n_feedback)
			if n_feedback==(int(v.n_player)*2) and n_feedback !=0 :
				for key in v.dict_connected_devices :
					c.send(v.dict_connected_devices[key]['self_ip'],"start_game","kikou")
#		init_timer(v.duration)
#		watchdog_timer()
				v.current_phase = "in_game"
				enable_detection("in_game",True)
				return True
			else : 
				pass
		else :
			pass
	return False

def start_game_slave():
	v.current_phase = "in_game"
	v.is_playable = True


def process_command_pre_game(emetteur,commande,data):
	print(emetteur, commande,data)
	if v.dict_connected_devices[emetteur]['associated_device_ip']==get_self_ip() and commande == "setgame" and v.configuration=="HOST":
		print("setgame")
		set_game(data)
	elif commande =="setprofile":
		set_profil(emetteur,data)
		if v.configuration=="HOST":
			associate_devices()
			c.print_dict()
	elif commande=="request_feedback":
		c.send(get_self_ip(),"setprofil",v.dict_connected_devices[get_self_ip()]['feedback'])
	elif commande =="setmate" :
		set_mate(data)
		print("set_mate")
	elif commande == "start_game_slave":
		start_game_slave()
	elif commande == "stop" :
		print("ARNAUD APPUIE SUR LE BOUTON")
	else :
		pass

def process_command_in_game(emetteur,commande,data):
	print(emetteur , commande , data)
	if  v.dict_connected_devices[get_self_ip()]['associated_device_ip'] == emetteur :	
		if commande == "moteur" :
			moteur(data)	
		elif commande == "laser":
			laser(data)
		elif commande == "stop" :
			print("G GAGNER")
			v.is_playable=False
		elif commande == "notify_event" :
			recept_event(emetteur,data)
		else :
			pass

