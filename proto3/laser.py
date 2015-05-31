from variables import *

laser=board.PWM(OUT_LASER,400)

def init_laser(player):
	global laser
	laser = board.PWM(OUT_LASER,set[player])
	

def state(state):
		if state == "high" :
			laser.start(50)
		else :
			laser.start(0)


