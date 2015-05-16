from variables import *
import socket
import RPi.GPIO as board
from threading import Thread

import time
import sys

def off(callback):
	board.cleanup()
	server.close()
	sys.exit("bye")

def listen() :
	global client_socket	
	data= client_socket.recv(1024)
	if (len(data)>0) :
		emetteur=data.split('&')[0]
		commande=data.split('&')[1]
		parametre=data.split('&')[-1]
		return emetteur,commande,parametre
	#	print("La cible est :" + str(cible) )
	#	print("La commande est :" +str(commande))
	#	print("Le param?tre est :" + str(parametre))
	return 	(0,0)
#board.add_event_detect(32,board.RISING,callback = off, bouncetime = 300)

def configure_server() :
	global PORT,HOST,client_socket
	board.output(OUT_GUEST,board.HIGH)
	print("--- Server is being initalized ---")
	server.bind((HOST,PORT))
	print("--- Server has been successfully set up ---")

def wait_for_connection():
	global server
	server.listen(4)
	print("--- Server waiting for connection ---")
	client_socket, client_addr =server.accept()
	print(str(client_addr)+ " has connected to Rpi " )	

def start_server_daemon():
	print("Starting daemon")
	t_create_server = Thread(target=configure_server)
	t_create_server.setDaemon(True)
	t_create_server.start()

def change_status(callbakc):	
	global status
	if status="HOST" :
		status="GUEST"
	else :
		status="HOST"
	wait_status+=5

def init_raspberry(status):
	global status 
	board.add_detection_event(38,board.RISING,callback=change_status,bouncetime=1)
	time.sleep(wait_status)
	board.remove_detection_event(38)

def ready():
	global nb_p, p_connected, nb_rpi, rpi_connected
	if nb_p=p_connected and nb_rpi== rpi_connected :
		return True
	else :
		return False
