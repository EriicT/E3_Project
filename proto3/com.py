import variables as v
from threading import Thread
import commands

def print_dict():	
	for key in v.dict_connected_devices :
		print key
		print v.dict_connected_devices[key]


def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")



def send(target,fonction,data):
	global message 
	message = target +"&" + fonction+ "&"  +data
	try :
		v.dict_connected_devices[target]['sock_send'].send(message)	
	except :
		print("Fail message")

def listen(socket) :
	data= socket.recv(1024)
	if (len(data)>0) :
		cible=data.split('&')[0]
		commande=data.split('&')[1]
		parametre=data.split('&')[-1]
		return cible,commande,parametre


def link_new_device(c_addr):
	for key in v.dict_connected_devices :
		if key != (v.HOST,v.PORT) and v.dict_connected_devices[c_addr]['sock_send'] == None :
			v.dict_connected_devices[c_addr]['sock_send'] = v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM)
			try :
				v.dict_connected_devices[c_addr]['sock_send'].connect((c_addr[0],40450))
				print("Connexion reussie")
			except :
				print("Ca n'a pas marche")

def listen_all():
	try :
		for key in v.dict_connected_devices :
			v.dict_connected_devices[key]['sock_listen'].setblocking(0)
			try :
				cible,commande,parametre=listen(v.dict_connected_devices[key]['sock_listen'])
				return cible,commande,parametre 			
			except :
				pass
	except :
		pass


def add_dict(c_socket,c_addr):
	v.dict_connected_devices[c_addr] = dict({
		'self_ip' :str(c_addr[0]),
		'sock_listen': c_socket,
		'sock_send':None ,
		'is_linked':False,
		'name' : "" ,
		'type' : "",
		'role' :"",
		'associated_device_ip': "",
		'feedback':"",
		})


def configure_server() :
	v.board.output(v.OUT_GUEST,v.board.HIGH)
	print("--- Server is being initalized ---")
	print(" MY IP IS " + str( v.HOST) )
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
		link_new_device(client_addr)	
	
def start_server_daemon():
	print("--- Starting daemon ---")
	v.t_create_server = Thread(target=thread_server)
	v.t_create_server.setDaemon(True)
	v.t_create_server.start()


