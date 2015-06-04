import time
import variables as v
from wconf import *
from moteur import *
from laser import *
from read_freq import *
#from game import *

if configure_server():
	start_server_daemon()

while v.is_linked == False :
	time.sleep(5)

while v.is_linked!=v.is_playable :	
	v.board.output(v.OUT_RDY,v.board.HIGH)
	try : 
		interlocuteur,commande,parametre=listen_all()
		print("La commande vient de :"+str(interlocuteur))
		print("La commande est: "+str(commande))
		print("Le parametre est :"+str(parametre))
		if commande =="setprofil" :
			print("Set Profil")
			set_profil(interlocuteur,parametre)		
		elif commande =="setgame":
			set_game(parametre)
		v.is_playable = start_game()
		if v.is_playable == True :
			print("Game Launched")
	except :
		pass

print("IS IG")
while v.is_playable :
	try :
		interlocuteur,commande,parametre=listen_all()
		print("IG intelocuteur : "+ str(interlocuteur))
		print("IG commande : " + str(commande) )
		print("IG commande : " + str(parametre) )
		if commande == "laser" :
			state(parametre)
		elif commande == "moteur":
			moteur(parametre)
	except :
		pass
print("Fin du game Bitchies! ")

