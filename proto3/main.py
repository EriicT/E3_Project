import time
import variables as v
from wconf import *
from moteur import *
from laser import *
from read_freq import *
global is_linked
#watchdog_moteur()
if configure_server() :
	start_server_daemon()

#start_server_daemon()
enable_moteur(True)
init_laser("GUEST")
time.sleep(10)
print(v.is_linked)
while v.is_linked==True :	
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

print("Personne au bout de 10 sec ! ")

