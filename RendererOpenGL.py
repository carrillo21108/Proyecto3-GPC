
import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *
from math import pi,sin,cos

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
modelo.loadTexture("textures/rocket.bmp")

rend.scene.append(modelo)

rend.camPosition = glm.vec3(modelo.translate.xy,0)
rend.target = modelo.translate
rend.camAngle = 0.0
rend.camRadio = abs(modelo.translate.z)

#Musica
pygame.mixer.music.load("music/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

shot_sound = pygame.mixer.Sound("music/shot.wav")
shot_sound.set_volume(0.3)

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
                shot_sound.play()
            elif event.key==pygame.K_2:
                rend.setShaders(vertex_shader,stripes_shader);
                shot_sound.play()
            elif event.key==pygame.K_3:
                rend.setShaders(vertex_shader,pencil_shader);
                shot_sound.play()
            elif event.key==pygame.K_4:
                rend.setShaders(vertex_shader,dot_shader);
                shot_sound.play()
    
    if keys[K_d]:
        if rend.camAngle==360:
            rend.camAngle=0.0
            
        rend.camAngle += 1
        rend.camPosition.x = rend.target.x+rend.camRadio*sin(rend.camAngle*pi/180)
        rend.camPosition.z = rend.target.z+rend.camRadio*cos(rend.camAngle*pi/180)
    elif keys[K_a]:
        if rend.camAngle==-360:
            rend.camAngle=0.0
            
        rend.camAngle -= 1
        rend.camPosition.x = rend.target.x+rend.camRadio*sin(rend.camAngle*pi/180)
        rend.camPosition.z = rend.target.z+rend.camRadio*cos(rend.camAngle*pi/180)
    if keys[K_w]:
        if rend.camPosition.z>-1:
            rend.camPosition.z -= 5 * deltaTime
            rend.camRadio = abs(modelo.translate.z)+rend.camPosition.z
    elif keys[K_s]:
        if rend.camPosition.z<5:
            rend.camPosition.z += 5 * deltaTime
            rend.camRadio = abs(modelo.translate.z)+rend.camPosition.z
        
    if keys[K_g]:
        if rend.camPosition.y<5:
            rend.camPosition.y += 5 * deltaTime
    elif keys[K_e]:
        if rend.camPosition.y>-5:
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