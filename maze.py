"""
Game Programming: Assignment 4
Maze Game


Julian Morris and Jacob Riedel
11/3/14

Code: For part 3 on improving the game section, we decided to implement the
smooth move and smooth falling. We did this by making the player move multiple
steps for every tile it moves, just as you suggested. However, since Python is
slow, it crashes fairly often if the global variable "steps" is set to anything
above 4, where it only starts to get smooth when steps is more than 12, preferably 24.
Also, the steps variable must be such that 24 is a multiple of steps.
ex. 24/steps must be an integer so that the image doesn't get stuck between tiles.
"""


from graphics import *
from threading import Timer
from time import sleep
import random

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20

movementSpeed = .1
#steps = 24                 Use this value to see our smooth implementation. It crashes after about 15 seconds though.
steps = 4
pause = 0.001

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT


MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
}

DIG = {
    'z':(-1,1),
    'x':(1,1)
    }

"""Gets the screen Position."""
def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

"""Gets the scaled index of the screen position."""
def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

"""Gets the index if the board is represented in one dimension."""
def index (x,y):
    return x + (y*LEVEL_WIDTH)

"""Character class that both Players and Baddies inherits from."""
class Character (object):
    def __init__ (self,pic,x,y,window,level,screen):
        (sx,sy) = screen_pos(x,y)
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level
        self._screen = screen
        self.isDead = False
    
    """returns the locations of the character."""
    def same_loc (self,x,y):
        return (self._x == x and self._y == y)

#nothing = 0,bricks = 1,ladder = 2,rope = 3,gold = 4.

    """Movement Logic for the characters."""
    def move (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy
        unStandable = [0,3,4]
        gravity = 0
        i=0

        if self._level[index(self._x,self._y)] != 1:
            if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
                
                if self._level[index(tx,ty)] == 0 and self._level[index(self._x,self._y)] in unStandable and dy == -1:
                    pass
                if self._level[index(tx,ty)] == 3 and self._level[index(self._x,self._y)] ==0 and dy == -1:
                    pass
                
                elif self._level[index(tx,ty)] == 0 and self._level[index(self._x,self._y)]==2 and dy == -1:
                    self._x = tx
                    self._y = ty
                    while i < steps:
                        self._img.move(dx*CELL_SIZE/steps,dy*CELL_SIZE/steps)
                        i += 1
                        sleep(pause)

                
                elif self._level[index(tx,ty)] != 0 and self._level[index(tx,ty)] != 1:
                    self._x = tx
                    self._y = ty
                    while i < steps:
                        self._img.move(dx*CELL_SIZE/steps,dy*CELL_SIZE/steps)
                        i += 1
                        sleep(pause)
                
                
                elif self._level[index(tx,ty)] == 0 and dy==0:
                    if self._level[index(tx,ty)] == 0:
                        while ty+gravity+1 < LEVEL_HEIGHT and self._level[index(tx,ty+gravity)]==0:
                            gravity += 1
                        if self._level[index(tx,ty+gravity)]!=1:
                            self._x = tx
                            self._y = ty+gravity
                            while i < steps:
                                self._img.move(dx*CELL_SIZE/steps,(gravity)*CELL_SIZE/steps)
                                i += 1
                                sleep(pause)
                        else:
                            self._x = tx
                            self._y = ty+gravity-1
                            while i < steps:
                                self._img.move(dx*CELL_SIZE/steps,(gravity-1)*CELL_SIZE/steps)
                                i += 1
                                sleep(pause)
                    
                    else:
                        self._x = tx
                        self._y = ty
                        while i < steps:
                            self._img.move(dx*CELL_SIZE/steps,dy*CELL_SIZE/steps)
                            i += 1
                            sleep(pause)
                
                elif self._level[index(self._x,self._y)] == 3 and self._level[index(tx,ty)] == 0 and dy == 1:
                    while self._level[index(tx,ty+gravity)]==0 and ty+gravity+1 < LEVEL_HEIGHT:
                        gravity += 1
                        
                    if self._level[index(tx,ty+gravity)]!=1:
                        self._x = tx
                        self._y = ty+gravity
                        while i < steps:
                            self._img.move(dx*CELL_SIZE/steps,(gravity+1)*CELL_SIZE/steps)
                            i += 1
                            sleep(pause)

                    else:
                        self._x = tx
                        self._y = ty+gravity-1
                        while i < steps:
                            self._img.move(dx*CELL_SIZE/steps,(gravity)*CELL_SIZE/steps)
                            i += 1
                            sleep(pause)
        else:
            self.isDead = True

                        
    """Tests the movement for the baddies to see whether it can move there."""
    def testMove (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy
        unStandable = [0,3,4]
        gravity = 0

        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] == 0 and self._level[index(self._x,self._y)] in unStandable and dy == -1:
                return False
            elif self._level[index(tx,ty)] == 0 and self._level[index(self._x,self._y)]==2 and dy == -1:
                return True
            elif self._level[index(tx,ty)] != 0 and self._level[index(tx,ty)] != 1:
                return True
            elif self._level[index(tx,ty)] == 0 and dy==0:
                if self._level[index(tx,ty+1)] == 0:
                    while ty+gravity+1 < LEVEL_HEIGHT and self._level[index(tx,ty+gravity)]==0:
                        gravity += 1
                    if self._level[index(tx,ty+gravity)]!=1:
                        return True
                    else:
                        return True
                    return False
                else:
                    return True
                return False
            elif self._level[index(self._x,self._y)] == 3 and self._level[index(tx,ty)] == 0 and dy == 1:
                while self._level[index(tx,ty+gravity)]==0 and ty+gravity+1 < LEVEL_HEIGHT:
                    gravity += 1
                if self._level[index(tx,ty+gravity)]!=1:
                    return True
                else:
                    return True
                return False
            return False
        return False
    
    """Dig method that destroys a brick. Fills up after some time."""            
    def dig (self,x,y):
        tx = self._x + x
        ty = self._y + y
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] == 1 or self._level[index(tx,ty)] == 4:
                hole = Hole(tx,ty,self._window,self._screen,self._level)
                return hole

