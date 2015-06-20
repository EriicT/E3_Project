import variables as v

def init_laser(player):
	v.laser = v.board.PWM(v.OUT_LASER,v.set_laser[player]['frequency'])
	
def laser(state):
	try :
		if state.startswith("ON") :
			v.laser.start(50)
		elif state.startswith("OFF"):
			v.laser.start(0)
		else :
			pass
	except :
		pass


