from OpenGL.GL import *
import glm
from numpy import array, float32
import pygame
from obj import Obj

class Model(object):
    def __init__(self,filename,translate=glm.vec3(0,0,0),rotation=glm.vec3(0,0,0),scale=glm.vec3(1,1,1)):
        model = Obj(filename)
        
        data = []
        untransformedVerts = []
        textCoords = []
        normals = []
        
        for face in model.faces:
            
            vertCount = len(face)
            v0 = model.vertices[face[0][0]-1]
            v1 = model.vertices[face[1][0]-1]
            v2 = model.vertices[face[2][0]-1]
            if vertCount == 4:
                v3 = model.vertices[face[3][0]-1]
                
            vt0 = model.textcoords[face[0][1]-1]
            vt1 = model.textcoords[face[1][1]-1]
            vt2 = model.textcoords[face[2][1]-1]
            if vertCount == 4:
                vt3 = model.textcoords[face[3][1]-1]

            vn0 = model.normals[face[0][2]-1]
            vn1 = model.normals[face[1][2]-1]
            vn2 = model.normals[face[2][2]-1]
            if vertCount == 4:
                vn3 = model.normals[face[3][2]-1]
                
            untransformedVerts.append(v0)
            untransformedVerts.append(v1)
            untransformedVerts.append(v2)
            if vertCount == 4:
                untransformedVerts.append(v0)
                untransformedVerts.append(v2)
                untransformedVerts.append(v3)
            
            textCoords.append([vt0[0],vt0[1]])
            textCoords.append([vt1[0],vt1[1]])
            textCoords.append([vt2[0],vt2[1]])
            if vertCount==4:
                textCoords.append([vt0[0],vt0[1]])
                textCoords.append([vt2[0],vt2[1]])
                textCoords.append([vt3[0],vt3[1]])

            normals.append(vn0)
            normals.append(vn1)
            normals.append(vn2)
            if vertCount == 4:
                normals.append(vn0)
                normals.append(vn2)
                normals.append(vn3)
        
        for i in range(0,len(untransformedVerts),3):
            for item in untransformedVerts[i]:
                data.append(item)
            for item in textCoords[i]:
                data.append(item)
            for item in normals[i]:
                data.append(item) 
            
            for item in untransformedVerts[i+1]:
                data.append(item)
            for item in textCoords[i+1]:
                data.append(item)
            for item in normals[i+1]:
                data.append(item) 
            
            for item in untransformedVerts[i+2]:
                data.append(item)
            for item in textCoords[i+2]:
                data.append(item)
            for item in normals[i+2]:
                data.append(item) 
        
        self.vertBuffer = array(data,dtype=float32)
        
        #Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        
        #Vertex Array Object
        self.VAO = glGenVertexArrays(1)
        
        self.translate = translate
        self.rotation = rotation
        self.scale = scale

    def loadTexture(self,textureName):
        self.textureSurface = pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface,"RGB",True)
        self.textureBuffer = glGenTextures(1)
        
    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMat = glm.translate(identity,self.translate)
        
        pitch = glm.rotate(identity,glm.radians(self.rotation.x),glm.vec3(1,0,0))
        yaw = glm.rotate(identity,glm.radians(self.rotation.y),glm.vec3(0,1,0))
        roll = glm.rotate(identity,glm.radians(self.rotation.z),glm.vec3(0,0,1))
        
        rotationMat = pitch*yaw*roll
        scaleMat = glm.scale(identity,self.scale)
        
        return translateMat*rotationMat*scaleMat
        

    def render(self):
        
        #Atamos los buffers del object a la GPU
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
        glBindVertexArray(self.VAO)
        
        #Especificar la informacion de vertices
        #Buffer ID, Buffer Size in Bytes, Buffer data, Usagge
        glBufferData(GL_ARRAY_BUFFER,self.vertBuffer.nbytes,self.vertBuffer,GL_STATIC_DRAW)
        
        #Atributos
        #Especificar que representa el contenido del vertice
        #Attribute Number,Size,Type,Is it normalized,Stride,Offset

        #Atributo de posiciones
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        #Atributo de coordenadas de textura
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(4*3))
        glEnableVertexAttribArray(1)
        
        #Atributo de normales
        glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(4*5))
        glEnableVertexAttribArray(2)
      
        #Acrivar la textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D,                       #Texture type
                               0,                                   #Positions
                               GL_RGB,                              #Interal Format
                               self.textureSurface.get_width(),     #width
                               self.textureSurface.get_height(),    #height
                               0,                                   #Border
                               GL_RGB,                              #Format
                               GL_UNSIGNED_BYTE,                    #Type
                               self.textureData)                    #Data
        
        #glGenerateMipmap(GL_TEXTURE_2D)
        glGenerateTextureMipmap(self.textureBuffer)

        glDrawArrays(GL_TRIANGLES,0,int(len(self.vertBuffer)/8))
        
        