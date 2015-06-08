
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
		r_now = datetime.datetime.now().microsecond
		r_delta=r_now-r_last
		r_echant+=1
		r_duree_echant+=r_delta 
		r_moyenne_echant=abs(r_duree_echant/r_echant)
		if v.set_laser[v.configuration]['min_period']<v.r_moyenne_echant<v.set_laser[v.configuration]['max_period'] and v.set_laser[v.configuration]['echant'] > v.r_echant:
			r_frequence= round(float(1/(r_moyenne_echant*10E-7)),0)
			print("touche droit " +str(r_frequence))
			r_delta=0
			r_echant=0
			r_duree_echant=0
			r_last=r_now
		elif r_moyenne_echant>1900 or 1750>r_moyenne_echant:
			r_last=r_now
			r_echant=0
			r_duree_echant=0
		else :
			r_last=r_now	

def count_back(callback):
		b_now = datetime.datetime.now().microsecond
		b_delta=b_now-b_last
		b_echant+=1
		b_duree_echant+=b_delta 
		b_moyenne_echant=abs(b_duree_echant/b_echant)
		if v.set_laser[v.configuration]['min_period']<v.b_moyenne_echant<v.set_laser[v.configuration]['max_period'] and v.set_laser[v.configuration]['echant'] > v.b_echant :
			b_frequence= round(float(1/(b_moyenne_echant*10E-7)),0)
			print("touche arriere " + str(b_frequence))
			b_delta=0
			b_echant=0
			b_duree_echant=0
			b_last=b_now
		elif b_moyenne_echant>1900 or 1750>b_moyenne_echant:
			b_last=b_now
			b_echant=0
			b_duree_echant=0
		else :
			b_last=b_now	
			
