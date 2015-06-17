import variables as v

laser= v.board.PWM(v.OUT_LASER,400)

def init_laser(player):
	global laser
	laser = v.board.PWM(v.OUT_LASER,v.set_laser[player]['frequency'])
	
def laser(state):
	print("fonction laser")
	if state == "ON" :
		print("laser ok")
		laser.start(50)
	else :
		print("laser non")
		laser.start(0)


