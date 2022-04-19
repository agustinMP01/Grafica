import glfw
import sys
from modelo import Flappy
from typing import Optional 

class Controller(object):
    flappy: Optional['Flappy']

    def __init__(self):
        self.flappy = None

    def set_flappy(self,f):
        self.flappy = f


    def on_key(self,window,key,scancode,action,mods):
        if not (action == glfw.PRESS):
            return
        if key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit()

        #Pasar los eventos la modelo
        elif key == glfw.KEY_UP and action == glfw.PRESS:
            self.flappy.move_up()    


