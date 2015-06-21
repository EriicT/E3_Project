import variables as v


def moteur(commande):
	try :
		global m_last, vitesse_r,angle_r,coefficient,vitesse_c
		vitesse_r =float(commande.split('*')[0])
		angle_r =float(commande.split('*')[1])

		v.PWM_MG_FW.start(0)
		v.PWM_MD_BW.start(0)
		v.PWM_MG_BW.start(0)
		v.PWM_MD_FW.start(0)
	
		vitesse_c = round(float((0.5*abs(vitesse_r))+50),0) 
		coefficient=round(float((90-abs(angle_r))/90),0)
		v.m_last=v.datetime.datetime.now().microsecond
		try :
			if -90<angle_r<-50 :
				v.board.output(v.OUT_L,v.board.HIGH)
				v.board.output(v.OUT_R,v.board.LOW)
			elif 50<angle_r<90 :
				v.board.output(v.OUT_L,v.board.LOW)
				v.board.output(v.OUT_R,v.board.HIGH)
			else :
				v.board.output(v.OUT_R,v.board.LOW)
				v.board.output(v.OUT_L,v.board.LOW)
		except :
			print("probleme tournant")
	
		if vitesse_r==0 :
			if angle_r > 50 : 
				v.PWM_MG_FW.start(angle_r)
				v.PWM_MD_BW.start(angle_r)
			elif angle_r< -50  :
				v.PWM_MG_BW.start(abs(angle_r))
				v.PWM_MD_FW.start(abs(angle_r))
			else :
				v.PWM_MG_FW.start(0)
				v.PWM_MG_BW.start(0)
				v.PWM_MD_FW.start(0)
				v.PWM_MD_BW.start(0)
				
		elif vitesse_r > 1 :
			if angle_r > 5 :
				v.PWM_MG_FW.start(vitesse_c)
				v.PWM_MD_FW.start(vitesse_c*coefficient)
			elif angle_r < -5 :
				v.PWM_MG_FW.start(vitesse_c*coefficient)
				v.PWM_MD_FW.start(vitesse_c)
			else :
				v.PWM_MG_FW.start(vitesse_c)
				v.PWM_MD_FW.start(vitesse_c)
		elif vitesse_r <-1 :
			if angle_r >5 :
				v.PWM_MG_BW.start(vitesse_c)
				v.PWM_MD_BW.start(vitesse_c*coefficient)
			elif angle_r < -5 :
				v.PWM_MG_BW.start(vitesse_c*coefficient)
				v.PWM_MD_BW.start(vitesse_c)
			else : 
				v.PWM_MG_BW.start(vitesse_c)
				v.PWM_MD_BW.start(vitesse_c)
				
		else :
			v.PWM_MG_FW.start(0)
			v.PWM_MG_BW.start(0)
			v.PWM_MD_FW.start(0)
			v.PWM_MD_BW.start(0)		 
	except :
		print("probleme")

def enable_moteur(value) :
	if value == True :
		v.board.output(v.MG_EN,v.board.HIGH)
		v.board.output(v.MD_EN,v.board.HIGH)
	else :
		v.board.output(v.MG_EN,v.board.LOW)
		v.board.output(v.MD_EN,v.board.LOW)
	


