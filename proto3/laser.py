import variables as v

laser= v.board.PWM(v.OUT_LASER,400)

def init_laser(player):
	global laser
	laser = v.board.PWM(v.OUT_LASER,v.set[player])
	

def state(state):
		if state == "high" :
			laser.start(50)
		else :
			laser.start(0)


