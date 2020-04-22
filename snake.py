from tkinter import Canvas, Tk
from xmlrpc.client import boolean

import numpy as np



def can_play(func):
    def _can_play(self, *args, **kwargs):
        if self.alive:
            pos_before=self.position.copy()
            func(self, *args, **kwargs)
            xy=(self.position-pos_before)*self.RATIO
            self.board.move(self.snake,xy[0],xy[1])
    return _can_play


def check_death(func):
    def _check_death(self, *args, **kwargs):
        func(self, *args, **kwargs)
        x = self.position[0]
        y = self.position[1]
        # Assert snake not out of bound
        if x < 0 or x > self.dim-1 or y < 0 or y > self.dim-1:
            self.alive = False
            # Assert snake is not biting is tail
        for el in self.tail:
            if np.array_equal(self.position, el):
                self.alive = False
    return _check_death

def check_bonus(func):
    def _check_bonus(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if np.array_equal(self.bonus,self.position):
            self.board.delete('bonus')
            self.create_bonus()
            self.extend+=1
            self.score+=1
    return _check_bonus

def check_tail(func):
    def _check_tail(self, *args, **kwargs):
        extend=self.extend>0
        p=self.position.copy()
        func(self, *args, **kwargs)
        self.tail.insert(0,p)
        if not extend:
            self.tail.pop()
        else:
            self.extend-=1
    return _check_tail

class Snake(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Create main board with 15 cells
        self.dim = 15
        self.FRAME_TIME=16
        self.RATIO=20
        #snake time to change is position from one cell in ms (the lower the faster)
        self.game_speed=250
        #Indicate when to update. Update if > game speed
        self.pos_update= 0
        self.board = Canvas(bg='black', width=self.dim*self.RATIO, height=self.dim*self.RATIO)
        self.board.pack()
        self.seed = 1540
        np.random.seed(self.seed)
        self.create_bonus()
        self.create_snake()
        # Check if the tail should extend and how many time
        self.extend=0
        self.score=0
        self.bind('<Any-KeyPress>',self.connecting_head_with_keys)
        self.re_update()

    def create_snake(self):
        self.position = np.random.randint(self.dim, size=2)
        self.tail = []
        self.snake_size = 1
        self.dir = 't'
        self.alive = True
        x1=self.position[0]*self.RATIO
        y1=self.position[1]*self.RATIO
        x2=self.position[0]*self.RATIO+self.RATIO
        y2=self.position[1]*self.RATIO+self.RATIO
        self.snake=self.board.create_oval(x1,y1,x2,y2,fill='red')

    def create_bonus(self):
        self.bonus = np.random.randint(self.dim, size=2)
        x1=self.bonus[0]*self.RATIO
        y1=self.bonus[1]*self.RATIO
        x2=self.bonus[0]*self.RATIO+self.RATIO
        y2=self.bonus[1]*self.RATIO+self.RATIO
        self.apple = self.board.create_rectangle(x1,y1,x2,y2,fill='blue',tag='bonus')

    def re_update(self):
        self.pos_update+=self.FRAME_TIME
        if self.game_speed < self.pos_update:
            self.moving_snake()
            self.tail_disp_update()
            self.pos_update=0
        self.after(self.FRAME_TIME,self.re_update)
    
    def moving_snake(self):
        if self.dir == 't':
            self.mv_up()
        elif self.dir == 'b':
            self.mv_down()
        elif self.dir == 'r':
            self.mv_right()
        elif self.dir == 'l':
            self.mv_left()
    
    def tail_disp_update(self):
        self.board.delete('tail')
        for p in self.tail:
            x1=p[0]*self.RATIO
            y1=p[1]*self.RATIO
            x2=p[0]*self.RATIO+self.RATIO
            y2=p[1]*self.RATIO+self.RATIO
            self.board.create_oval(x1,y1,x2,y2,fill='green',tag='tail')

        
    def connecting_head_with_keys(self, event=None):
        key=event.keysym
        if key=='Left' and self.dir != 'r':
            self.dir='l'
        elif key=='Right' and self.dir != 'l':
            self.dir='r'
        elif key=='Up' and self.dir != 'b':
            self.dir='t'
        elif key=='Down' and self.dir != 't':
            self.dir='b'
        else:
            pass
        return


    @can_play
    @check_death
    @check_bonus
    @check_tail
    def mv_up(self):
        if self.dir != 'b':
            self.position[1] -= 1
            self.dir = 't'
        else:
            self.mv_down()

    @can_play
    @check_death
    @check_bonus
    @check_tail
    def mv_down(self):

        if self.dir != 't':
            self.position[1] += 1
            self.dir = 'b'
        else:
            self.mv_up()

    @can_play
    @check_death
    @check_bonus
    @check_tail
    def mv_left(self):

        if self.dir != 'r':
            self.position[0] -= 1
            self.dir = 'l'
        else:
            self.mv_right()

    @can_play
    @check_death
    @check_bonus
    @check_tail
    def mv_right(self):

        if self.dir != 'l':
            self.position[0] += 1
            self.dir = 'r'
        else:
            self.mv_left()

    @can_play
    def rel_mv_front(self):
        switcher = {
            't': self.mv_up,
            'b': self.mv_down,
            'l': self.mv_left,
            'r': self.mv_right
        }
        switcher[self.dir]()

    @can_play
    def rel_mv_left(self):
        switcher = {
            't': self.mv_left,
            'b': self.mv_right,
            'l': self.mv_down,
            'r': self.mv_up
        }
        switcher[self.dir]()

    @can_play
    def rel_mv_right(self):
        switcher = {
            't': self.mv_right,
            'b': self.mv_left,
            'l': self.mv_up,
            'r': self.mv_down
        }
        switcher[self.dir]()

    # def create_bonus(self):
    #     self.bonus = np.random.randint(self.dim,size=2)
    
    def in_tail(self,x,y) -> boolean:
        for el in self.tail:
            if x == el[0] and y == el[1]:
                return True
        return False

    def display(self):
        to_disp=""
        for y in range(self.dim-1,-1,-1):
            for x in range(self.dim):
                if self.position.tolist() ==[x,y] or self.in_tail(x,y):
                    to_disp+='O'
                elif self.bonus.tolist() == [x,y]:
                    to_disp+='b'
                else:
                    to_disp+=' '
            to_disp+='\n'
        print(to_disp)