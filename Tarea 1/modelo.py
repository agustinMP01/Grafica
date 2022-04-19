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

        gpu_body_quad = create_gpu(bs.createColorQuad(0.8,0.8,0.8),pipeline)

        body = sg.SceneGraphNode("body")
        body.transform = tr.scale(0.125,0.125,1)
        body.childs += [gpu_body_quad]

        flappy = sg.SceneGraphNode("flappy")

        flappy.childs += [body]

        transform_flappy = sg.SceneGraphNode("flappyTR")
        transform_flappy.childs += [flappy]

        self.model = transform_flappy
        self.pos = 0
        self.alive = True

    def move_up(self):
        self.pos = 1

    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model,pipeline,"transform") 

    def update(self, dt):
        if self.pos == 1:
            self.model.transform = tr.translate(0,0.5,0)
        else:    
            self.model.transform = tr.translate(0,-0.1,0)
     
