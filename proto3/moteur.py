from variables import *


def moteur(commande):
	global m_last
	vitesse_r =float(commande.split('*')[0])
	angle_r =float(commande.split('*')[1])

	PWM_MG_FW.start(0)
	PWM_MD_BW.start(0)
	PWM_MG_BW.start(0)
	PWM_MD_FW.start(0)
	
	vitesse_c = round(float((0.5*abs(vitesse_r))+50),2) 
	coefficient=round(float((90-abs(angle_r))/90),2)
	m_last=datetime.datetime.now().microsecond
	
	if vitesse_r==0 :
		PWM_MG_FW.start(0)
		PWM_MG_BW.start(0)
		PWM_MD_FW.start(0)
		PWM_MD_BW.start(0)

	elif -5<angle_r<5 :
		if vitesse_r> 1:
			PWM_MG_FW.start(vitesse_c)
			PWM_MD_FW.start(vitesse_c)
		else : 
			PWM_MG_BW.start(vitesse_c)
			PWM_MD_BW.start(vitesse_c)
	elif vitesse_r > 1 :
		if angle_r > 5 :
			PWM_MG_FW.start(vitesse_c)
			PWM_MD_FW.start(vitesse_c*coefficient)
		else :
			PWM_MG_FW.start(vitesse_c*coefficient)
			PWM_MD_FW.start(vitesse_c)
	elif vitesse_r <-1 :
		if angle_r >5 :
			PWM_MG_BW.start(vitesse_c)
			PWM_MD_BW.start(vitesse_c*coefficient)
		else :
			PWM_MG_BW.start(vitesse_c*coefficient)
			PWM_MD_BW.start(vitesse_c)
	else :
		PWM_MG_FW.start(0)
		PWM_MG_BW.start(0)
		PWM_MD_FW.start(0)
		PWM_MD_BW.start(0)		 
	
def watchdog_moteur():
	global m_last
	m_now = datetime.datetime.now().microsecond
	delta=m_now -m_last
	print(delta)
	if abs( delta ) > 1000000 :
		PWM_MG_FW.start(0)
		PWM_MG_BW.start(0)
		PWM_MD_FW.start(0)
		PWM_MD_BW.start(0)
	else : 
		pass		
	
	m_watchdog=threading.Timer(1,watchdog_moteur)
	m_watchdog.start()

def enable_moteur(value) :
	if value == True :
		board.output(MG_EN,board.HIGH)
		board.output(MD_EN,board.HIGH)
	else :
		board.output(MG_EN,board.LOW)
<<<<<<< HEAD
		board.output(MD_EN,board.LOW)
=======
		board.output(MD_EN,board.LOW)

>>>>>>> 138cf84152a1d84c7998f611692ccb4146137473
