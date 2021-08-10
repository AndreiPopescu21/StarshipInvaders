import tkinter as tk
import sys,os
# Go one directory back
sys.path.append("..")
# Get the size of the window from the settings
from Game.settings import windowSize
# Get the star background from the animations
from Animations.BackgroundAnimations import BackgroundAnimations
# Import the Game
from Game.Game import Game

# The class that contains the menu UI
class MenuFrame:
    # The constructor of the class
    def __init__(self,window,menuPlayButton,settingsButton,gameFrame):
        self.window=window
        self.gameFrame=gameFrame
        self.menuPlayButton=menuPlayButton
        self.settingsButton=settingsButton

        # The offset between images
        self.imageOffset=60
        
        # The frame of the menu
        self.frame=tk.Frame(self.window)

        # Load the images and sounds        
        self.loadResources()

        # Configure the menu UI
        self.menuConfig()

    # The function that loads the images and sounds
    def loadResources(self):
        # Handle exceptions
        try:
            # The path to UI Buttons
            UIButtonPath=os.path.join(os.path.dirname( __file__ ),"..","Assets","UI","Buttons")
    
            # Load Start Button Image
            startImagePath=os.path.join(UIButtonPath,"Start_BTN.png")
            self.startImage=tk.PhotoImage(file=startImagePath)

            # Load the Load Button Image
            loadImagePath=os.path.join(UIButtonPath,"Load_BTN.png")
            self.loadImage=tk.PhotoImage(file=loadImagePath)

            # Load the Exit Button Image
            exitImagePath=os.path.join(UIButtonPath,"Exit_BTN.png")
            self.exitImage=tk.PhotoImage(file=exitImagePath)

            # Load the Setttings Button Image
            settingsImagePath=os.path.join(UIButtonPath,"Settings_BTN.png")
            self.settingsImage=tk.PhotoImage(file=settingsImagePath)
        except:
            print("Error when loading resources")

    # The function that configure the menu UI
    def menuConfig(self):
        # Create and display the canvas
        self.canvas=tk.Canvas(self.frame,width=windowSize[0],height=windowSize[1])
        self.canvas.pack()

        # Create the star background
        backgroundAnimations=BackgroundAnimations(self.canvas)
        backgroundAnimations.createStarBackground()

        # Add the game title
        self.canvas.create_text(windowSize[0]/2,60,fill="#ffff00",font="Arial 40", text="Starship Invaders")

        # Add play button
        playButton = tk.Button(self.canvas,bg="black", image =self.startImage, command = self.playButtonClick, width=397,height=113,borderwidth=0,activebackground="black")
        playButtonY=200
        playButtonDisplay=self.canvas.create_window(windowSize[0]/2,playButtonY,window=playButton)

        # Add load button
        loadButton = tk.Button(self.canvas,bg="black", image =self.loadImage, command = self.loadButtonClick, width=113,height=113,borderwidth=0,activebackground="black")
        loadButtonX=windowSize[0]/2+self.startImage.width()/2+self.imageOffset
        playButtonY=playButtonY
        loadButtonDisplay=self.canvas.create_window(loadButtonX,playButtonY,window=loadButton)

        # Add exit button
        exitButton = tk.Button(self.canvas,bg="black", image =self.exitImage, command = self.exitButtonClick, width=397,height=113,borderwidth=0,activebackground="black")
        exitButtonY=340
        exitButtonDisplay=self.canvas.create_window(windowSize[0]/2,exitButtonY,window=exitButton)

        # Add settings button
        settingsButton = tk.Button(self.canvas,bg="black", image =self.settingsImage, command = self.settingsButtonClick, width=113,height=113,borderwidth=0,activebackground="black")
        settingsButtonY=340
        settingsButtonX=loadButtonX
        settingsButtonDisplay=self.canvas.create_window(settingsButtonX,settingsButtonY,window=settingsButton)

    # The function that triggers when the play button is pressed
    def playButtonClick(self):
        # Load the game frame
        self.menuPlayButton()
        # Start the game
        self.gameFrame.startGame()

    # The function that triggers when the load button is pressed
    def loadButtonClick(self):
        # Load the game frame
        self.menuPlayButton()
        # Load the game
        self.gameFrame.loadGame()

    # The function that triggers when the exit button is pressed   
    def exitButtonClick(self):
        sys.exit()

    # The function that triggers when the settings button is pressed   
    def settingsButtonClick(self):
        # Load the settings menu
        self.settingsButton()