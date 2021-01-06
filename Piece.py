from PIL import Image, ImageTk
from tkinter import NW
from math import fabs

class Piece:
	def __init__(self,x:int,y:int,typ:str,color:chr):
		self.x = x
		self.y = y
		self.typ = typ
		self.color = color
		self.img = ImageTk.PhotoImage(Image.open("imgs\\"+color+"_"+typ+".png").resize((64,64)))
		self.selected = False
		self.all=[]
		self.alive = True
		self.firstMove = True

	def draw(self,can):
		if not self.alive:
			return 0
		can.create_image((self.x)*80 -35*2,(self.y)*80 -35*2, anchor=NW, image=self.img)
		if self.selected:
			can.create_oval(self.x*80-40*2, self.y*80-40*2, self.x*80, self.y*80, outline="#FF0000", width=4)
			for i in self.openBlocks():
				can.create_oval(i[0]*80-40*2, i[1]*80-40*2, i[0]*80, i[1]*80, outline="#FF0000", width=4)
				
		#print("imgs\\"+self.color+"_"+self.typ+".png")

	def click(self,m):
		if self.x*80-80 < m.x < self.x*80 and self.y*80-80 < m.y < self.y*80:
			#print(self.typ,self.color)
			self.selected = not self.selected
		elif self.selected:
			self.moveTo(m.x//80 +1,m.y//80 +1)
		else:
			self.selected = False

	def detectMove(self,x1,y1):
		col = (self.color == "w")*2 -1
		########################## ROOK DETECT ##########################
		if self.typ == "rook":
			wayx = range(min(self.x,x1),max(self.x,x1)+1)
			wayy = range(min(self.y,y1),max(self.y,y1)+1)
			for i in self.all:
				if i.x == x1 and i.y == y1 and i.color != self.color:
					continue
				
				if i.x in wayx and i.y in wayy:
					if i.x == self.x and i.y == self.y:
						continue
					return False
					
			return self.x == x1 or self.y == y1
		
		########################## PAWN DETECT ##########################
		if self.typ == "pawn":
			wayy = range(min(self.y,y1),max(self.y,y1)+1)
			for i in self.all:
				if i.x == self.x and i.y in wayy:
					if i.x == self.x and i.y == self.y:
						continue
					return False
			
			
			if col*self.y <= col*y1:
				return False
			if fabs(self.x - x1) >1:
				return False
			if self.x != x1 and fabs(self.x - x1) == 1:
				for i in self.all:
					if i.here(x1*80-35*2,y1*80-35*2):
						if i.color is not self.color:
							return True
				return False
			if col*(self.y - y1) - self.firstMove <= 1:
				return True
		
		########################## BISHOP DETECT ##########################
		if self.typ == "bishop":
			wayx = list(range(self.x, x1 + int( (x1-self.x)/fabs(x1-self.x) ), int((x1-self.x)/fabs(x1-self.x))))
			wayy = list(range(self.y, y1 + int( (y1-self.y)/fabs(y1-self.y) ), int((y1-self.y)/fabs(y1-self.y))))
			way = [(wayx[i],wayy[i]) for i in range(len(wayx))]
			for i in self.all:
				if i.x == x1 and i.y == y1 and i.color != self.color:
					break
				if (i.x,i.y) in way:
				#if i.x in wayx and i.y in wayy :
					if i.x==self.x and i.y==self.y:
						continue
					#print(i.typ,i.color,i.x,i.y,"\n",list(wayx),list(wayy),way)
					return False
				
			return fabs(self.x-x1) == fabs(self.y-y1)
		
		########################## QUEEN DETECT ##########################
		if self.typ == "queen":
			if fabs(self.x-x1) == fabs(self.y-y1):
				wayx = list(range(self.x, x1 + int( (x1-self.x)/fabs(x1-self.x) ), int((x1-self.x)/fabs(x1-self.x))))
				wayy = list(range(self.y, y1 + int( (y1-self.y)/fabs(y1-self.y) ), int((y1-self.y)/fabs(y1-self.y))))
				way = [(wayx[i],wayy[i]) for i in range(len(wayx))]
				for i in self.all:
					if i.x == x1 and i.y == y1 and i.color != self.color:
						continue
					if (i.x,i.y) in way:
					#if i.x in wayx and i.y in wayy :
						if i.x==self.x and i.y==self.y:
							continue
						#print(i.typ,i.color,i.x,i.y,"\n",list(wayx),list(wayy),way)
						return False
			if self.x == x1 or self.y == y1:
				wayx = range(min(self.x,x1),max(self.x,x1)+1)
				wayy = range(min(self.y,y1),max(self.y,y1)+1)
				for i in self.all:
					if i.x == x1 and i.y == y1 and i.color != self.color:
						continue
					if i.x in wayx and i.y in wayy:
						if i.x == self.x and i.y == self.y:
							continue
						return False
			return self.x == x1 or self.y == y1 or fabs(self.x-x1) == fabs(self.y-y1)
		
		########################## KNIGHT DETECT ##########################
		if self.typ == "knight":
			return (fabs(self.x - x1)==2 and fabs(self.y - y1) ==1) or (fabs(self.x - x1)==1 and fabs(self.y - y1) ==2)
			
		########################## KING DETECT ##########################
		if self.typ == "king":
			return fabs(self.x - x1) <=1 and fabs(self.y - y1) <=1
		
	def here(self,x,y):
		return (self.x*80-80 < x < self.x*80 and self.y*80-80 < y < self.y*80)*self.alive
		
	def openBlocks(self):
		for i in range(9):
			for j in range(9):
				try:
					if self.detectMove(i,j):
						t = True
						z = False
						for u in self.all:
							if u.x == i and u.y == j and u.color == self.color:
								t=False
							if u.x == i and u.y == j and u.color != self.color:
								t=True
						if t:
							yield (i,j,z)
				except:
					pass
	def moveTo(self,x1,y1):
		if not self.detectMove(x1,y1):
			return 0
		if self.firstMove:
			self.firstMove = False
		for i in self.all:
			if i.here(x1*80-35*2,y1*80-35*2):
				#print(i.color+"_"+i.typ,x1*80,y1*80)
				if i.color is not self.color:
					i.alive = False
					i.selected = False
					i.x = -20
					i.y = -20
				else:
					x1 = self.x 
					y1 = self.y
		self.x = x1
		self.y = y1
		self.selected = False