import variables as v

def count_left(callback):
		v.l_now = datetime.datetime.now().microsecond
		v.l_delta=v.l_now-v.l_last
		v.l_echant+=1
		v.l_duree_echant+=v.l_delta 
		v.l_moyenne_echant=abs(v.l_duree_echant/v.l_echant)
		if 1750<v.l_moyenne_echant<1900 and v.l_echant>40 :
			print("touche gauche"+str(count))
			v.l_delta=0
			count+=1
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
		v.r_now = datetime.datetime.now().microsecond
		v.r_delta=v.r_now-v.r_last
		v.r_echant+=1
		v.r_duree_echant+=v.r_delta 
		v.r_moyenne_echant=abs(v.r_duree_echant/v.r_echant)
		if 1750<v.r_moyenne_echant<1900 and v.r_echant>40 :
			print("touche droit")
			v.r_delta=0
			v.r_echant=0
			v.r_duree_echant=0
			v.r_last=v.r_now
		elif v.r_moyenne_echant>1900 or 1750>v.r_moyenne_echant:
			v.r_last=v.r_now
			v.r_echant=0
			v.r_duree_echant=0
		else :
			v.r_last=v.r_now	

def count_back(callback):
		v.b_now = datetime.datetime.now().microsecond
		v.b_delta=v.b_now-v.b_last
		v.b_echant+=1
		v.b_duree_echant+=v.b_delta 
		v.b_moyenne_echant=abs(v.b_duree_echant/v.b_echant)
		print(v.b_echant,v.b_delta, v.b_moyenne_echant)
		if 1750<v.b_moyenne_echant<1900 and v.b_echant>40 :
			print("touche")
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
			
board.add_event_detect(IN_L,board.RISING,callback=count_left,bouncetime=1)
board.add_event_detect(IN_R,board.RISING,callback=count_right,bouncetime=1)
board.add_event_detect(IN_B,board.RISING,callback=count_back,bouncetime=1)
