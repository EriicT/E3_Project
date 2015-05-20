from variables import *


def moteur(commande):
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

	if ( (vitesse.startswith("-") != angle.startswith("-")) and (80<a<90) ):
		PWM_MD_FW.start(v)
		PWM_MG_BW.start(v)
	elif v < 10 : 
		pass
	elif( ((vitesse.startswith("-") and angle.startswith("-") ) or not(vitesse.startswith("-") and angle.startswith("-") )) and (80<a<90) ):
		PWM_MG_FW.start(v)
		PWM_MD_BW.start(v)
				
	elif vitesse.startswith("-") and (0<a<10):
		PWM_MG_BW.start(v)
		PWM_MD_BW.start(v)

	elif (0<a<10):
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
	
	

def enable_moteur(value) :
	if value == True :
		board.output(MG_EN,board.HIGH)
		board.output(MD_EN,board.HIGH)
	else :
		board.output(MG_EN,board.LOW)
		board.output(MD_EN,board.LOW)
