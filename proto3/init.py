import RPi.GPIO as board
import sys

#Moteur Gauche
MG_DW = 3
MG_FW = 5
MG_EN = 7

#Moteur Droit 
MD_DW = 11
MD_FW = 13
MD_EN = 15

#Laser
OUT_LASER = 19

#Leds
OUT_RDY = 31
OUT_GUEST = 33
OUT_HOST = 35
OUT_ON = 37

#Panneau photovoltaique
IN_L = 8
IN_R = 10
IN_B = 12

#Boutons d'entree
IN_SELECT = 36
IN_START = 38


def off(callback) :
	board.cleanup()
	sys.exit("Bye")	

def init():
	board.cleanup()	
	board.setmode(board.BOARD)
	board.setup(MG_DW,board.OUT)
	board.setup(MG_FW,board.OUT)
	board.setup(MG_EN,board.OUT)
	board.setup(MD_DW,board.OUT)
	board.setup(MD_FW,board.OUT)
	board.setup(MD_EN,board.OUT)
	board.setup(OUT_LASER,board.OUT)
	board.setup(OUT_RDY,board.OUT)
	board.setup(OUT_GUEST,board.OUT)
	board.setup(OUT_HOST,board.OUT)
	board.setup(OUT_ON,board.OUT)

	board.setup(IN_SELECT,board.IN,pull_up_down=board.PUD_DOWN)
	board.setup(IN_START,board.IN,pull_up_down=board.PUD_DOWN)
	board.setup(IN_B,board.IN,pull_up_down=board.PUD_UP)
	board.setup(IN_R,board.IN,pull_up_down=board.PUD_UP)
	board.setup(IN_L,board.IN,pull_up_down=board.PUD_UP)
	
def start():
	board.output(MG_DW,board.LOW)
	board.output(MG_FW,board.LOW)
	board.output(MG_EN,board.LOW)
	board.output(MD_DW,board.LOW)
	board.output(MD_FW,board.LOW)
	board.output(MD_EN,board.LOW)
	board.output(OUT_LASER,board.LOW)
	board.output(OUT_RDY,board.LOW)
	board.output(OUT_GUEST,board.LOW)
	board.output(OUT_HOST,board.LOW)
	board.output(OUT_ON,board.HIGH)

	board.add_event_detect(IN_START,board.RISING,callback=off,bouncetime=300)


