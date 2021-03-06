import variables as v
from threading import Thread
import commands
#import database as d

global ID
ID = v.dict_connected_devices

def get_self_ip():
	return str(commands.getoutput("hostname -I"))[:-1]

def print_dict():	
	for key in ID :
		print key
		print ID[key]


def off(callback):
	v.board.cleanup()
	v.server.close()
	sys.exit("bye")

def android_send(socket,data):
	socket.send((data).encode("UTF-8"))
	print data

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
		
	#if target != None :
	#	print (message, "to ", target)
	#	print_dict()
	#	ID[target]['sock_send'].send(message.encode("UTF-8"))	

def notify_event(type_event,data):
	global message_event
	message_event=str(type_event)+data
#	d.write(message_event)	

def init_dict():
	ID[get_self_ip()] = dict({
		'self_ip' :get_self_ip(),
		'sock_listen':"",
		'sock_send':"",
		'is_linked':False,
		'name' : "Eric",
		'type' : "raspberry",
		'role' : "slave_master",
		'associated_device_ip': "",
		'feedback':"True",
		
	})

def link_new_device(c_addr):
	v.time.sleep(1)
	if  ID[str(c_addr)]['sock_send'] == None :
		try :
			ID[str(c_addr)]['sock_send'] = v.socket.socket(v.socket.AF_INET,v.socket.SOCK_STREAM)
			ID[str(c_addr)]['sock_send'].connect((str(c_addr),40450))
			v.list_send.append(ID[str(c_addr)]['sock_send'])
			print("connexion a ", c_addr)	
			print(ID[str(c_addr)]['sock_send'])		
		except :
			print("Pas reussi a se connecter en retour")

def listen_all():
	global ready_con
	ready_con,_,_= v.select.select(v.list_con,[],[],0)
	for sock in ready_con:
		try :
			data,addr = sock.recvfrom(1024)
			if len(data)>1 : 
				cible=data.split('&')[0]
				commande=data.split('&')[1]
				parametre=data.split('&')[-1]	
				return cible,commande,parametre
			else : 
				return False, False, False
		except :
			return False,False,False
	return False, False, False
		
		
def add_dict(c_socket,c_addr):
	print(" add dict ")
	if ID.get(str(c_addr[0])) == None:
		ID[str(c_addr[0])] = dict({
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
		v.list_con.append(c_socket)
		print c_socket
		print(v.list_con[0])
		link_new_device(str(c_addr[0]))
		send(str(c_addr[0]),"hello","you*fdp")
	else :
		v.list_con.remove(ID[str(c_addr[0])]['sock_listen'])
		v.list_con.append(c_socket)
		ID[str(c_addr[0])]['sock_listen'] == c_socket	

def configure_server() :
#	v.board.output(v.OUT_GUEST,v.board.HIGH)
	print("--- Server is being initalized ---")
	print(" MY IP IS " + str( v.HOST) )
	v.server.bind((v.HOST,v.PORT))
	print("--- Server has been successfully set up ---")
	v.time.sleep(0.2)
	print_dict()
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

def start_server_daemon():
#	print("--- Starting daemon ---")
	v.t_create_server = Thread(target=thread_server)
	v.t_create_server.setDaemon(True)
	v.t_create_server.start()


def stop_server():
	v.t_create_server.join()
