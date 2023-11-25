
from turtle import down
import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *
from math import pi,sin,cos

width = 1920
height = 1080

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
skyBoxTextures = ["skybox/px.png","skybox/nx.png","skybox/py.png","skybox/ny.png","skybox/pz.png","skybox/nz.png"]
models = ["models/rocket.obj","models/alien.obj","models/satelite.obj","models/saturn.obj"]
textures = ["textures/rocket.bmp","textures/alien.bmp","textures/satelite.bmp","textures/saturn.bmp"]

rend.createSkybox(skyBoxTextures,skybox_vertex_shader,skybox_fragment_shader)

rend.setShaders(vertex_shader,unlit_shader)

actual_model = 0
modelo = Model(filename=models[actual_model],translate=glm.vec3(0,0,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(1,1,1))
modelo.loadTexture(textures[actual_model])
rend.scene.append(modelo)

rend.camPosition = glm.vec3(modelo.translate.xy,0)
rend.target = modelo.translate
rend.camAngle = 0.0
rend.camRadio = abs(modelo.translate.z)

#Musica y sonidos
pygame.mixer.music.load("music/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

shot_sound = pygame.mixer.Sound("music/shot.wav")
shot_sound.set_volume(0.3)
change_sound = pygame.mixer.Sound("music/change.mp3")
change_sound.set_volume(0.3)

#Valores iniciales
mousePos = (0.0,0.0)
movingXZ = False
movingY = False

#Funciones movimiento de camara
def rightCircularMovement(rend):
    if rend.camAngle==360:
        rend.camAngle=0.0
            
    rend.camAngle += 1
    rend.camPosition.x = rend.target.x+rend.camRadio*sin(rend.camAngle*pi/180)
    rend.camPosition.z = rend.target.z+rend.camRadio*cos(rend.camAngle*pi/180)
    
def leftCircularMovement(rend):
    if rend.camAngle==-360:
        rend.camAngle=0.0
            
    rend.camAngle -= 1
    rend.camPosition.x = rend.target.x+rend.camRadio*sin(rend.camAngle*pi/180)
    rend.camPosition.z = rend.target.z+rend.camRadio*cos(rend.camAngle*pi/180)
    
def zoomIn(rend):
    if rend.camPosition.z>-1:
        rend.camPosition.z -= 5 * deltaTime
        rend.camRadio = abs(modelo.translate.z)+rend.camPosition.z
        
def zoomOut(rend):
    if rend.camPosition.z<5:
        rend.camPosition.z += 5 * deltaTime
        rend.camRadio = abs(modelo.translate.z)+rend.camPosition.z
        
def upVerticalMovement(rend):
    if rend.camPosition.y<5:
        rend.camPosition.y += 5 * deltaTime

def downVerticalMovement(rend):
    if rend.camPosition.y>-5:
        rend.camPosition.y -= 5 * deltaTime

isRunning = True
while isRunning:
    deltaTime = clock.tick(60)/1000
    
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning = False
            
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: #Salir del programa
                isRunning = False
            elif event.key==pygame.K_SPACE: #Barra espaciadora para cambiar de obj
                actual_model+=1
                if actual_model==len(models):
                    actual_model = 0
                
                change_sound.play()
                modelo = Model(filename=models[actual_model],translate=glm.vec3(0,0,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(1,1,1))
                modelo.loadTexture(textures[actual_model])
                rend.scene.pop()
                rend.scene.append(modelo)                
            
            #1...7: Shaders
            elif event.key==pygame.K_1: #Toon shader [1]
                rend.setShaders(vertex_shader,toon_shader);
                shot_sound.play()
            elif event.key==pygame.K_2: #Gourad shader [2]
                rend.setShaders(vertex_shader,gourad_shader);
                shot_sound.play()
            elif event.key==pygame.K_3: #Colors shader [3]
                rend.setShaders(vertex_shader,colors_shader);
                shot_sound.play()
            elif event.key==pygame.K_4: #Stripes shader [4]
                rend.setShaders(vertex_shader,stripes_shader);
                shot_sound.play()
            elif event.key==pygame.K_5: #Pencil Shader [5]
                rend.setShaders(vertex_shader,pencil_shader);
                shot_sound.play()
            elif event.key==pygame.K_6: #Dot Shader [6]
                rend.setShaders(vertex_shader,dot_shader);
                shot_sound.play()
            elif event.key==pygame.K_7: #Fat Vertex Shader [7]
                rend.setShaders(fat_vertex_shader,unlit_shader);
                shot_sound.play()
                
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1:   #Al mantener el click izquierdo, el movimiento XZ es verdadero
                mousePos = event.pos
                movingXZ = True
            elif event.button == 3: #Al mantener el click derecho, el movimiento Y es verdadero
                mousePos = event.pos
                movingY = True
            elif event.button == 4:  # Rueda de desplazamiento hacia arriba, zoomIn
                zoomIn(rend)
            elif event.button == 5:  # Rueda de desplazamiento hacia abajo, zoomOut
                zoomOut(rend)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: #Al soltar el click izquierdo, el movimiento XZ es falso
                movingXZ = False
            if event.button == 3: #Al soltar el click derecho, el movimiento Y es falso
                movingY = False
                
        elif event.type == pygame.MOUSEMOTION:
            if movingXZ:
                if event.pos[0]<mousePos[0]: #De derecha a izquierda
                    rightCircularMovement(rend)
                else:
                    leftCircularMovement(rend)
                mousePos = event.pos
            if movingY:
                if event.pos[1]<mousePos[1]: #De abajo hacia arriba
                    downVerticalMovement(rend)
                else:
                    upVerticalMovement(rend)
                mousePos = event.pos

    if keys[K_d]:   #Movimiento circular a la derecha [d]
        rightCircularMovement(rend)
    elif keys[K_a]: #Movimiento circular a la izquierda [a]
        leftCircularMovement(rend)
        
    if keys[K_w]:   #ZoomIn al objeto [w]
        zoomIn(rend)
    elif keys[K_s]: #ZoomOut al objeto [s]
        zoomOut(rend)
        
    if keys[K_g]:   #Movimiento de camara hacia arriba [g]
        upVerticalMovement(rend)
    elif keys[K_e]: #Movimiento de camara hacia abajo [e]
        downVerticalMovement(rend)

    if keys[K_UP]:  #Aumentar fatness [UP]
        if rend.fatnessFrecuency<4.0:
            rend.fatnessFrecuency+=1*deltaTime
    elif keys[K_DOWN]: #Disminuir fatness [DOWN]
        if rend.fatnessFrecuency>1.0:
            rend.fatnessFrecuency-=1*deltaTime

    rend.elapsedTime += deltaTime
    rend.update()
    rend.render()
    pygame.display.flip()
    
pygame.quit()