import variables as v
from threading import Thread
import commands

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]

def print_dict():	
	for key in v.dict_connected_devices :
		print key
		print v.dict_connected_devices[key]

def connect(addr) :
	v.dict_connected_devices[str(addr)] = dict({
		'self_ip' : str(addr),
		'sock_listen' : None ,
		'sock_send' : v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM),
		'is_linked' : False,
		'name' : "",
		'type' :  "androi",
		'role' : "master",
		'associated_device_ip' : get_self_ip(),
		'feedback' :"True",
		})
	v.dict_connected_devices[str(addr)]['sock_send'].connect((addr,40450))
	send(addr,"hello","monpetitmate")

def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")

def send(target,fonction,data):
	global message 
	if target != None :
		message = get_self_ip()+"&" + fonction+ "&"  +data
		print message
		try :
			v.dict_connected_devices[str(target)]['sock_send'].send(message.encode("UTF-8"))	
		except :
			print("Fail message")

def notify_event(type_event,data):
	global message_event
	message_event=str(type_event)+data
	c.send("10.5.5.1","notify_event",message_event)
	c.send(v.dict_connected_devices[get_self_ip()]['associated_device_ip'],"notify_event",message_event)


def init_dict():
	global conf_name,conf_role,conf_type
	conf_type="raspberry"
	conf_name="slave"
	conf_role="slave_slave"
	v.dict_connected_devices["10.5.5.1"] =dict({
		'self_ip' : "10.5.5.1",
		'sock_listen' :"",
		'sock_send' : v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM),			
		'is_linked':"False",
		'name' : "Rasberry Master",
		'type' : "Raspberry",
		'role' : "slave_master",
		'associated_device_ip' : "",
		'feedback' : "",
	})
	try :
		v.time.sleep(1)
		print("jvais me connecter au host")
		v.dict_connected_devices["10.5.5.1"]['sock_send'].connect(('10.5.5.1',40450))
		send("10.5.5.1","setprofile","name*raspberry2*type*raspberry*role*slave_slave")
		print("Envoi configuration reussi")
	except :
		print("Configuration n'a pas marche")

	v.dict_connected_devices[get_self_ip()] = dict({
		'self_ip' :get_self_ip(),
		'sock_listen':"",
		'sock_send':"",
		'is_linked':False,
		'name' : conf_name,
		'type' : conf_type,
		'role' : conf_role,
		'associated_device_ip': "",
		'feedback':"",
		})




def link_new_device(c_addr):
	print_dict()
	if  v.dict_connected_devices[str(c_addr)]['sock_send'] == None :
		try :
			v.dict_connected_devices[str(c_addr)]['sock_send'] = v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM)
			v.dict_connected_devices[str(c_addr)]['sock_send'].connect((c_addr[0],40450))
		
		except :
			print("Pas reussi a se connecter en retour")

def listen_all():
	global ready_con
	ready_con,_,_= v.select.select(v.list_con,[],[],0)
	for sock in ready_con:
		data,addr = sock.recvfrom(1024)
		if len(data)>1 :
			print data
			cible=data.split('&')[0]
			commande=data.split('&')[1]
			parametre=data.split('&')[-1]	
			return cible,commande,parametre
		else : 
			return False, False, False
	return False, False, False
		
def add_dict(c_socket,c_addr):
	print(" add dict ")
	print_dict()
	if str(c_addr[0]) != "10.5.5.1" :
		v.dict_connected_devices[str(c_addr[0])] = dict({
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
		print(v.dict_connected_devices)
		link_new_device(str(c_addr[0]))
	v.list_con.append(c_socket)

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
	v.ready_serv,_,_ = v.select.select(v.list_serv, [],[],0) 
	for serv in v.ready_serv :
		print("--- Server waiting for connection ---")
		client_socket, client_addr = serv.accept()
		v.is_linked = True
		print (v.is_linked)	
		print(str(client_addr)+ " has connected to Rpi " )
		add_dict(client_socket,client_addr)

def init_server():	
	v.server.listen(6)
	v.list_serv.append(v.server)
	v.ready_serv,_,_= v.select.select(v.list_serv,[],[],0)
	init_dict()

def start_server_daemon():
	print("--- Starting daemon ---")
	v.t_create_server = Thread(target=thread_server)
	v.t_create_server.setDaemon(True)
	v.t_create_server.start()


def stop_server():
	v.t_create_server.join()

