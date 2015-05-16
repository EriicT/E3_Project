import RPi.GPIO as board
import sys
import socket
import datetime

#Moteur Gauche
MG_BW = 3
MG_FW = 5
MG_EN = 7

#Moteur Droit 
MD_BW = 11
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

#Configuration host
HOST=''
PORT=45500
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

#Laser Frequencies
set=dict()
set["GUEST"]=450*1.06
set["HOST"]=550*1.08

#Reception
l_first=True
l_last=0
l_delta=0
l_duree_echant=0
l_now=0
l_echant=0
l_moyenne_echant=0
l_frequence=0

r_first=True
r_last=0
r_delta=0
r_duree_echant=0
r_now=0
r_echant=0
r_moyenne_echant=0
r_frequence=0

b_first=True
b_last=0
b_delta=0
b_duree_echant=0
b_now=0
b_echant=0
b_moyenne_echant=0
b_frequence=0

#Configuration wifi
status="HOST"
wait_status=5
nb_p=0
nb_rpi=0
p_connected=0
rpi_connected=0

board.cleanup()	
board.setmode(board.BOARD)
board.setup(MG_BW,board.OUT)
board.setup(MG_FW,board.OUT)
board.setup(MG_EN,board.OUT)
board.setup(MD_BW,board.OUT)
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
	
board.output(MG_BW,board.LOW)
board.output(MG_FW,board.LOW)
board.output(MG_EN,board.LOW)
board.output(MD_BW,board.LOW)
board.output(MD_FW,board.LOW)
board.output(MD_EN,board.LOW)
board.output(OUT_LASER,board.LOW)
board.output(OUT_RDY,board.LOW)
board.output(OUT_GUEST,board.LOW)
board.output(OUT_HOST,board.LOW)
board.output(OUT_ON,board.HIGH)

PWM_MG_BW=board.PWM(MG_BW,500)
PWM_MG_FW=board.PWM(MG_FW,500)
PWM_MD_BW=board.PWM(MD_BW,500)
PWM_MD_FW=board.PWM(MD_FW,500)


def off(callback) :
	board.cleanup()
	sys.exit("Bye")	
	server.close()

board.add_event_detect(IN_START,board.RISING,callback=off,bouncetime=300)


