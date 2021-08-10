import tkinter as tk
from random import randint
import time,sys,math,os
# Import the bullet class
from .Bullet import Bullet
# Import the window size from the settings
from .settings import windowSize

class Enemy:
    def __init__(self,canvas,movementSpeed):
        self.canvas=canvas
        self.movementSpeed=movementSpeed

        # The general variables
        self.downBorder=360
        self.position=[randint(100,600),randint(100,self.downBorder)]
        self.hitboxOffset=25
        self.imageType=0

        self.lastShootTime=0
        self.shootDelay=2
        self.lastMoveTime=0
        self.timeMoveDelay=2

        # Load the images and sounds
        self.loadResources()

        # Configure the enemy
        self.configureEnemy()
    
    # The function that configures the enemy
    def configureEnemy(self):
        self.imageType=randint(0,len(self.enemyPhotos)-1)
        self.image=self.enemyPhotos[self.imageType]
    
    # The function that sets the image of the enemy
    def setImage(self,imageIndex):
        self.image=self.enemyPhotos[imageIndex-1]
        self.imageType=imageIndex-1

    # The function that draws the enemy
    def drawEnemy(self):
        self.canvas.create_image(self.position,image=self.image)

    # The function that moves the enemy
    def moveEnemy(self,newPosition):
        # Update the player position
        self.position[0]+=(newPosition[0]-self.position[0])/math.sqrt(newPosition[0]**2+self.position[0]**2+0.0001)*self.movementSpeed
        self.position[1]+=(newPosition[1]-self.position[1])/math.sqrt(newPosition[1]**2+self.position[1]**2+0.0001)*self.movementSpeed
        
        # Take actions if the enemy leaves the screen
        self.handleWindowExit()

    # The function that moves the enemy random
    def moveEnemyRandom(self):
        # If there is enough time since the last move
        if time.time()-self.lastMoveTime>self.timeMoveDelay:
            # Move the enemy
            self.moveVector=[randint(0,windowSize[0]),randint(0,self.downBorder)]
            self.moveEnemy(self.moveVector)
            # Update the last shoot time
            self.lastMoveTime=time.time()
        else:
            # Move the enemy
            self.moveEnemy(self.moveVector)

    # The function that set the position of the enemy
    def setPosition(self,position):
        self.position=position

    # The function that takes action when 2 enemies collide
    def enemyCollidedOtherEnemy(self):
        # Set a new position
        newPosition=[self.position[0]+self.image.height()/2,self.position[1]+self.image.width()/2]
        # Move the enemy
        self.moveEnemy(newPosition)

    # The function that takes action when the enemy shoot
    def enemyShoot(self):
        # If there is enough time since the last shoot
        if time.time()-self.lastShootTime>self.shootDelay:
            # Set the shoot position
            shootPosition=[self.position[0],self.position[1]+self.image.height()//2]
        
            # Create a new bullet
            bullet=Bullet(self.canvas,shootPosition,1,"#FF0000")
            # Update the last shoot time
            self.lastShootTime=time.time()
            return bullet
        return False

    # The function that takes action when the enemy leaves the screen
    def handleWindowExit(self):
        # If the enemy leaves the screen on X
        if self.position[0]<0:
            self.position[0]=windowSize[0]
        elif self.position[0]>windowSize[0]:
            self.position[0]=0
        # If the enemy leaves the screen on Y
        if self.position[1]<0:
            self.position[1]=0
        elif self.position[1]>self.downBorder:
            self.position[1]=0

    # The function that check if the enemy collides with another object
    def enemyCollision(self,objectCollided):
        width,height=self.image.width(),self.image.height()

        # The hitbox for X axis        
        if self.position[0]-width/2+self.hitboxOffset<objectCollided.position[0] and self.position[0]+width/2-self.hitboxOffset>objectCollided.position[0] :
            # The hitbox for Y axis
            if self.position[1]+height/2-self.hitboxOffset>objectCollided.position[1] and self.position[1]-height/2+self.hitboxOffset<objectCollided.position[1]:
                return True
        return False

    # The function that loads the images and sounds
    def loadResources(self):
        self.enemyPhotos=[]
        # Load all 3 enemy images
        for i in range(1,4):
            try:
                imagePath=os.path.join(os.path.dirname( __file__ ), '..', 'Assets','Spaceships','Enemy%s.png'%i)
                self.enemyPhotos.append(tk.PhotoImage(file=imagePath))
            except:
                print("error")