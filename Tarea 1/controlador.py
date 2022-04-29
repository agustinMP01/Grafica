import glfw
import sys

from soupsieve import select
from modelo import Flappy
from typing import Optional 
from modelo import Menus
from modelo import PipeGenerator
from modelo import Score
class Controller(object):
    flappy: Optional['Flappy']
    menu: Optional['Menus']
    gen: Optional['PipeGenerator']
    score: Optional['Score']

    def __init__(self):
        self.flappy = None
        self.menu = None
        self.gen = None
        self.lock = False

    def set_flappy(self,f):
        self.flappy = f

    def set_menu(self,m):
        self.menu = m    

    def set_gen(self,g):
        self.gen = g

    def on_key(self,window,key,scancode,action,mods):
        if not (action == glfw.PRESS):
            return
  
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        #Pasar los eventos la modelo
        elif key == glfw.KEY_UP and action == glfw.PRESS:
            self.flappy.move_up()    
            
        elif key == glfw.KEY_ENTER and action == glfw.PRESS and not self.lock:
            self.menu.on = True
            self.gen.on = True
            self.flappy.alive = True
            self.lock = True


