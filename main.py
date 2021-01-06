import tkinter as tk
import numpy as np
import os
from PIL import Image, ImageTk
from Piece import Piece

root = tk.Tk()
root.minsize(640,640)
root.maxsize(640,640)
root.configure(background='black')

grid = np.zeros((8,8,3),dtype="U25")
yatay = "ABCDEFGH"
dikey = "12345678"
col = "gray black "*4
col = col.split(" ")[:8]
"""
siyah = {}
beyaz = {}

for i in os.listdir("imgs"):
	z = ImageTk.PhotoImage(Image.open("imgs\\"+i).resize((64,64)))
	if i[0] == "w":
		beyaz.update({i.split("_")[1].split(".")[0] : z})
	if i[0] == "b":
		siyah.update({i.split("_")[1].split(".")[0] : z})
print(beyaz)
"""
for i in range(len(grid)):
	for j in range(len(grid[i])):
		grid[j][i] = np.array([yatay[j],dikey[i],str(i*80)+str(" , ")+str(j*80)])

can = tk.Canvas(root,width=640,height=640)
can.pack(side = tk.LEFT)
allpieces = []

bpawns = [Piece(i+1,2,"pawn","b") for i in range(8)]
wpawns = [Piece(i+1,7,"pawn","w") for i in range(8)]
brooks = [Piece(1,1,"rook","b"),Piece(8,1,"rook","b")]
wrooks = [Piece(1,8,"rook","w"),Piece(8,8,"rook","w")]
bknights = [Piece(2,1,"knight","b"),Piece(7,1,"knight","b")]
wknights = [Piece(2,8,"knight","w"),Piece(7,8,"knight","w")]
bbishops = [Piece(3,1,"bishop","b"),Piece(6,1,"bishop","b")]
wbishops = [Piece(3,8,"bishop","w"),Piece(6,8,"bishop","w")]
bqueen = [Piece(4,1,"queen","b")]
wqueen = [Piece(4,8,"queen","w")]
bking = [Piece(5,1,"king","b")]
wking = [Piece(5,8,"king","w")]

for i in [bpawns,wpawns,brooks,wrooks,bknights,wknights,wbishops,bbishops,bqueen,wqueen,bking,wking]:
	for u in i:
		allpieces.append(u)

for i in allpieces:
	i.all = allpieces


def click(m):
	for i in allpieces:
		i.click(m)
	print(yatay[int(m.x//80)]+str(8-int(m.y//80)))

def loop():
	selectedPiece = False
	for i in allpieces:
		if not selectedPiece:
			if i.selected:
				selectedPiece = True
		else:
			i.selected = False
	root.after(100,loop)

def draw():
	can.delete("all")

	for i in range(8):
		for j in range(8):
			can.create_rectangle(i*80, j*80, i*80+80, j*80+80,fill=col[j])
			#can.create_image((i+1)*80 -35*2,(j+1)*80 -35*2, anchor=tk.NW, image=beyaz["rook"])
		col.append(col.pop(0))
	for i in allpieces:
		i.draw(can)
		
	#for u in allpieces:
	#	if u.selected:
	#		for i in u.openBlocks():
	#			can.create_oval(i[0]*80-40*2, i[1]*80-40*2, i[0]*80, i[1]*80, outline="#00FF00", width=4)
    #can.create_image((5+1)*80 -35*2,(5+1)*80 -35*2, anchor=tk.NW, image=beyaz["rook"])
	root.after(300,draw)

root.bind("<Button-1>",click)
loop()
draw()
root.mainloop()