import time
import variables as v
from com import *
from game import *

if configuration():
	if configure_server():
		init_server()

v.board.output(v.OUT_RDY,v.board.HIGH)

while v.is_linked!=v.is_playable :
	start_server_daemon()			
	interlocuteur,commande,parametre=listen_all()
	if interlocuteur == False :
		pass
	else :
	#	print(interlocuteur,commande,parametre)
		process_command_pre_game(interlocuteur,commande,parametre)			
		v.is_playable = start_game()
	
	if v.is_playable :
			break


while v.is_playable :
	interlocuteur,commande,parametre=listen_all()
	if interlocuteur == False :			
		pass
	else :
		process_command_in_game(interlocuteur,commande,parametre)
		
print("Fin du game Bitchies! ")

