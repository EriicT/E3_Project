import variables as v
from wconf import *
	
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
	
	
def set_game(data):
	v.n_player=int(data.split('*')[0])
	v.duration=int(data.split('*')[-1])
	print("Set game, nb player = ", v.n_player) 


def start_game():
	n_feedback =0
	for key in v.dict_connected_devices :
		if v.dict_connected_devices[key]['feedback']==str(True) :
			n_feedback += 1
	if n_feedback==(v.n_player) and n_feedback!=0 :
		init_timer(v.duration)
		watchdog_timer()
		return True

	else : 
		return False

