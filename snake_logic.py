from builtins import bool
from tkinter import Canvas, Tk

import numpy as np


def can_play(func):
    def _can_play(self, *args, **kwargs):
        if self.alive:
            func(self, *args, **kwargs)
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

class SnakeLogic():

    def __init__(self, dim):
        # Create main board with 15 cells
        self.dim = dim
        self.seed = 1540
        np.random.seed(self.seed)
        self.create_bonus()
        self.create_snake()
        # Check if the tail should extend and how many time
        self.extend=0
        self.score=0

    def create_snake(self):
        self.position = np.random.randint(self.dim, size=2)
        self.tail = []
        self.snake_size = 1
        self.dir = 't'
        self.alive = True

    def create_bonus(self):
        self.bonus = np.random.randint(self.dim, size=2)

    def change_dir(self,dir:str):
        if (
            (dir == 't' and self.dir!='b') or
            (dir == 'b' and self.dir!='t') or
            (dir == 'l' and self.dir!='r') or
            (dir == 'r' and self.dir!='l') 
            ):
            self.dir=dir
    
    def moving_snake(self):
        if self.dir == 't':
            self.mv_up()
        elif self.dir == 'b':
            self.mv_down()
        elif self.dir == 'r':
            self.mv_right()
        elif self.dir == 'l':
            self.mv_left()

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
    #     self.bonus = np.random.randint(self.dim,size=2)
    
    def in_tail(self,x:int,y:int) -> bool:
        for el in self.tail:
            if x == el[0] and y == el[1]:
                return True
        return False
