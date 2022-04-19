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

        gpu_flappy = create_gpu(bs.createColorQuad(0.8,0.8,0.8),pipeline)

        flappy = sg.SceneGraphNode("flappy")
        flappy.transform =tr.scale(0.125,0.125,0)
        flappy.childs += [gpu_flappy]


        transform_flappy = sg.SceneGraphNode("flappyTR")
        transform_flappy.childs += [flappy]

        self.model = transform_flappy
        self.pos_y = 0
        self.alive = True


    def move_up(self):
        self.pos_y += 0.5

    def draw(self,pipeline):

        #Inicio en x=-0.25. En y actualizo para que caiga segun dt 
        self.model.transform = tr.translate(-0.25,self.pos_y,0)
        sg.drawSceneGraphNode(self.model,pipeline,"transform") 

    def update(self, dt):
        self.pos_y -= dt
        
     
