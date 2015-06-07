
import variables as v 
import os

def set_host():
	os.system("sudo ifdown wlan0")
	os.system("sudo cp wifi/interfaces_last /etc/network/interfaces")
	os.system("sudo cp wifi/hostapd_host /etc/default/hostapd")
	os.system("sudo ifup wlan0")
	try :
		os.system("sudo service isc-dhcp-server start")
	except :
		os.system("sudo service isc-dhcp-server restart")
	try :	
		os.system("sudo service hostapd start")
	except : 
		os.system("sudo service hostapd restart")
	v.board.remove_event_detect(v.IN_SELECT)
def set_guest():
	os.system("sudo service networking stop")
	os.system("sudo service isc-dhcp-server stop")
	os.system("sudo ifdown wlan0")
	os.system("sudo cp wifi/interfaces_guest /etc/network/interfaces")
	os.system("sudo cp wifi/hostapd_guest /etc/default/hostapd")
	os.system("sudo ifup wlan0")
	os.system("ifconfig")
	#os.system("sudo service networking restart")
	v.board.remove_event_detect(v.IN_SELECT)
def switch(callback):
	print("configuration " + str(v.configuration))
	v.time.sleep(0.5)
	if v.configuration == "HOST" :
		set_guest()
		v.configuration = "GUEST"
	else :
		set_host()
		v.configuration = "HOST"
