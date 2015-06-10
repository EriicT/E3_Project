import variables as v

def init_timer(time):
	global v.start_timer, v.end_time
	v.start_time = v.datetime.datetime.now()
	v.end_time = v.start_time + datetime.timedelta(time)
	return True

def timer_playable() :
	global v.end_time, v.now_time, 
	v.now_timer = datetime.datetime.now()
	if v.now_time > v.end_time
		 return False
	return True

def watchdog_timer() :
	global v.is_playable
	v.is_playable = timer_playable()
	v.threading.Timer(1,watcdhog_timer).start()	

