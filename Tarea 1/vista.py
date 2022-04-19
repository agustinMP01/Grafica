import glfw
import sys
from OpenGL.GL import *

import grafica.easy_shaders as es

if __name__=='__main__':
    if not glfw.init():
        sys.exit()


    #Ventana
    width, height = 640, 960
    window = glfw.create_window(width,height,'Falppy Berd',None,None)      
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)    

    #Controlador

    #Pipeline
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    glClearColor(0,0.8,1,1)
    glPolygonMode(GL_FRONT,GL_FILL)

    #Modelos

    #Modelo-Controlador

    #Ciclo While

t0 = glfw.get_time()
while not glfw.window_should_close(window):

    ti = glfw.get_time()
    dt = ti - t0
    t0 = ti