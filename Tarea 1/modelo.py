
from random import randint, random
from typing import List
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es


from OpenGL.GL import glClearColor, GL_STATIC_DRAW

def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu

class Flappy(object):
    
    def __init__(self,pipeline):

        gpu_flappy = create_gpu(bs.createColorQuad(1,1,0.2),pipeline)

        flappy = sg.SceneGraphNode("flappy")
        flappy.transform =tr.scale(0.125,0.083,0)
        flappy.childs += [gpu_flappy]


        transform_flappy = sg.SceneGraphNode("flappyTR")
        transform_flappy.childs += [flappy]

        self.model = transform_flappy
        self.pos_y = 0.25
        self.pos_x = -0.25
        self.vel_y= 0
        self.alive = True

    def move_up(self):
        #Otorga velocidad vertical a flappy para poder volar
        self.vel_y = 1

    def collide(self, pipes: 'PipeGenerator'):
        if not pipes.on:
            return

        for p in pipes.pipes:
            if self.pos_y < -0.49:

                self.pos_y = 0.25
                self.alive = False

            if (not (p.length_down < self.pos_y < p.length_up)) and self.pos_x == p.pos_x:

                self.pos_y = 0.25
                print('perdiste')

    def draw(self,pipeline):
        
        #Inicio Flappy en x = pos_x, y = pos_y
        self.model.transform = tr.translate(self.pos_x,self.pos_y,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform") 


    def update(self, dt):

        #Gravedad y velocidad terminal que afectan a flappy
        grav = -2
        terminal_vel = 2

        while self.pos_y > 0.99:
            self.pos_y = 0.99

        #Caida libre en cada update
        #self.pos_y += self.vel_y*dt

        #Limite para velocidad al caer
        if self.vel_y > -terminal_vel:
            self.vel_y += grav*dt



class Floor(object):

    def __init__(self,pipeline):
        gpu_floor = create_gpu(bs.createColorQuad(0.67,1,0.18),pipeline)

        floor = sg.SceneGraphNode("floor")
        floor.transform =tr.scale(2,1,0)
        floor.childs += [gpu_floor]

        transform_floor = sg.SceneGraphNode("floorTR")
        transform_floor.childs += [floor]

        self.model=transform_floor

    def draw(self,pipeline):
        self.model.transform = tr.translate(0,-1,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform")

    def update(self):
        return

class Pipe(object):
    def __init__(self,pipeline):
        gpu_pipe = create_gpu(bs.createColorQuad(0.8,0.8,0.8),pipeline)

        #Tuberia
        pipe = sg.SceneGraphNode("pipe")
        pipe.transform = tr.scale(0.25,2,0) #x = 0.25, o sea, 2 flappys delta_y = 0.498 o sea 6 flappys
        pipe.childs += [gpu_pipe]

        #Tuberia arriba
        pipe_up = sg.SceneGraphNode("pipe up")
        pipe_up.transform = tr.translate(0,1.25,0)
        pipe_up.childs += [pipe]

        #Tuberia abajo
        pipe_down = sg.SceneGraphNode("pipe down")
        pipe_down.transform = tr.translate(0,-1.25,0)
        pipe_down.childs += [pipe]

        #Ensamble de tuberias
        pipes = sg.SceneGraphNode("pipes")
        pipes.transform = tr.translate(0,0.25,0)
        pipes.childs += [pipe_up,pipe_down] 

        transform_pipes = sg.SceneGraphNode("pipesTR")
        transform_pipes.childs += [pipes]

        self.model = transform_pipes
        self.pos_x = 1.5
        self.pos_y = 0

        if random() <=0.66:
            sign = randint(-1,1)
            alpha = 0.15*randint(1,2)
            self.pos_y += sign*alpha

        self.length_up = self.pos_y 
        self.length_down = self.pos_y 

    def draw(self,pipeline):

        self.model.transform = tr.translate(self.pos_x,self.pos_y,0)

        sg.drawSceneGraphNode(self.model, pipeline, "transform")


    def update(self,dt):
        self.pos_x -= dt

class PipeGenerator(object):
    pipes: List["Pipe"]

    def __init__(self):
        self.pipes = []
        self.on = True

    def create_pipe(self,pipeline):
        if len(self.pipes) >= 3 or not self.on:
            return

        self.pipes.append(Pipe(pipeline))

    def draw(self,pipeline):
        for k in self.pipes:
            k.draw(pipeline)

    def update(self,dt):

        for k in self.pipes:
            if k.pos_x < -1:
                self.pipes.pop(0)	
            k.update(dt)

