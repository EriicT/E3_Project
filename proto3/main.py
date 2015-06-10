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

time.sleep(5)
while v.is_linked!=v.is_playable :	
	interlocuteur,commande,parametre=listen_all()
	process_command_pre_game(interlocuteur,commande,parametre)
	v.is_playable = start_game()
	
while v.is_playable :
		interlocuteur,commande,parametre=listen_all()
		process_command_pre_game(interlocuteur,commande,parametre)

print("Fin du game Bitchies! ")

