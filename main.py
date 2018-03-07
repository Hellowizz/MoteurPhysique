# -*- coding: utf-8 -*-
from math       import *
from tkGraphPad import *
from geom import *
from copy import deepcopy

class Pmat :

  def __init__(self, mass, position, speed, force) :
    self.mass = mass
    self.position = position
    self.speed = speed
    self.force = force
    self.pasCompteurLeapFrog = 0
    #buffer de forces
    #self.h = 1 / Frequence echantillonage # Pas

  def gravity(self, g, t) :
    newPosY = (g.y / 2) * pow(t,2) + self.speed.y * t + Z0
    newPosX = (g.x / 2) * pow(t,2) + self.speed.x * t + Z0
    return Point(newPosX, newPosY)

    #print("x =", self.position.x, " y =", newPosY)

  def integrateurEulerExplicite(self, t, alpha) :
    self.position += t * self.speed
    self.speed += t * (self.force - (alpha / self.mass) * self.speed)

  def integrateurEulerImplicite(self, t, alpha) :
    self.speed = (self.mass / (self.mass + t * alpha)) * (self.speed + t * self.force)
    self.position += t * self.speed

  def leapFrog(self, h, alpha) :
    #if(self.pasCompteurLeapFrog % 2 == 0) :
    #  self.integrateurEulerImplicite(h, alpha)
    #else :
    #  self.integrateurEulerExplicite(h, alpha)

    #self.pasCompteurLeapFrog += 1
    
    self.speed += h * (self.force - (alpha / self.mass) * self.speed)
    self.position += h * self.speed

  def detectColision(self, h, alpha) :
    # position p(t)
    # delta_p(t) un vecteur

    cpy = deepcopy(self);

    actualPos = self.position
    cpy.leapFrog(h, alpha)
    nextPos = self.position;
    if(nextPos.y <= 0) :
      self.position.y = 0
      self.speed.y = -self.speed.y

    if(nextPos.y >= 5) :
      self.position.y = 5
      self.speed.y = -self.speed.y

    if(nextPos.x <= 0) :
      self.position.x = 0
      self.speed.x = -self.speed.x

    if(nextPos.x >= 10) :
      self.position.x = 10
      self.speed.x = -self.speed.x


class Link :

  def __init__(self, length, stiffness, viscous, seuil) :
    self.length = length # distance entre les particules
    #rempli une force
    self.stiffness = stiffness
    self.viscous = viscous
    self.seuil = seuil

#class fixPoint() :

#___________________VARIABLES GLOBALES___________________#

STEP = 0.001
X0 = 0.1
Z0 = 0.1
POSITION_INIT = Vecteur(X0, Z0)
ALPHA = 1
FORCE = Vecteur(0, -9.81)

boule = None
boulecpy = None
bouleBleue = None
bouleVerte = None

#_______________________FONCTIONS________________________#

#==========================
# Modeleur : Construction -- "statique"
def Modeleur() :
  ''' '''
  global boule
  global boulecpy
  global bouleBleue
  global bouleVerte

  #liste de particules
  #liste de ressorts

  vecSpeed = Vecteur(5, 9)
  boule = Pmat(4, POSITION_INIT, vecSpeed, FORCE)
  bouleBleue = Pmat(4, POSITION_INIT, vecSpeed, FORCE)
  bouleVerte = Pmat(4, POSITION_INIT, vecSpeed, FORCE)

  boulecpy = Pmat(4, POSITION_INIT, vecSpeed, FORCE)

  pass
    
#==========================
# fonction animatrice
def anim():
  """fonction animatrice"""
  global boule
  global bouleBleue
  global bouleVerte

  boule.integrateurEulerExplicite(STEP, ALPHA)
  bouleBleue.integrateurEulerImplicite(STEP, ALPHA)
  bouleVerte.leapFrog(STEP, ALPHA)
  bouleVerte.detectColision(STEP, ALPHA)
  bouleBleue.detectColision(STEP, ALPHA)
  boule.detectColision(STEP, ALPHA)

  pass
        
#==========================
# fonction de dessin
def draw():
  """fonction de dessin"""
  win.clear() # nettoyage
  dt = dtscale.get()

  global boule
  global boulecpy
  global bouleBleue
  global bouleVerte

  fillcircle(boule.position, 0.1, "maroon1")
  fillcircle(bouleBleue.position, 0.1, "blue")
  fillcircle(bouleVerte.position, 0.1, "SeaGreen1")
  

  vecGravity = Vecteur(0, -10)
  newPoint = boulecpy.gravity(vecGravity, STEP)
  cmpt = 0

  while newPoint.y >= 0 : 
    cmpt += 1
    posInit = boulecpy.position
    nextPoint = boulecpy.gravity(vecGravity, dt * cmpt)
    #print("new pos : ", boule.position.y)
    line(newPoint, nextPoint, "red", 0.1)
    newPoint = nextPoint
  
  pass

#____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
#==========================

  # Démarrage du réceptionnaire d'evenements :
  win=MainWindow("Corde 1D",900,450,"lightgrey")
  win.SetDrawZone(0,0,10,5)
      
  dt = 0.1
  Modeleur()    
  
  # scrollbars
  dtscale=win.CreateScalev(label='dt',inf=0,sup=1,step=0.01)
  dtscale.set(dt)

  win.anim=anim  
  win.draw=draw
  win.startmainloop()
