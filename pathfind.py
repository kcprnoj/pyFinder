import pygame

pygame.init()
screenWidth = 365
screenHeight = 365
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Pathfinder')
rect = pygame.Rect((0, 0, 50, 50))
rect.center = screen.get_rect().center

def checkWhere(mouseX, mouseY):
    retval = [-1,-1]
    for i in range(17):
        x=15+20*i
        x_size=15
        y_size=15
        if (mouseX >= x and mouseX <= x+x_size):
            retval[0] = i
        for j in range(17):
            y=15+20*j
            if (mouseY >= y and mouseY <= y+y_size):
                retval[1] = j
    return retval

def drawNew(inval, R, G, B):
    if inval[0] != -1 and inval[1] != -1:
        x=15+20*inval[0]
        y=15+20*inval[1]
        x_size=15
        y_size=15
        pygame.draw.polygon(screen,(R, G, B), ([x,y],[x,y+y_size],[x+x_size,y+y_size], [x+x_size,y]),0)    
        pygame.display.update()

class Coordinates:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val

class Map:
    map = [[-3 for i in range(17)] for j in range(17)]
    start = [0,0]
    dest = [0,0]
    def __init__(self, start, dest):
        for i in range(17):
            self.map[0][i]=-1
        for i in range(17):
            self.map[i][0]=-1
        for i in range(17):
            self.map[16][i]=-1
        for i in range(17):
            self.map[i][16]=-1
        
        self.start=start
        self.dest=dest
        self.map[start[0]][start[1]]=-2
        self.map[dest[0]][dest[1]]=0

        drawNew(dest, 200, 100, 100)
        drawNew(start, 200, 100, 100)

    def printMap(self):
        screen.fill((0,0,200))

        for i in range(17):
            for j in range(17):
                cords=[i,j]
                if(self.map[i][j] == -1):
                    drawNew(cords, 0, 0, 0)
                elif(self.map[i][j] == -2 or self.map[i][j] == 0):
                    drawNew(cords, 200, 100, 100)
                elif(self.map[i][j] == -3):
                    drawNew(cords, 255, 255, 255)
                else:
                    if(30+5*self.map[i][j] <= 255):
                        drawNew(cords, 0, 30+5*self.map[i][j], 0)
                    else:
                        drawNew(cords, 0, 255, 0)
    
    def findrout(self, x, y):
        path = []
        list = []
        list.append(Coordinates(x,y,self.map[x][y]))
        while self.map[x][y] != 0:
            list = []
            if(self.map[x+1][y]>=0):
                list.append(Coordinates(x+1,y,self.map[x+1][y]))
            if(self.map[x][y+1]>=0):
                list.append(Coordinates(x,y+1,self.map[x][y+1]))
            if(self.map[x-1][y]>=0):
                list.append(Coordinates(x-1,y,self.map[x-1][y]))
            if(self.map[x][y-1]>=0):
                list.append(Coordinates(x,y-1,self.map[x][y-1]))

            min=Coordinates(-1,-1,99999)
        
            for i in range(len(list)):
                if(self.map[list[i].x][list[i].y]<min.val and self.map[list[i].x][list[i].y]>=0):
                    min=list[i]

            if(min.val == 0):
                break;

            path.append(min)
            x=min.x
            y=min.y
            cords=[x,y]
            drawNew(cords, 255, 0, 0)            
    
    def sampleAlgorithm(self, cordsX, cordsY):
        list = []
        list.append(Coordinates(cordsX,cordsY,self.map[cordsX][cordsY]))
        i=0
        while True:
            if(i == len(list)):
                print('There is no possible route')
                self.printMap()
                return 0
            if(self.map[list[i].x+1][list[i].y]!=-1 and (self.map[list[i].x+1][list[i].y]>list[i].val+1 or self.map[list[i].x+1][list[i].y] == -3 or self.map[list[i].x+1][list[i].y] == -2)):
                list.append(Coordinates(list[i].x+1,list[i].y,list[i].val+1))
            if(self.map[list[i].x][list[i].y+1]!=-1 and (self.map[list[i].x][list[i].y+1]>list[i].val+1 or self.map[list[i].x][list[i].y+1] == -3 or self.map[list[i].x][list[i].y+1] == -2)):
                list.append(Coordinates(list[i].x,list[i].y+1,list[i].val+1))
            if(self.map[list[i].x-1][list[i].y]!=-1 and (self.map[list[i].x-1][list[i].y]>list[i].val+1 or self.map[list[i].x-1][list[i].y] == -3 or self.map[list[i].x-1][list[i].y] == -2)):
                list.append(Coordinates(list[i].x-1,list[i].y,list[i].val+1))
            if(self.map[list[i].x][list[i].y-1]!=-1 and (self.map[list[i].x][list[i].y-1]>list[i].val+1 or self.map[list[i].x][list[i].y-1] == -3 or self.map[list[i].x][list[i].y-1] == -2)):
                list.append(Coordinates(list[i].x,list[i].y-1,list[i].val+1))

            if(self.map[list[i].x][list[i].y] == -2):
                self.printMap()
                return self.findrout(list[i].x, list[i].y)
            else:
                self.map[list[i].x][list[i].y] = list[i].val
                i+=1

    def changeVal(self, x, y, val):
        self.map[x][y] = val
    def reset(self):
        for i in range(17):
            for j in range(17):
                self.map[i][j] = -3
        for i in range(17):
            self.map[0][i]=-1
        for i in range(17):
            self.map[i][0]=-1
        for i in range(17):
            self.map[16][i]=-1
        for i in range(17):
            self.map[i][16]=-1
        self.map[self.start[0]][self.start[1]]=-2
        self.map[self.dest[0]][self.dest[1]]=0
        map.printMap()

running=True
flag=0
map = Map([1,3],[13,12])
map.printMap()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if flag == -1:
                    map.reset()
                    flag=0
                else:
                    flag=1

    if(pygame.mouse.get_pressed()[0] == 1):
        cords = checkWhere(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        if(map.map[cords[0]][cords[1]] != -2 and map.map[cords[0]][cords[1]] != 0):
            map.changeVal(cords[0],cords[1], -1)
            drawNew(cords, 0, 0, 0)
    if(flag == 1):
        map.sampleAlgorithm(13,12)
        flag=-1