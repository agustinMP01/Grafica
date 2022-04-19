from cmath import sqrt
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
        flappy.transform =tr.scale(0.125,0.125,0)
        flappy.childs += [gpu_flappy]


        transform_flappy = sg.SceneGraphNode("flappyTR")
        transform_flappy.childs += [flappy]

        self.model = transform_flappy
        self.pos_y = 0
        self.alive = True
        self.vel_y= 0

    def move_up(self):
        #Otorga velocidad vertical a flappy para poder volar
        self.vel_y = 1

    def draw(self,pipeline):
        
        #Inicio Flappy en x=-0.25. En y actualizo para que caiga segun dt 
        self.model.transform = tr.translate(-0.25,self.pos_y,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform") 


    def update(self, dt):

        #Gravedad y velocidad terminal que afectan a flappy
        grav = -2
        terminal_vel = 2

        #"Choque" entre flappy y el piso
        while self.pos_y < -0.49:
            self.pos_y = -0.49

        while self.pos_y > 0.99:
            self.pos_y = 0.99

        #Caida libre en cada update
        self.pos_y += self.vel_y*dt

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
