import math
import random
import pygame
# import tkinter as tk
# from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start 
        self.dirnx = 1 
        self.dirny = 0
        self.color = color 
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx 
        self.dirny = dirny 
        self.pos = (self.pos[0] + self.dirnx,self.pos[1] + self.dirny)
    
    def draw(self, surface, eyes=False):
        
        dis = self.w // self.rows 
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1, dis-2, dis-2))

        if eyes:
            center = dis//2 
            radius = 3 
            circleMiddle = (i*dis+center-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)

            pygame.draw.circle(surface,"black",circleMiddle,radius)
            pygame.draw.circle(surface,"black",circleMiddle2, radius)



        

class snake(object):

    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # The head of our snake
        self.body.append(self.head) # Adding head to the body list 
        
        # Direction vectors for snake
        self.dirnx = 0 
        self.dirny = 1


        

    def move(self):
    
        

            
        keys = pygame.key.get_pressed()

        for key in keys:

            if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # Loop through every cube in snake body
             
            # Store the cube position on the grid
            # If the cube's current position is where we turned
            # We get the direction we should be turning 
            # We move our cube in that direction
            # Then we have to remove the last body from our queue 
             
            p = c.pos[:] 

            if p in self.turns:
                 
                turn = self.turns[p]

                c.move(turn[0],turn[1])

                if i == len(self.body) -1:

                    self.turns.pop(p)
            
            else:
                 
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx, c.dirny)




    def reset(self, pos):
        pass

    def addCube(self):
        
        tail = self.body[-1]

        dx,dy = tail.dirnx, tail.dirny 

        if dx == 1 and dy == 0:

            self.body.append(cube((tail.pos[0] -1, tail.pos[1])))

        elif dx == -1 and dy == 0: 

            self.body.append(cube((tail.pos[0] +1, tail.pos[1])))

        elif dx == 0 and dy == 1:

            self.body.append(cube((tail.pos[0], tail.pos[1] -1)))

        elif dx == 0 and dy == -1:

            self.body.append(cube((tail.pos[0], tail.pos[1] +1)))


        self.body[-1].dirnx = dx 
        self.body[-1].dirny = dy 



        

    def draw(self, surface):
        
        for i, c in enumerate(self.body):
             
            if i == 0:
                c.draw(surface,True)
            else:
                 c.draw(surface)




def drawGrid(w, rows, surface):
    
    sizeBetween = w // rows 

    x = 0 
    y = 0

    for i in range(rows):

        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface,"white",(x,0),(x,w))
        pygame.draw.line(surface,"white",(0,y),(w,y))



        

def redrawWindow(surface):

    global rows, width, s, snack

    surface.fill("black")
    drawGrid(width,rows,surface)
 
    snack.draw(surface)
    s.draw(surface)
    pygame.display.update()





def randomSnack(rows, item):
    
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def message_box(subject, content):
    pass


def main():
    global width, rows, s, snack

    width = 500
    height = 500
    rows = 20

    window = pygame.display.set_mode((width,height))

    s = snake((255.0,0.0,0.0),(10,10))

    snack = cube(randomSnack(rows, s), color=(0,255,0))


    clock = pygame.time.Clock()

    flag = True 

    while flag:

        pygame.time.delay(50)

        clock.tick(10)

        redrawWindow(window)

        s.move()
        
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))




        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                flag = False





main()