
import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
skyBoxTextures = ["skybox/px.png","skybox/nx.png","skybox/py.png","skybox/ny.png","skybox/pz.png","skybox/nz.png"]
models = []
textures = []
rend.createSkybox(skyBoxTextures,skybox_vertex_shader,skybox_fragment_shader)

rend.setShaders(vertex_shader,siren_shader)

modelo = Model(filename="models/toonRocket.obj",translate=glm.vec3(0,0,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(1,1,1))
modelo.loadTexture("textures/toonRocket.bmp")

rend.scene.append(modelo)

rend.target = modelo.translate

isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning = False
            
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                isRunning = False
            elif event.key==pygame.K_SPACE:
                rend.toggleFilledMode()
                
            elif event.key==pygame.K_1:
                rend.setShaders(vertex_shader,siren_shader);
            elif event.key==pygame.K_2:
                rend.setShaders(vertex_shader,stripes_shader);
            elif event.key==pygame.K_3:
                rend.setShaders(vertex_shader,pencil_shader);
            elif event.key==pygame.K_4:
                rend.setShaders(vertex_shader,dot_shader);
    
    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime #5 unidades por segundo
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime
        
    if keys[K_w]:
        rend.camPosition.z -= 5 * deltaTime
    elif keys[K_s]:
        rend.camPosition.z += 5 * deltaTime
        
    if keys[K_g]:
        rend.camPosition.y += 5 * deltaTime
    elif keys[K_e]:
        rend.camPosition.y -= 5 * deltaTime

    if keys[K_UP]:
        if rend.fatness<1.0:
            rend.fatness+=1*deltaTime
    elif keys[K_DOWN]:
        if rend.fatness>0.0:
            rend.fatness-=1*deltaTime

    rend.elapsedTime += deltaTime
    rend.update()
    rend.render()
    pygame.display.flip()
    
pygame.quit()