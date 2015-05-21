from variables import *


def moteur(commande):
	global m_last
	vitesse=commande.split('*')[0]
	angle=commande.split('*')[1]
	
	if angle.startswith("-") :
		a=float(angle[1:])
	else :
		a=float(angle)

	if vitesse.startswith("-"):
		v=(float(vitesse[1:])*0.55)+40
	else :
		v=(float(vitesse))*0.55+40
	
	if v > 100 :
		v=100

	coef = float((90-a)/90)

	PWM_MG_FW.start(0)
	PWM_MD_BW.start(0)
	PWM_MG_BW.start(0)
	PWM_MD_FW.start(0)

	m_last=datetime.datetime.now().microsecond
	
	if v ==0 and 0<a<5 :
		PWM_MG_FW.start(0)
		PWM_MD_BW.start(0)
		PWM_MG_BW.start(0)
		PWM_MD_FW.start(0)

	elif v==0 and int(angle)<-60 :
		PWM_MG_FW.start(80)
		PWM_MD_BW.start(80)
	
	elif v==0 and int(angle)>60 :
		PWM_MG_BW.start(80)
		PWM_MD_FW.start(80)
	else :
		if ( (vitesse.startswith("-") != angle.startswith("-")) and (70<a<90) ):
			PWM_MD_FW.start(v)
			PWM_MG_BW.start(v)

		elif( ((vitesse.startswith("-") and angle.startswith("-") ) or not(vitesse.startswith("-") and angle.startswith("-") )) and (70<a<90) ):
			PWM_MG_FW.start(v)
			PWM_MD_BW.start(v)
				
		elif vitesse.startswith("-") and (0<a<5):
			PWM_MG_BW.start(v)
			PWM_MD_BW.start(v)

		elif (0<a<5):
			PWM_MG_FW.start(v)
			PWM_MD_FW.start(v)
	
		elif vitesse.startswith("-") :
			if  angle.startswith("-") :
				PWM_MG_BW.start(v*coef)
				PWM_MD_BW.start(v)
			else :
				PWM_MG_BW.start(v)
				PWM_MD_BW.start(v*coef)

		else :
			if angle.startswith("-") :
				PWM_MG_FW.start(v*coef)
				PWM_MD_FW.start(v)
			else :
				PWM_MG_FW.start(v)
				PWM_MD_FW.start(v*coef)
	
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
		board.output(MD_EN,board.LOW)