"""Player character class."""
class Player (Character):
    def __init__ (self,x,y,window,level,screen):
        Character.__init__(self,'android.gif',x,y,window,level,screen)
        self.gold = 0
        self.posOnLadder = 0
        
    def at_exit (self):
        if self._level[index(self._x,self._y)] == 1:
            self.isDead = True
        return (self._y == 0)
    
    def at_ladder (self):
        ladderY = [0,1,2]
        if self._x == 34 and self._y in ladderY and self.posOnLadder!=self._y:
            self.posOnLadder = self._y
            return True
        else:
            return False
            
    
    def hasLost(self):
        if self.isDead:
            return True
            
    def onGold (self, level, img):
        if self._level[index(self._x, self._y)] == 4:
            self.gold += 1
            self.dig(0,0)
            print self.gold
            
            if self.gold >= 2:
                self._level[index(34,0)] = 2
                self._level[index(34,1)] = 2
                self._level[index(34,2)] = 2
                
                """the ladders are drawn after all the golds are collected."""
                for i in img:
                    i.draw(self._window)

"""Enemy class."""
class Baddie (Character):
    def __init__ (self,x,y,window,level,player,screen):
        Character.__init__(self,'red.gif',x,y,window,level,screen)
        self._player = player

    def baddieMove(self):
        if not self.isDead:
            if self._x == self._player._x and self._y == self._player._y:
                self._player.isDead = True
            if self._y > self._player._y and self.testMove(0,-1):
                self.move(0,-1)
                t =Timer(movementSpeed,self.baddieMove)
                t.start()
            elif self._y < self._player._y and self.testMove(0,1):
                self.move(0,1)
                t =Timer(movementSpeed,self.baddieMove)
                t.start()
            else:        
                if self._x > self._player._x and self.testMove(-1,0):
                    self.move(-1,0)
                    t =Timer(movementSpeed,self.baddieMove)
                    t.start()
                elif self._x < self._player._x and self.testMove(1,0):
                    self.move(1,0)
                    t =Timer(movementSpeed,self.baddieMove)
                    t.start()
                else:
                    (x,y) = MOVE[random.choice(MOVE.keys())]
                    self.move(x,y)
                    t =Timer(movementSpeed,self.baddieMove)
                    t.start()
        else:
            self._img.undraw()

