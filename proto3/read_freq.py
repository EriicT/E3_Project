from variables import *
count=0
def count_left(callback):
		global count,l_first,l_last,l_delta,l_duree_echant,l_now,l_echant,l_moyenne_echant,l_frequence
		l_now = datetime.datetime.now().microsecond
		l_delta=l_now-l_last
		l_echant+=1
		l_duree_echant+=l_delta 
		l_moyenne_echant=abs(l_duree_echant/l_echant)
		if 1750<l_moyenne_echant<1900 and l_echant>40 :
			print("touche gauche"+str(count))
			l_delta=0
			count+=1
			l_echant=0
			l_duree_echant=0
			l_last=l_now
		elif l_moyenne_echant>1900 or 1750>l_moyenne_echant:
			l_last=l_now
			l_echant=0
			l_duree_echant=0
		else :
			l_last=l_now	

def count_right(callback):
		global r_first,r_last,r_delta,r_duree_echant,r_now,r_echant,r_moyenne_echant,r_frequence
		r_now = datetime.datetime.now().microsecond
		r_delta=r_now-r_last
		r_echant+=1
		r_duree_echant+=r_delta 
		r_moyenne_echant=abs(r_duree_echant/r_echant)
		if 1750<r_moyenne_echant<1900 and r_echant>40 :
			print("touche droit")
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
		global b_first,b_last,b_delta,b_duree_echant,b_now,b_echant,b_moyenne_echant,b_frequence
		b_now = datetime.datetime.now().microsecond
		b_delta=b_now-b_last
		b_echant+=1
		b_duree_echant+=b_delta 
		b_moyenne_echant=abs(b_duree_echant/b_echant)
		print(b_echant,b_delta, b_moyenne_echant)
		if 1750<b_moyenne_echant<1900 and b_echant>40 :
			print("touche")
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
			
board.add_event_detect(IN_L,board.RISING,callback=count_left,bouncetime=1)
board.add_event_detect(IN_R,board.RISING,callback=count_right,bouncetime=1)
board.add_event_detect(IN_B,board.RISING,callback=count_back,bouncetime=1)
