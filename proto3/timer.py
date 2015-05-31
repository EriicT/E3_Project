import variables as v

def init_timer(time):
	global v.start_timer, v.end_timer
	start_time = datetime.datetime.now()
	end_time = start_time + datetime.timedelta(time)
	return True

def timer_playable() :
	global v.end_timer, v.now_timer, 
	v.now_timer = datetime.datetime.now()
	if v.now_timer.hours == v.end_timer.hours and v.now_timer.minutes == v.end_timer.minutes and v.now_timer.seconds == v.end_timer.seconds :
		 return False
	return True

def watchdog_timer() :
	global v.is_playable
	v.is_playable = timer_playable()
		

