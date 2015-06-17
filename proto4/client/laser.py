import variables as v

laser= v.board.PWM(v.OUT_LASER,400)

def init_laser(player):
	v.laser = v.board.PWM(v.OUT_LASER,v.set_laser[player]['frequency'])
	v.laser.start(50)
	
def laser(state):
		if state == "ON" :
			laser.start(50)
		elif state == "OFF" :
			laser.start(0)
		else : 
			pass

