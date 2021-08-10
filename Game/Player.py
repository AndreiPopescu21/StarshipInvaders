import tkinter as tk
import time,os
# Load the size of the window from settings
from .settings import windowSize
from .Bullet import Bullet

# The class that controls the player
class Player():
    # The constructor of the function
    def __init__(self,canvas):
        self.canvas=canvas

        # Load images and sounds
        self.loadResources()

        # The general variables
        self.position=[windowSize[0]//2,windowSize[1]-200]
        self.movementSpeed=0.6
        self.lives=2
        self.hitboxOffset=25

        self.lastShootTime=0
        self.lastShootSide=0
        self.shootDelay=1

    # The function that draws the player
    def drawPlayer(self):
        # Add the player to the canvas
        self.displayedPlayer=self.canvas.create_image(self.position,image=self.image)

    # The function that moves the player
    def movePlayer(self,moveVector):
        # Update player's coordinates
        self.position[0]+=moveVector[0]*self.movementSpeed
        self.position[1]+=moveVector[1]*self.movementSpeed

        # Take actions if the player leaves the window
        self.handleWindowExit()

    # The function that takes action if the player leaves the window
    def handleWindowExit(self):
        # If the player leaves the screen on X coordinates
        if self.position[0]<0:
            self.position[0]=windowSize[0]
        elif self.position[0]>windowSize[0]:
            self.position[0]=0

        # If the player leaves the screen on Y coordinates
        if self.position[1]<0:
            self.position[1]=windowSize[1]
        elif self.position[1]>windowSize[1]:
            self.position[1]=0

    # The function that check if the player collided with any object
    def playerCollision(self,objectCollided):
        width,height=self.image.width(),self.image.height()
        
        # The hitbox for X axis
        if self.position[0]-width/2+self.hitboxOffset<objectCollided.position[0] and self.position[0]+width/2-self.hitboxOffset>objectCollided.position[0] :
            # The hitbox for Y axis
            if self.position[1]+height/2-self.hitboxOffset>objectCollided.position[1] and self.position[1]-height/2+self.hitboxOffset<objectCollided.position[1]:
                self.handleCollision()    
                return True

        return False

    # The function that takes action when the player collides with any object
    def handleCollision(self):
        self.lives-=1

    # The function that triggers when the player shoots
    def playerShoot(self):
        # If there was enough time since the last shoot
        if time.time()-self.lastShootTime>self.shootDelay:
            shootPosition=[0,0]

            # Change the side of the shot bullet
            if self.lastShootSide==1:
                shootPosition[0]=self.position[0]+self.image.width()/5
            else:
                shootPosition[0]=self.position[0]-self.image.width()/5
            shootPosition[1]=self.position[1]-self.image.height()/8
            self.lastShootSide^=1
        
            # Create Bullet
            bullet=Bullet(self.canvas,shootPosition,-1,"#00FF00")

            # Update the last time the player shot
            self.lastShootTime=time.time()
            return bullet
        return False

    # The function that adds lives to the player
    def addLives(self):
        self.lives+=10

    # The function that loads the images and sounds
    def loadResources(self):
        # Load resources
        try:
            # Path to the spaceships folder
            path=os.path.join(os.path.dirname( __file__ ), '..', 'Assets','Spaceships')
            # Player image
            playerImagePath=os.path.join(path,'Player_Starship.png')
            self.image=tk.PhotoImage(file = playerImagePath)

        except:
            print("error")