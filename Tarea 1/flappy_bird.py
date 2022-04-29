import glfw
import sys
from OpenGL.GL import *

import grafica.easy_shaders as es

from modelo import *
from controlador import Controller


if __name__=='__main__':
    if not glfw.init():
        sys.exit()

    #Ventana
    width, height = 640, 960
    window = glfw.create_window(width,height,'Mario Waton: Está waton',None,None)      
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)    

    #Controlador
    controller = Controller()
    glfw.set_key_callback(window,controller.on_key)

    #Pipeline MAIN
    pipeline = es.SimpleTextureTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    glClearColor(0,0.8,1,1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #Modelos
    flappy = Flappy(pipeline)
    floor = Floor(pipeline)
    pipes = Pipe(pipeline)
    gen = PipeGenerator()
    bground = Background(pipeline)
    score = Score(pipeline)
    menus = Menus(pipeline)

    #Seteamos la cantidad de puntos para ganar
    score.goal = int(sys.argv[1])

    #Modelo-Controlador
    controller.set_flappy(flappy)
    controller.set_gen(gen)
    controller.set_menu(menus)

    #Ciclo While
    t0 = glfw.get_time()
    suma_dt = 0
    counter = 2


    while not glfw.window_should_close(window):
        ti = glfw.get_time()
        dt = ti-t0
        t0 = ti

        suma_dt += dt

        #Atrapamos eventos
        glfw.poll_events()

        #Limpiamos pantalla
        glClear(GL_COLOR_BUFFER_BIT)
   

        #"CONTADOR" cada un tiempo determinado crea una pipe y un floor
        if suma_dt >= 1:
            gen.create_pipe(pipeline)
            suma_dt=0
            counter +=1
        elif counter == 2:
            gen.create_floor(pipeline)
            counter = 0

        #Updates    
        gen.update(dt)
        flappy.update(dt)
        floor.update(dt)

        if not flappy.hit:
            score.udpate(gen)

        #Logica
        flappy.collide(gen)


        #Draws
        bground.draw(pipeline) 

        if flappy.alive:
            flappy.draw(pipeline)

        gen.draw_pipes(pipeline)
        gen.draw_floor(pipeline)

        if not flappy.alive and flappy.hit:
            menus.draw_lose(pipeline)


        if score.score >= score.goal:
            gen.on = False
            flappy.alive = False
            menus.draw_victory(pipeline)
            
        if not menus.on:
            menus.draw_main(pipeline)

        if flappy.alive:
            score.draw(pipeline)

        glfw.swap_buffers(window)

    #Terminamos app
    glfw.terminate()
    sys.exit()