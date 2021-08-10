import tkinter as tk
from random import randint

# The class that keeps track of each star
class Star:
    # The maximum radius of the star
    maxStarRadius=5

    # The constructor of the class
    def __init__(self,canvas,position):
        self.canvas=canvas
        self.position=position
        
        # Get a random radius
        self.starRadius=randint(1,Star.maxStarRadius)

    # The function that display the star
    def drawStar(self):
        self.canvas.create_oval([self.position[0], self.position[1], self.position[0]+self.starRadius,self.position[1]+self.starRadius],fill='white')