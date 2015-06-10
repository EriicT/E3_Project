
import variables as v

def count_left(callback):
		v.l_now = v.datetime.datetime.now().microsecond
		v.l_delta=v.l_now-v.l_last
		v.l_echant+=1
		v.l_duree_echant+=v.l_delta 
		v.l_moyenne_echant=abs(v.l_duree_echant/v.l_echant)
		if v.set_laser[v.configuration]['min_period']<v.l_moyenne_echant<v.set_laser[v.configuration]['max_period'] and v.set_laser[v.configuration]['echant']>v.l_echant :
			v.l_frequence= round(float(1/(v.l_moyenne_echant*10E-7)),0)
			print("touche gauche " + str(v.l_frequence) + str(v.configuration))
			v.l_delta=0
			v.l_echant=0
			v.l_duree_echant=0
			v.l_last=v.l_now
		elif v.l_moyenne_echant>1900 or 1750>v.l_moyenne_echant:
			v.l_last=v.l_now
			v.l_echant=0
			v.l_duree_echant=0
		else :
			v.l_last=v.l_now	

def count_right(callback):
		v.r_now =v.datetime.datetime.now().microsecond
		v.r_delta=v.r_now-v.r_last
		v.r_echant+=1
		v.r_duree_echant+=v.r_delta 
		v.r_moyenne_echant=abs(v.r_duree_echant/v.r_echant)
		if v.set_laser[v.configuration]['min_period']<v.r_moyenne_echant<v.set_laser[v.configuration]['max_period'] and v.set_laser[v.configuration]['echant'] > v.r_echant:
			v.r_frequence= round(float(1/(v.r_moyenne_echant*10E-7)),0)
			print("touche droit " +str(r_frequence))
			v.r_delta=0
			v.r_echant=0
			v.r_duree_echant=0
			v.r_last=v.r_now
		elif v.r_moyenne_echant>1900 or 1750>v.r_moyenne_echant:
			v.r_last=r_now
			v.r_echant=0
			v.r_duree_echant=0
		else :
			v.r_last=v.r_now	

def count_back(callback):
		v.b_now = v.datetime.datetime.now().microsecond
		v.b_delta=v.b_now-v.b_last
		v.b_echant+=1
		v.b_duree_echant+=b_delta 
		v.b_moyenne_echant=abs(v.b_duree_echant/v.b_echant)
		if v.set_laser[v.configuration]['min_period']<v.b_moyenne_echant<v.set_laser[v.configuration]['max_period'] and v.set_laser[v.configuration]['echant'] > v.b_echant :
			v.b_frequence= round(float(1/(v.b_moyenne_echant*10E-7)),0)
			print("touche arriere " + str(v.b_frequence))
			v.b_delta=0
			v.b_echant=0
			v.b_duree_echant=0
			v.b_last=v.b_now
		elif v.b_moyenne_echant>1900 or 1750>v.b_moyenne_echant:
			v.b_last=v.b_now
			v.b_echant=0
			v.b_duree_echant=0
		else :
			v.b_last=v.b_now	
			
