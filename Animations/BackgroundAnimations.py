import tkinter as tk
from random import randint
import sys
# Import the star class
from .Star import Star
# Go one directory back
sys.path.append("..")
# From settings import the size of the window
from Game.settings import windowSize

# The class that animates the background
class BackgroundAnimations:
    # The constructor of the class
    def __init__(self,canvas):
        self.canvas=canvas
        
        # Set the number of stars
        self.starNumber=500

        # The speed of the stars
        self.speed=2

    # The function that creates a background with stars
    def createStarBackground(self):
        # Set the canvas background to black
        self.canvas.configure(bg="black")

        # Add the stars to the canvas
        for i in range(0,self.starNumber):
            # Create a random position for the star
            position=[randint(0,windowSize[0]),randint(0,windowSize[1])]

            # Create and draw the star
            star=Star(self.canvas,position)
            star.drawStar()
