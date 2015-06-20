import time
import variables as v
from laser import *
from com import *
from game import *

init_laser("GUEST")
laser("ON")
if configuration():
	if configure_server():
		init_server()


while v.is_linked!=v.is_playable :
	thread_server()			
	interlocuteur,commande,parametre=listen_all()
	if interlocuteur == False :
		pass
	else :
		process_command_pre_game(interlocuteur,commande,parametre)			
		v.is_playable = start_game_slave()
	if v.is_playable :
		print("IN REAL GAME")
		break
	
while v.is_playable :
	thread_server()
	interlocuteur,commande,parametre=listen_all()
	if interlocuteur == False :
		pass
	else :
		process_command_in_game(interlocuteur,commande,parametre)	
		
print("Fin du game Bitchies! ")

