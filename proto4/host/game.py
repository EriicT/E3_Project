import variables as v
import com as c
from read_freq import *
from wconf import *
from moteur import *
from laser import *
from read_freq import *
from database import *

import commands

global ID
ID = v.dict_connected_devices

global players
players=v.dict_player

def stop() :
	for key in ID :
		c.send(key,"stop","kikoo")
	send_score()

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]

def associate_devices():
	for key in v.dict_connected_devices:
		if ID[key]['role'] == "true_master" :
			ID[key]['associated_device_ip'] = get_self_ip()
			ID[get_self_ip()]['associated_device_ip'] = key
			ID[key]['is_linked'] = True
			ID[get_self_ip()]['is_linked'] = True
			break
			c.print_dict()

		elif ID[key]['role'] == "master" :
			for second_key in v.dict_connected_devices:
				if ID[second_key]['role'] == "slave_slave" and ID[second_key]['is_linked'] == False : 
					ID[key]['associated_device_ip'] = second_key
					ID[second_key]['associated_device_ip'] = key
					ID[key]['is_linked'] = True
					ID[second_key]['is_linked'] = True
					v.time.sleep(1)
					c.send(key,"setmate","associated_device_ip&"+str(second_key))
					c.send(second_key,"setmate","associated_device_ip*"+str(key))
					break		
		else :
			print("NON")

	
def init_timer(duration):
	final_duration=int(60*duration)
	v.start_time = v.datetime.datetime.now()
	v.end_timer = v.start_time + v.datetime.timedelta(seconds=final_duration)

def send_score():
	global long_score_1, long_score_2, long_nothing
	(player1,player2) = players.keys()
	print("score sent ")
	long_nothing = str("-;-;-;-;-_-;-;-;-;-_-;-;-;-;-_-;-;-;-;_-;-;-;-_-;-;-;-;")
	long_score_1 = str(player1)+str(";")+str(players[player1]['has_touch'])+str(";")+str(players[player1]['has_been_touched'])+str(";")+str(players[player1]['score'])
	long_score_2 = str(player2)+str(";")+str(players[player2]['has_touch'])+str(";")+str(players[player2]['has_been_touched'])+str(";")+str(players[player2]['score'])
	c.send(players[player1]['ip'],"android",str("score&")+long_score_1+str("_")+long_score_2+str("_")+long_nothing)
	c.send(players[player2]['ip'],"android",str("score&")+long_score_2+str("_")+long_score_1+str("_")+long_nothing)
	v.threading.Timer(5,send_score).start()	

	if v.is_playable == False :
		v.threading.Timer(5,send_score).cancel()

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

def score_timer():
	if v.is_playable == False :
		v.threading.Timer(5,send_score).cancel()
	else :	
		send_score()
def pause():
	enable_detection("all",False)


def send_unique_score(address):
	global lg1, lg2, lgn, player
	player = ID[address]['name']
	lgn = str("-;-;-;-;_-;-;-;-;_-;-;-;-;_-;-;-;-;_-;-;-;-;_-;-;-;-;")
	lg1 = str(player)+str(";")+str(players[player]['has_touch'])+str(";")+str(players[player]['has_touched'])+str(";")+str(players[player]['score'])
        for key in players :
		if player != players[key] :
			lg2 = key+str(";")+str(players[key]['has_touch'])+str(";")+str(players[key]['has_been_touched'])+str(";")+str(players[key]['score'])
   			break
		else :
			pass	
	c.send(address,"android",str("score&")+lg1+str("_")+lg2+str("_")+lgn)

def set_configuration(config):
	v.HOST = get_self_ip()
	c.init_dict()
	init_laser("HOST")

def enable_detection(phase,state):
	if phase == "configuration" :
		if state == True :
		#	v.board.add_event_detect(v.IN_START, v.board.RISING,callback=off,bouncetime=300)
		#	v.board.add_event_detect(v.IN_SELECT,v.board.RISING,callback=switch,bouncetime=1)
			pass
		else :
			v.board.remove_event_detect(v.IN_SELECT)
			v.board.remove_event_detect(v.IN_START)
	
	elif phase == "pre_game" :
		pass
	
	elif phase == "in_game" :
		if state == True :
			init_laser(v.configuration)
			print("initdzdad")
			try :
				v.board.add_event_detect(v.IN_L, v.board.RISING, callback=count_left)
				v.board.add_event_detect(v.IN_R, v.board.RISING, callback=count_right)
				print("init ok panneau")
			except :
				print("init laser pas ok")
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
	print("IN recept even")
	for key in v.dict_player:
		try :
			if ID[emetteur]['associated_device_ip'] == v.dict_player[key]['ip'] :
				v.player1=v.dict_player[key]['ip']
				v.name_player1=key
				print v.player1, v.name_player1
			else :
				v.player2=v.dict_player[key]['ip']
				v.name_player2=key
				print v.player2, v.name_player2
		except :
			print("probleme dans la selection")
	new_event(v.name_player1,v.name_player2,data,v.csvf)
	try :
#		v.time.sleep(0.001)
		c.send(ID[emetteur]['associated_device_ip'],"lolol","beTouched&"+v.name_player2)
#		v.time.sleep(0.001)
		c.send(v.dict_player[v.name_player2]['ip'],"lolol","hitTarget&"+v.name_player1)
#		send_score(players.keys())
	except :
		print("Ca n'a pas marche")

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
		ID[str(cible)][splited_data[cursor]] =splited_data[cursor+1]
		cursor+=2

	if (len(ID[str(cible)]['name'])>1) and ID[str(cible)]['type']=="android" :
		if  v.dict_player.get(ID[str(cible)]['name'])==None :
			v.dict_player[ID[str(cible)]['name']]=dict({
				'has_touch':0,
				'has_been_touched':0,
				'score':0,
				'ip':str(cible),
			})

	c.print_dict()

def set_mate(data):
	set_profil(get_self_ip(),data)
	c.send(get_self_ip(),"setprofil",ID[get_self_ip()]['feedback'])

def start_game():
	n_feedback =0
	for key in v.dict_connected_devices :
		if ID[key]['feedback'].startswith("True") : 
			n_feedback += 1
			if n_feedback==(int(v.n_player)*2) and n_feedback !=0 :
				v.time.sleep(3)
				create_database()
				for key in v.dict_connected_devices :
					c.send(ID[key]['self_ip'],"start","startTimer&"+str(v.duration))
					print("INGAME")
					print(players)

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
	if commande != "moteur":
		print(emetteur, commande,data)

	if ID[emetteur]['associated_device_ip']==get_self_ip() and commande == "setgame" and v.configuration=="HOST":
		print("setgame")
		set_game(data)
	elif commande =="setprofile":
		set_profil(emetteur,data)
		if v.configuration=="HOST":
			associate_devices()
			c.print_dict()
	elif commande=="request_feedback":
		c.send(get_self_ip(),"setprofil",ID[get_self_ip()]['feedback'])
	elif commande =="setmate" :
		set_mate(data)
		print("set_mate")
	elif commande == "stop" :
		stop()
	else :
		pass

def process_command_in_game(emetteur,commande,data):
#	print(emetteur,commande,data)
	if  ID[get_self_ip()]['associated_device_ip'] == emetteur :	
		if commande == "moteur" :
			moteur(data)	
		elif commande == "laser":
			laser(data)
		elif commande == "stop" :
			print("G GAGNER")
			v.is_playable=False
		else :
			pass

	elif commande == "notify_event" :
		recept_event(emetteur,data)

	else :	
		pass
