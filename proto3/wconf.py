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
	try :
		for key in v.dict_connected_devices :
			v.dict_connected_devices[key]['socket_connected'].setblocking(0)
			try :
				cible,commande,parametre=listen(v.dict_connected_devices[key]['socket_connected'])
				return cible,commande,parametre 			
			except :
				pass
	except :
		pass

def add_dict(c_socket,c_addr):
	v.dict_connected_devices[str(c_addr[0])] = dict({
		'self_ip' :str(c_addr[0]),
		'socket_connected': c_socket,
		'name' : "" ,
		'type' : "",
		'role' :"",
		'associated_device_ip': "",
		'feedback':"",
		})
	print v.dict_connected_devices

def set_profil(cible,data):
	global splited_data
	splited_data = str(data).split('*')
	len_data=len(splited_data)
	cursor = 0
	while cursor != len_data :
		v.dict_connected_devices[cible][splited_data[cursor]] =splited_data[cursor+1]
		cursor+=2
	print(v.dict_connected_devices)
					
def connect(c_socket):
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
#		v.dict_connected_devices[client_addr]=client_socket
#		print(client_addr , client_socket, str(len(v.dict_connected_devices)))
		add_dict(client_socket,client_addr)
		v.is_linked = True
		print (v.is_linked)	
		print(str(client_addr)+ " has connected to Rpi " )
	
	
def start_server_daemon():
	print("--- Starting daemon ---")
	v.t_create_server = Thread(target=thread_server)
	v.t_create_server.setDaemon(True)
	v.t_create_server.start()

def start_listening_daemon():
	print("--- Starting Listening daemon ---")
	v.t_listening = Thread(target=listen_all)
	v.t_listening.setDaemon(True)
	v.t_listening.start()

def print_dict():	
	print(v.dict_connected_devices)
