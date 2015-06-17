import variables as v


def init_laser(player):
	global laser
	laser = v.board.PWM(v.OUT_LASER,v.set_laser[player]['frequency'])
	

def laser(state):
		if state == "ON" :
			laser.start(50)
		else :
			laser.start(0)


