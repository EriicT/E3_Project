import time
from wconf import *
from variables import *
from moteur import *
from laser import *
from read_freq import *

#watchdog_moteur()
#configure_server()
start_server_daemon()
enable_moteur(True)
init_laser("GUEST")
while 1 :
	if ready_to_listen== True :
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
		
	else :
		pass	



