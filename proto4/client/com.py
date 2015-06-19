import variables as v
from threading import Thread
import commands

global ID
ID=v.dict_connected_devices

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]

def print_dict():	
	for key in ID :
		print key
		print ID[key]

def connect(addr) :
	ID[str(addr)] = dict({
		'self_ip' : str(addr),
		'sock_listen' : None ,
		'sock_send' : None,
		'is_linked' : False,
		'name' : "",
		'type' :  "android",
		'role' : "master",
		'associated_device_ip' : get_self_ip(),
		'feedback' :"True",
		})
	print("ok")

def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")

def android_send(socket,data):
	socket.send((data).encode("UTF-8"))

def raspberry_send(socket,fonction,data):
	socket.send(get_self_ip()+"&"+fonction+"&"+data)
	
def send(target,fonction,data):
	_,v.ready_send,_= v.select.select([],v.list_send,[],0)
	for sock in v.ready_send :
		if ID[target]['sock_send'] == sock :
			if ID[target]['type']=="android" :
				try :
					android_send(sock,data)
				except :
					print("Envoie a " +target +"(android), echoue")
			else :
				try :
					raspberry_send(sock,fonction,data)
				except :	
					print("Envoie a "+target+"(raspberry),echoue")

def notify_event(type_event,data):
	global message_event
	message_event=str(type_event)+data
	c.send("10.5.5.1","notify_event",message_event)
	c.send(ID[get_self_ip()]['associated_device_ip'],"notify_event",message_event)


def init_dict():
	ID["10.5.5.1"] =dict({
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
		ID["10.5.5.1"]['sock_send'].connect(('10.5.5.1',40450))
		send("10.5.5.1","setprofile","name*raspberry2*type*raspberry*role*slave_slave")
		print("Envoi configuration reussi")

	except :
		print("Configuration n'a pas marche")

	ID[get_self_ip()] = dict({
		'self_ip' :get_self_ip(),
		'sock_listen':"",
		'sock_send':"",
		'is_linked':False,
		'name' : "raspberry2",
		'type' : "raspberry",
		'role' : "slave_slave",
		'associated_device_ip': "",
		'feedback':"",
		})
	print_dict()




def link_new_device(c_addr):
	print_dict()
	if  ID[str(c_addr)]['sock_send'] == None :
		try :
			ID[str(c_addr)]['sock_send'] = v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM)
			ID[str(c_addr)]['sock_send'].connect((c_addr[0],40450))
			v.list_send.append(ID[str(c_addr)]['sock_send'])
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
	if str(c_addr[0]) != "10.5.5.1" and ID.get(str(c_addr[0])) == None:
		ID[str(c_addr[0])] = dict({
			'self_ip' :str(c_addr[0]),
			'sock_listen': c_socket,
			'sock_send':None ,
			'is_linked':False,
			'name' : "raspberry1" ,
			'type' : "raspberry",
			'role' :"slaver_master",
			'associated_device_ip': "",
			'feedback':"True",
		})
		print(ID)
		link_new_device(str(c_addr[0]))
		v.list_con.append(c_socket)
	else :
		try :
			v.list_con.remove(ID[str(c_addr[0])]['sock_listen'])
		except :
			pass
		v.list_con.append(c_socket)
		ID[str(c_addr[0])]['sock_listen'] == c_socket	

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
	if len(v.list_serv) > 0 :
		v.ready_serv,_,_ = v.select.select(v.list_serv, [],[],0) 
		for serv in v.ready_serv :
			print("--- Server waiting for connection ---")
			client_socket, client_addr = serv.accept()
			v.is_linked = True
			print (v.is_linked)	
			print(str(client_addr)+ " has connected to Rpi " )
			add_dict(client_socket,client_addr)
	else :
		return 

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

