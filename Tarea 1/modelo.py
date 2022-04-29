
from random import randint, random
from typing import List
from grafica.assets_path import getAssetPath
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
from grafica.gpu_shape import GPUShape
from typing import Optional

import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from OpenGL.GL import *

class Flappy(object):
    
    def __init__(self,pipeline):

        shape = bs.createTextureQuad(1,1)
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        gpuShape.texture = es.textureSimpleSetup(
            getAssetPath("mario.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

        self.model = gpuShape

        self.pos_y = 0.25
        self.pos_x = -0.25
        self.vel_y= 0

        self.alive = False
        self.hit = False

    def move_up(self):
        #Otorga velocidad vertical a flappy para poder volar
        self.vel_y = 1

    def collide(self, pipes: 'PipeGenerator'):

        if not pipes.on:
            return

        for p in pipes.pipes:
            if self.pos_y <= -0.49:

                self.alive = False
                pipes.die()
                self.hit = True

            elif self.pos_y <= p.length_down and p.pos_x -0.5  < self.pos_x  < p.pos_x :

                self.alive = False
                pipes.die()
                self.hit = True

            elif self.pos_y >= p.length_up and p.pos_x-0.5  < self.pos_x < p.pos_x  : 

                self.alive = False
                pipes.die()
                self.hit = True 
        

    def draw(self,pipeline):
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"),1,GL_TRUE,tr.matmul([tr.translate(self.pos_x,self.pos_y,0),
        tr.scale(0.25,0.25,0) ]))
        pipeline.drawCall(self.model)

    def update(self, dt):

        if self.alive:
        #Gravedad y velocidad terminal que afectan a flappy
            grav = -2
            terminal_vel = 2

            if not self.alive:
                self.pos_y = 0.25

            while self.pos_y > 0.99:
                self.pos_y = 0.99

        #Caida libre en cada update
            self.pos_y += self.vel_y*dt

        #Limite para velocidad al caer
            if self.vel_y > -terminal_vel:
                self.vel_y += grav*dt

        else:
            return

class Floor(object):

    def __init__(self,pipeline):
        floor = bs.createTextureQuad(5,1)
        gpuFloor = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuFloor)
        gpuFloor.fillBuffers(floor.vertices, floor.indices, GL_STATIC_DRAW)
        gpuFloor.texture = es.textureSimpleSetup(
            getAssetPath("floor.png"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

        self.model = gpuFloor
        self.pos_x = 2

    def draw(self,pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"),1,GL_TRUE,
            tr.matmul([tr.translate(self.pos_x,-0.8, 0),tr.scale(2, 0.5, 1)]))
        pipeline.drawCall(self.model)

    def update(self,dt):
        self.pos_x -= dt


class Pipe(object):
    def __init__(self,pipeline):

        pipe = bs.createTextureQuad(2,3)
        gpuPipe = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuPipe)
        gpuPipe.fillBuffers(pipe.vertices, pipe.indices, GL_STATIC_DRAW)
        gpuPipe.texture = es.textureSimpleSetup(
            getAssetPath("skewer_down.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)


        self.model = gpuPipe
        self.pos_x = 2
        self.pos_y = 0

        sign = randint(-1,1)
        alpha = 0.15*randint(1,2)

        if random() <=0.66:
            self.pos_y += sign*alpha

            self.length_up = self.pos_y +0.5
            self.length_down = self.pos_y #Limite de la pipe abajo NO TOCAR

        self.length_down = self.pos_y #Limite de la pipe abajo NO TOCAR
        self.length_up = self.pos_y + 0.5

    def draw_down(self,pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(self.pos_x, self.pos_y-0.5, 0),tr.scale(1, 1, 0)]))
        pipeline.drawCall(self.model)  
        
    def draw_up(self,pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(self.pos_x, self.pos_y+1, 0),tr.scale(1, -1, 0)]))
        pipeline.drawCall(self.model)  
            

    def update(self,dt):
        self.pos_x -= dt

class PipeGenerator(object):
    pipes: List["Pipe"]
    floors: List["Floor"]

    def __init__(self):
        self.pipes = []
        self.floors = []
        self.on = False

    def create_pipe(self,pipeline):
        if len(self.pipes) >= 4 or not self.on:
            return

        self.pipes.append(Pipe(pipeline))

    def create_floor(self,pipeline):
        if len(self.floors)>=3 or not self.on:
            return

        self.floors.append(Floor(pipeline))

    def die(self):
        self.on = False


    def draw_pipes(self,pipeline):
        for k in self.pipes:
            k.draw_up(pipeline) 
            k.draw_down(pipeline)


    def draw_floor(self,pipeline):
        for f in self.floors:
            f.draw(pipeline)

    def update(self,dt):

        for k in self.pipes:
            if k.pos_x <= -1.5:
                self.pipes.pop(0)	
            k.update(dt)

        for f in self.floors:
            if f.pos_x <= -2:
                self.floors.pop(0)
            f.update(dt)    

