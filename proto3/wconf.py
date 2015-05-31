import variables as v
from threading import Thread


def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")


def listen(socket) :
	data= socket.recv(1024)
	if (len(data)>0) :
		cible=data.split('&')[0]
		commande=data.split('&')[1]
		parametre=data.split('&')[-1]
		return cible,commande,parametre

def listen_all():
	for key in v.dict_connected_devices :
		v.dict_connected_devices[key].setblocking(0)
		try :
			cible,commande,parametre=listen(v.dict_connected_devices[key])
			return cible,commande,parametre 			
		except :
			pass

			
def configure_server() :
	v.board.output(v.OUT_GUEST,v.board.HIGH)
	print("--- Server is being initalized ---")
	v.server.bind((v.HOST,v.PORT))
	print("--- Server has been successfully set up ---")
	v.time.sleep(0.2)
	return True

def thread_server():
	global client_socket, client_addr
	v.server.listen(6)
	while 1 :
		print("--- Server waiting for connection ---")
		client_socket, client_addr =v.server.accept()
		v.dict_connected_devices[client_addr]=client_socket
		print(client_addr , client_socket, str(len(v.dict_connected_devices)))
		v.is_linked = True
		print (v.is_linked)	
		print(str(client_addr)+ " has connected to Rpi " )

def start_server_daemon():
	print("--- Starting daemon ---")
	t_create_server = Thread(target=thread_server)
	t_create_server.setDaemon(True)
	t_create_server.start()

def print_dict():	
	print(v.dict_connected_devices)