"""Hole object used when you dig a hole."""
class Hole (object):
    def __init__(self,x,y,window,screen,level):
        self._x = x
        self._y = y
        self._level = level
        self.screen = screen
        self._window = window
        (self.sx,self.sy) = screen_pos(self._x,self._y)
        self._level[index(x,y)] = 0
        self._img = self.screen[(self.sx,self.sy)].undraw()
    
    def fillHole(self):
        self._level[index(self._x,self._y)] = 1
        self._img = self.screen[(self.sx,self.sy)].draw(self._window)

"""Text displayed when you win."""
def won (window):
    
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU WON!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

"""Text displayed when you lose."""
def lose (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU LOST!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

"""Initializes the level.""" 
def create_level (num):
    #nothing = 0,bricks = 1,ladder = 2,rope = 3,gold = 4.
    screen = [] 
    
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,2]) 
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2]) 
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,2]) 
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1])
    
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1]) 
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1])
    screen.extend([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3])   
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0]) 
    screen.extend([2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1]) 
     
    screen.extend([2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,2,3,3,3,3,3,3,3,2]) 
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2]) 
    screen.extend([2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    
    screen.extend([2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2])
    screen.extend([2,0,1,4,4,1,0,0,1,0,4,4,4,1,0,0,1,2,0,4,4,4,0,1,0,0,2,0,0,1,4,4,4,1,2])
    screen.extend([2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2]) 
    
    screen.extend([2,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2]) 
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1]) 
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) 
    
    return screen

"""
It takes a level and a window (created by graphics.GraphWin)
and draws a representation of the level in the window.
"""
def create_screen (level,window):
    # use this instead of Rectangle below for nicer screen
    brick = 'brick.gif'
    ladder = 'ladder.gif'
    rope = 'rope.gif'
    gold = 'gold.gif'
    elt = {}
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell != 0:
            (sx,sy) = screen_pos_index(index)
            if cell == 1:
                elt[(sx,sy)] = image(sx,sy,brick)
            elif cell==2:
                elt[(sx,sy)] = image(sx,sy,ladder)
            elif cell==3:
                elt[(sx,sy)] = image(sx,sy,rope)
            elif cell==4:
                elt[(sx,sy)] = image(sx,sy,gold)

            elt[(sx,sy)].draw(window)
    return elt


def main ():
    """Draws the game board."""
    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20)   

    rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
    rect.setFill('sienna')
    rect.setOutline('sienna')
    rect.draw(window)
    rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
    rect.setFill('white')
    rect.setOutline('white')
    rect.draw(window)

    level = create_level(1)
    img = []
    
    """Attempt at drawing the ladder so that the player is not hidden behind the ladder."""
    screen = create_screen(level,window)
    level[index(34,0)] = 0
    img.append(screen[screen_pos(34,0)])
    level[index(34,1)] = 0
    img.append(screen[screen_pos(34,1)])
    level[index(34,2)] = 0
    img.append(screen[screen_pos(34,2)])
    
    screen[screen_pos(34,0)].undraw()
    screen[screen_pos(34,1)].undraw()
    screen[screen_pos(34,2)].undraw()
    
    """Creates the characters."""
    p = Player(10,18,window,level,screen)
    baddie1 = Baddie(5,1,window,level,p,screen)
    baddie2 = Baddie(10,1,window,level,p,screen)
    baddie3 = Baddie(15,1,window,level,p,screen)
    
    b1 = Timer(movementSpeed,baddie1.baddieMove)
    b2 = Timer(movementSpeed,baddie2.baddieMove)
    b3 = Timer(movementSpeed,baddie3.baddieMove)
    b1.start()
    b2.start()
    b3.start()
    holes = []
    
    """Game loop."""
    while not p.at_exit():
        key = window.checkKey()
        if p.isDead:
            lose(window)
        p.onGold(level, img)    #Checks to see if the player is standing on gold.
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:           
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
        if key in DIG:
            (x,y) = DIG[key]
            holes.append(p.dig(x,y))
        if holes != []:           # Digging and filling implementation.
            if holes[0] == None:
                del holes[0]
            else:
                hole = holes.pop(0)
                t =Timer(5,hole.fillHole)
                t.start()
        if p.at_ladder() == True:
            p._img.undraw()            
            p._img.draw(window)

            
           
    won(window)

if __name__ == '__main__':
    main()
