import heapq
import math
import pygame
from button import button
BLUE=[106,159,181]
class point(object):
    """docstring for point"""
    def __init__(self,parent_i,parent_j, fcost=-1,gcost=-1):
        super(point, self).__init__()
        self.parent_i=parent_i
        self.parent_j=parent_j
        self.fcost=fcost
        self.gcost=gcost
def isValid(tup,grid):
    if tup[0]<ROW and tup[0]>=0 and tup[1]<COL and tup[1]>=0:
        if grid[tup[0]][tup[1]]==1:
            return True
        else:
            return False
    else:
        return False
def displayMessage(msg,window):
    Setdst=button(BLUE,0,501,1200,100,msg)
    Setdst.draw(window)
    pygame.display.update()
def showChoosen(h,color,window,src,dst):
    pygame.draw.rect(window,color,(h[0]*20+2,h[1]*20+2,18,18))
    pygame.display.update()
def hCost(tup,dst):
    return math.sqrt((tup[0]-dst[0])*(tup[0]-dst[0]) + (tup[1]-dst[1])*(tup[1]-dst[1]))
def changePriority(cost,tup,openset,cells,parent,dst):
    totalcost=round(cost+hCost(tup,dst),2)
    if totalcost<cells[tup[0]][tup[1]].fcost or (cells[tup[0]][tup[1]].fcost is -1):
        cells[tup[0]][tup[1]].fcost=totalcost
        cells[tup[0]][tup[1]].parent_i=parent[0]
        cells[tup[0]][tup[1]].parent_j=parent[1]
        cells[tup[0]][tup[1]].gcost=cost
        heapq.heappush(openset,(totalcost,tup))
        #print(f"gcost:{cost} fcost:{totalcost} parent:{parent} point:{tup}")

def traceback(cells,dst,window,src):
    now=(dst[0],dst[1])
    if not(cells[dst[0]][dst[1]].parent_j== -1 and cells[dst[0]][dst[1]].parent_i== -1):
        while not (cells[now[0]][now[1]].parent_j==now[1] and cells[now[0]][now[1]].parent_i==now[0]):
            now=(cells[now[0]][now[1]].parent_i,cells[now[0]][now[1]].parent_j)
            if src!=now and src!=dst:
                showChoosen((now[1],now[0]),(255, 163, 102),window,src,dst)

ROW=25
COL=60
sqrt2=math.sqrt(2)
def main(grid1,src1,dst1,window):
    grid=grid1
    src=src1
    dst=dst1
    displayMessage("simulating....",window)
    if(grid[src[0]][src[1]]==0):
        print("source invalid")
        return 
    if(grid[dst[0]][dst[1]]==0):
        print("destination invalid")
        return
    if(dst==src):
        print(f"destination reached:{src}")
        return
    cells=[[point(-1,-1) for j in range(COL)] for i in range(ROW)]
    cells[src[0]][src[1]].parent_j=src[1]
    cells[src[0]][src[1]].parent_i=src[0]
    cells[src[0]][src[1]].fcost=hCost(src,dst)
    cells[src[0]][src[1]].gcost=0
    openset=[(hCost(src,dst),(src[0],src[1]))]
    heapq.heapify(openset)
    closedSet=[[False for j in range(COL)] for i in range(ROW)]
    while not len(openset)==0:
        dequeued=heapq.heappop(openset)
        pt=dequeued[1]
        gcost=cells[pt[0]][pt[1]].gcost
        if pt[0]==dst[0] and pt[1]==dst[1]:
            traceback(cells,dst,window,src)
            displayMessage("path found",window)
            return
        if closedSet[pt[0]][pt[1]]:
            continue
        x=pt[0]
        y=pt[1]
        for i in [(0,-1),(0,1),(1,1),(1,0),(-1,-1),(-1,0),(1,-1),(-1,1)]:
            x1=x+i[0]
            y1=y+i[1]
            if isValid((x1,y1),grid) and not closedSet[x1][y1]:
                if src!=(x1,y1) and dst!=(x1,y1):
                    showChoosen((y1,x1),(0,255,0),window,src,dst)
                if abs(i[0]+i[1])==1:
                    changePriority(gcost+1,(x1,y1),openset,cells,(x,y),dst)
                else:
                    changePriority(gcost+sqrt2,(x1,y1),openset,cells,(x,y),dst)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                return
        closedSet[pt[0]][pt[1]]=True
        if pt!=src and pt!=dst:
            showChoosen((y,x),(220, 194, 119),window,src,dst)
    displayMessage("path not found",window)

if(__name__=="__main__"):
    main()

        
