import time
import variables as v
from com import *
from game import *

if configuration():
	if configure_server():
		start_server_daemon()
		enable_detection("in_game",True)

while v.is_linked == False :
	time.sleep(1)

v.board.output(v.OUT_RDY,v.board.HIGH)

while v.is_linked!=v.is_playable :
	try :	
		interlocuteur,commande,parametre=listen_all()
		if interlocuteur == False :
			pass
		else :
			process_command_pre_game(interlocuteur,commande,parametre)
			v.is_playable = start_game()
			if v.is_playable :
				break
	except :
		pass

while v.is_playable :
	try :
		interlocuteur,commande,parametre=listen_all()
		if interlocuteur == False :
			pass
		else :
			process_command_in_game(interlocuteur,commande,parametre)
	except :
		pass	
print("Fin du game Bitchies! ")

