import pygame
import time
from button import button
from aStar import main
BLUE=[106,159,181]
RED=[255,0,0]
c=(230, 230, 255)
ROW=25
COL=60

def displayMessage(msg,window):
	Setdst=button(BLUE,0,501,1200,100,msg)
	Setdst.draw(window)
	pygame.display.update()
def changeColor(newsrc,src,color):
	if not src:
		src=newsrc
		pygame.draw.rect(window,color,(src[0]*20+2,src[1]*20+2,18,18))
		pygame.display.update()
		return
	pygame.draw.rect(window,(255,255,255),(src[0]*20+2,src[1]*20+2,18,18))
	src=newsrc
	pygame.draw.rect(window,color,(src[0]*20+2,src[1]*20+2,18,18))
	pygame.display.update()
def createHurdles(h,grid,ar):
	if ar==1:
		pygame.draw.rect(window,(0,0,0),(h[0]*20+2,h[1]*20+2,18,18))
		grid[h[1]][h[0]]=0
		pygame.display.update()
	else:
		pygame.draw.rect(window,(255,255,255),(h[0]*20+2,h[1]*20+2,18,18))
		grid[h[1]][h[0]]=1
		pygame.display.update()
pygame.init()
window = pygame.display.set_mode((1200,600))
pygame.display.set_caption("A* Visualization")

window.fill((255,255,255))
pygame.display.update()
pygame.display.flip()
def index():
	window.fill((255,255,255))
	displayMessage("select a cell for start.... press F after selection",window)
	for x in range(0,501,20):
		pygame.draw.line(window,c,(0,x),(1200,x),2)
		pygame.display.update()
	for y in range(0,1201,20):
		pygame.draw.line(window,c,(y,0),(y,500),2)
		pygame.display.update()
	dst=None
	src=None
	run=True
	while run:
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
				follow=True
				while follow:
					pos=pygame.mouse.get_pos()
					if pos[0]>=0 and pos[0]<COL*20 and pos[1]>=0 and pos[1]<ROW*20:
						changeColor((int(pos[0]/20),int(pos[1]/20)),src,BLUE)
						src=(int(pos[0]/20),int(pos[1]/20))
					else:
						break
					for event in pygame.event.get():
						if event.type==pygame.MOUSEBUTTONUP and event.button==1:
							follow=False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f and src!=None:
					displayMessage(f"start selected row:{src[1]+1} ,col:{src[0]+1}",window)
					time.sleep(0.5)
					run=False
			if event.type==pygame.QUIT:
				pygame.quit()
	run=True
	displayMessage("select a cell for destination.... press F after selection",window)
	while run:
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
				follow=True
				while follow:
					pos=pygame.mouse.get_pos()
					point=(int(pos[0]/20),int(pos[1]/20))
					if pos[0]>=0 and pos[0]<COL*20 and pos[1]>=0 and pos[1]<ROW*20 and point!=src:
						changeColor(point,dst,RED)
						dst=point
					else:
						break
					for event in pygame.event.get():
						if event.type==pygame.MOUSEBUTTONUP and event.button==1:
							follow=False

			if event.type == pygame.KEYDOWN and dst!=None:
				if event.key == pygame.K_f:
					displayMessage(f"destination selected row:{dst[1]+1} ,col:{dst[0]+1}",window)
					time.sleep(0.5)
					run=False
			if event.type==pygame.QUIT:
				pygame.quit()
	run=True
	displayMessage("using left and right click to add/remove walls and press F at end",window)
	grid=[[1 for x in range(COL)] for y in range(ROW)]
	while run:
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN and event.button%2==1:
				k=event.button
				follow=True
				while follow:
					pos=pygame.mouse.get_pos()
					if pos[0]>=0 and pos[0]<COL*20 and pos[1]>=0 and pos[1]<ROW*20:
						h=(int(pos[0]/20),int(pos[1]/20))
						if h!=src and h!=dst:
							createHurdles(h,grid,k)
					else:
						break
					for event in pygame.event.get():
						if event.type==pygame.MOUSEBUTTONUP and event.button%2==1:
							follow=False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					displayMessage("Walls created",window)
					time.sleep(0.5)
					run=False
			if event.type==pygame.QUIT:
				pygame.quit()
	try:
		main(grid,(src[1],src[0]),(dst[1],dst[0]),window)
	except:
		pass
	else:
		displayMessage("press R to restart",window)
		run=True
		while run:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					run=False
				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_r:
						displayMessage("restarting...",window)
						try:
							index()
						except:
							pass
		pygame.quit()

if __name__=="__main__":
	try:
		index()
	except:
		pass