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
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_body_quad]

        flappy = sg.SceneGraphNode("flappy")

        flappy.childs += [body]

        transform_flappy = sg.SceneGraphNode("flappyTR")
        transform_flappy.childs += [flappy]

        self.model = transform_flappy
        self.pos = 0
        self.alive = True