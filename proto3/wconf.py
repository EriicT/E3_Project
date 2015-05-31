import variables as v
import socket
import RPi.GPIO as board
from threading import Thread
import time
import sys

def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")

def listen() :	
	data= client_socket.recv(1024)
	if (len(data)>0) :
		cible=data.split('&')[0]
		commande=data.split('&')[1]
		parametre=data.split('&')[-1]
		return commande,parametre
	#	print("La cible est :" + str(cible) )
	#	print("La commande est :" +str(commande))
	#	print("Le param?tre est :" + str(parametre))
	return 	(0,0)
#board.add_event_detect(32,board.RISING,callback = off, bouncetime = 300)

def configure_server() :
	v.board.output(v.OUT_GUEST,board.HIGH)
	print("--- Server is being initalized ---")
	v.server.bind((v.HOST,v.PORT))
	print("--- Server has been successfully set up ---")
	time.sleep(0.2)
	return True

def thread_server():
	#global v.server, v.dict_connected_devices, v.is_linked
	v.server.listen(6)
	while 1 :
		print("--- Server waiting for connection ---")
		client_socket, client_addr =v.server.accept()
		v.dict_connected_devices[client_addr]=client_socket
		print(client_addr , client_socket)
		v.is_linked = True
		print (v.is_linked)	
		print(str(client_addr)+ " has connected to Rpi " )

def start_server_daemon():
	print("--- Starting daemon ---")
	t_create_server = Thread(target=thread_server)
	t_create_server.setDaemon(True)
	t_create_server.start()

	
	
