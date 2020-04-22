
from tkinter import Canvas, Tk

import numpy as np

from snake_logic import SnakeLogic


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
        self.frame_update= 0
        self.board = Canvas(bg='black', width=self.dim*self.RATIO, height=self.dim*self.RATIO)
        self.board.pack()
        self.snake_control=SnakeLogic(self.dim)
        self.create_snake()
        self.create_bonus()
        self.bind('<Any-KeyPress>',self.connecting_head_with_keys)
        self.re_update()

    def create_snake(self):
        position = self.snake_control.position
        x1=position[0]*self.RATIO
        y1=position[1]*self.RATIO
        x2=position[0]*self.RATIO+self.RATIO
        y2=position[1]*self.RATIO+self.RATIO
        self.snake=self.board.create_oval(x1,y1,x2,y2,fill='red')

    def create_bonus(self):
        bonus=self.snake_control.bonus
        x1=bonus[0]*self.RATIO
        y1=bonus[1]*self.RATIO
        x2=bonus[0]*self.RATIO+self.RATIO
        y2=bonus[1]*self.RATIO+self.RATIO
        self.apple = self.board.create_rectangle(x1,y1,x2,y2,fill='blue',tag='bonus')

    def re_update(self):
        # Update frame counting
        self.frame_update+=self.FRAME_TIME
        # If frame counting is enoug for one step 
        if self.game_speed < self.frame_update:
            pos_bef=self.snake_control.position.copy()
            #Snake movement
            self.snake_control.moving_snake()
            xy=(self.snake_control.position-pos_bef)*self.RATIO
            #Update snake position on board
            self.board.move(self.snake,xy[0],xy[1])
            self.tail_disp_update()
            self.bonus_disp_update()
            # Reset frame update
            self.frame_update=0
        self.after(self.FRAME_TIME,self.re_update)
    
    def tail_disp_update(self):
        self.board.delete('tail')
        for p in self.snake_control.tail:
            x1=p[0]*self.RATIO
            y1=p[1]*self.RATIO
            x2=p[0]*self.RATIO+self.RATIO
            y2=p[1]*self.RATIO+self.RATIO
            self.board.create_oval(x1,y1,x2,y2,fill='green',tag='tail')

    def bonus_disp_update(self):
        self.board.delete('bonus')
        p=self.snake_control.bonus
        x1=p[0]*self.RATIO
        y1=p[1]*self.RATIO
        x2=p[0]*self.RATIO+self.RATIO
        y2=p[1]*self.RATIO+self.RATIO
        self.board.create_rectangle(x1,y1,x2,y2,fill='blue',tag='bonus')

        
    def connecting_head_with_keys(self, event=None):
        key=event.keysym
        if key=='Left':
            self.snake_control.change_dir('l')
        elif key=='Right':
            self.snake_control.change_dir('r')
        elif key=='Up':
            self.snake_control.change_dir('t')
        elif key=='Down':
            self.snake_control.change_dir('b')
        else:
            pass
        
        return
