

import os
import variables as v 

def set_host():
	os.system("sudo ifdown wlan0")
	os.system("sudo cp interfaces_last /etc/network/interfaces")
	os.system("sudo cp hostapd_p.conf /etc/default/hostapd")
	os.system("sudo ifup wlan0")
	os.system("sudo service isc-dhcp-server start")
	os.system("sudo service hostapd restart")
	v.board.remove_event_detect(v.IN_SELECT)

def set_guest():
	os.system("sudo service networking stop")
	os.system("sudo service isc-dhcp-server stop")
	os.system("sudo ifdown wlan0")
	os.system("sudo cp interfaces_guest /etc/network/interfaces")
	os.system("sudo cp hostapd_guest /etc/default/hostapd")
	os.system("sudo ifup wlan0")
	os.system("ifconfig")
	#os.system("sudo service networking restart")
	v.board.remove_event_detect(v.IN_SELECT)

def switch(callback):
	print("configuration " + str(v.configuration))
	v.time.sleep(0.5)
	if v.configuration == "HOST" :
		v.configuration = "GUEST"
		set_guest()
	else :
		v.configuration = "HOST"
		set_host()
