from variables import *





def init_timer(time):
	global start_time,end_time
	start_time = datetime.datetime.now()
	end_time = start_time + datetime.timedelta(time)
	return True

def timer_playable() :
	global end_time, now_timer, 
	now_timer = datetime.datetime.now()
	if now_timer.hours == end_timer.hours and now_timer.minutes == end_timer.minutes and now_timer.seconds == end_timer.seconds :
		 return False
	return True

def watchdog_timer() :
	global is_playable
	is_playable = timer_playable()
		

