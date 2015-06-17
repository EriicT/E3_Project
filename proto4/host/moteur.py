import variables as v


def moteur(commande):
	vitesse_r =float(commande.split('*')[0])
	angle_r =float(commande.split('*')[1])

	v.PWM_MG_FW.start(0)
	v.PWM_MD_BW.start(0)
	v.PWM_MG_BW.start(0)
	v.PWM_MD_FW.start(0)
	
	vitesse_c = round(float((0.5*abs(vitesse_r))+50),2) 
	coefficient=round(float((90-abs(angle_r))/90),2)
	v.m_last=v.datetime.datetime.now().microsecond
	
	if vitesse_r==0 :
		v.PWM_MG_FW.start(0)
		v.PWM_MG_BW.start(0)
		v.PWM_MD_FW.start(0)
		v.PWM_MD_BW.start(0)

	elif -5<angle_r<5 :
		if vitesse_r> 1:
			v.PWM_MG_FW.start(vitesse_c)
			v.PWM_MD_FW.start(vitesse_c)
		else : 
			v.PWM_MG_BW.start(vitesse_c)
			v.PWM_MD_BW.start(vitesse_c)
	elif vitesse_r > 1 :
		if angle_r > 5 :
			v.PWM_MG_FW.start(vitesse_c)
			v.PWM_MD_FW.start(vitesse_c*coefficient)
		else :
			v.PWM_MG_FW.start(vitesse_c*coefficient)
			v.PWM_MD_FW.start(vitesse_c)
	elif vitesse_r <-1 :
		if angle_r >5 :
			v.PWM_MG_BW.start(vitesse_c)
			v.PWM_MD_BW.start(vitesse_c*coefficient)
		else :
			v.PWM_MG_BW.start(vitesse_c*coefficient)
			v.PWM_MD_BW.start(vitesse_c)
	else :
		v.PWM_MG_FW.start(0)
		v.PWM_MG_BW.start(0)
		v.PWM_MD_FW.start(0)
		v.PWM_MD_BW.start(0)		 
	
def watchdog_moteur():
	v.m_now = datetime.datetime.now().microsecond
	v.delta=v.m_now -v.m_last
	print(v.delta)
	if abs( v.delta ) > 1000000 :
		v.PWM_MG_FW.start(0)
		v.PWM_MG_BW.start(0)
		v.PWM_MD_FW.start(0)
		v.PWM_MD_BW.start(0)
	else : 
		pass		
	
	m_watchdog=threading.Timer(1,watchdog_moteur)
	m_watchdog.start()

def enable_moteur(value) :
	if value == True :
		v.board.output(v.MG_EN,v.board.HIGH)
		v.board.output(v.MD_EN,v.board.HIGH)
	else :
		v.board.output(v.MG_EN,v.board.LOW)
		v.board.output(v.MD_EN,v.board.LOW)
	


