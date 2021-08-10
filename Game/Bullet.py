import tkinter as tk
# Import the size of the window from the settings
from .settings import windowSize
import time

# The class that controls the bullets
class Bullet:
    def __init__(self,canvas,position,direction,color):
        self.canvas=canvas
        self.position=position
        self.direction=direction
        self.color=color

        # The general variables
        self.thickness=4
        self.height=15
        self.movementSpeed=2

    # The function that draws the bullet
    def drawBullet(self):
        self.canvas.create_line(self.position[0], self.position[1], self.position[0], self.position[1]+self.height,fill=self.color, width=self.thickness)

    # The function that updates the bullet
    def updateBullet(self):
        self.position[1]+=self.direction*self.movementSpeed