class Background(object):
    def __init__(self,pipeline):

        background = bs.createTextureQuad(1,1)
        gpuBackground = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuBackground)
        gpuBackground.fillBuffers(background.vertices, background.indices, GL_STATIC_DRAW)
        gpuBackground.texture = es.textureSimpleSetup(
            getAssetPath("background2.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        self.model = gpuBackground

    def draw(self,pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.scale(2,2,1))
        pipeline.drawCall(self.model)

class Menus(object):
    def __init__(self,pipeline):

        #Ganar
        victory = bs.createTextureQuad(1,1)
        gpuVictory = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuVictory)
        gpuVictory.fillBuffers(victory.vertices, victory.indices, GL_STATIC_DRAW)
        gpuVictory.texture = es.textureSimpleSetup(
            getAssetPath("you_won.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        self.victory = gpuVictory

        #Perder
        lose = bs.createTextureQuad(1,1)
        gpuLose = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuLose)
        gpuLose.fillBuffers(lose.vertices, lose.indices, GL_STATIC_DRAW)
        gpuLose.texture = es.textureSimpleSetup(
            getAssetPath("game_over.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        self.lose = gpuLose

        #Inicio ''''''
        ''' HAY UN PLACEHOLDER ACA'''
        main = bs.createTextureQuad(1,1)
        gpuMain = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuMain)
        gpuMain.fillBuffers(main.vertices, main.indices, GL_STATIC_DRAW)
        gpuMain.texture = es.textureSimpleSetup(
            getAssetPath("pholder.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        self.main = gpuMain   
        self.on = False

    def draw_victory(self,pipeline):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.scale(1.5,0.5,1))
        pipeline.drawCall(self.victory)
 
    def draw_lose(self,pipeline):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.scale(1,1,1))
        pipeline.drawCall(self.lose)  

    def draw_main(self,pipeline):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.scale(1.5,1,1))
        pipeline.drawCall(self.main)  

    def update(self):
        return          

class Score(object):
    pipe: Optional['Pipe']

    def __init__(self,pipeline):

        score_unit = bs.createTextureQuad(1,1)
        gpuScore_unit = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuScore_unit)
        gpuScore_unit.fillBuffers(score_unit.vertices, score_unit.indices, GL_STATIC_DRAW) 

        self.score_u = gpuScore_unit

        score_ten = bs.createTextureQuad(1,1)
        gpuScore_ten = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuScore_ten)
        gpuScore_ten.fillBuffers(score_ten.vertices, score_ten.indices, GL_STATIC_DRAW)

        self.score_ten = gpuScore_ten

        self.score = 0
        self.goal = 0


    def separate(self, integer):

        integer_list = list(map(int,str(integer)))
        return integer_list

    def set_texture(self,score):
        list = self.separate(score)
        int_to_png = {0:"0.png",1:"1.png",2: "2.png",
                     3:"3.png",4:"4.png",5:"5.png",
                     6:"6.png",7:"7.png",8:"8.png",9:"9.png"}

        if len(list) == 1: #ES UNA UNIDAD
            self.score_u.texture = es.textureSimpleSetup(
                getAssetPath("0.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

            self.score_ten.texture = es.textureSimpleSetup(
                getAssetPath(int_to_png[list[0]]), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        else: #Tiene 2 digitos (Asumo que nadie jugara +100 puntos)
            self.score_u.texture = es.textureSimpleSetup(
                getAssetPath(int_to_png[list[0]]), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

            self.score_ten.texture = es.textureSimpleSetup(
                getAssetPath(int_to_png[list[1]]), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)                    


    def draw(self,pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-0.05,0.8,0),tr.scale(0.1,0.1,1)]))
        pipeline.drawCall(self.score_u)  

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.05,0.8,0),tr.scale(0.1,0.1,1)]))
        pipeline.drawCall(self.score_ten)  


    def udpate(self, pipes: 'PipeGenerator'):

        for p in pipes.pipes:
            eps = 0.0018
            if -0.25-eps<=p.pos_x <= -0.25+eps:
                self.score += 1

        self.set_texture(self.score)       

