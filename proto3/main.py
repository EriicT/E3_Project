import time
from wconf import *
from variables import *
from moteur import *
from laser import *
from read_freq import *


init_raspberry()
configure_server()
while 1 :
	wait_for_connection()
	emetteur,commande,parametre=listen()
	if emetteur=="mobile1" and commande=="launch_game" :
		while ready() != True :
			pass
		break 

enable_moteur(True)
init_laser(status)
while 1 :
	board.output(OUT_RDY,board.HIGH)
	commande,parametre=listen()
	if commande !=0:
 		if parametre !=0 :
			print("La commande est: "+str(commande))
			print("Le parametre est :"+str(parametre))
		if commande == "laser" :
			state(parametre)
		if commande == "moteur":
			moteur(parametre)
		
		



