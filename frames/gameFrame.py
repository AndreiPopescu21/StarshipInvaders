import tkinter as tk
import sys
# Go one directory back
sys.path.append("..")
# From the settings import the size of the window
from Game.settings import windowSize
# Import the Game
from Game.Game import Game

# The class that contains the game UI
class GameFrame:
    # The constructor of the class
    def __init__(self,window,leaderboardsMenu,leaderboardsFrame):
        self.window=window
        self.leaderboardsMenu=leaderboardsMenu
        self.leaderboardsFrame=leaderboardsFrame
        
        # The frame of the game
        self.frame=tk.Frame(self.window)

        # Configure the frame
        self.configureFrame()

    # The function that configures the frame
    def configureFrame(self):
        self.canvas=tk.Canvas(self.frame, width=windowSize[0], height=windowSize[1])
        self.canvas.pack(fill="x")

    # The function that starts the game
    def startGame(self):
        # Create the game
        game=Game(self.canvas,self.leaderboardsMenu,self.leaderboardsFrame)
        # Start the game
        game.startGame()

    # The function that loads the game
    def loadGame(self):
        # Create the game
        game=Game(self.canvas,self.leaderboardsMenu,self.leaderboardsFrame)
        # Load the game
        game.loadGame()