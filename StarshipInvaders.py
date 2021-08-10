# The resolution of the screen is 1280x720
# This file should be run such that the app will work as expected

import tkinter as tk
# Import the size of the window from settings
from Game.settings import windowSize
# From frame manager import the function that updates the current displayed frame and
# the function that returns all the frames
from frames.frameManager import showFrame, getFrames


# The function that configures the window
def configureWindow(title,windowSize):
    # Set the window size and title
    window.title(title)
    window.geometry(str(windowSize[0])+"x"+str(windowSize[1]))

    # Configure rows and columns
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Add each frame to the window
    for frame in frames:
        frames[frame].grid(row=0,column=0,sticky="nsew")

    # Show the menu frame
    showFrame(frames["menuFrame"])

# This function displays the game frame
def showGame():
    showFrame(frames["gameFrame"])

# This function displays the Settings frame
def showSettings():
    showFrame(frames["settingsFrame"])

# This function displays the menu frame
def showMenu():
    showFrame(frames["menuFrame"])

# This function displays the leadrboards frame
def showLeaderboards():
    showFrame(frames["leaderboardsFrame"])

# Instantie the window
window=tk.Tk()

# Set the window title
title="Starship Invaders"

# Create a dictionary with the functions that change the current frame
changeFrameFunctions={"menuPlayButton":showGame,
                    "menuSettingsButton":showSettings,
                    "settingsMenuButton":showMenu,
                    "leaderboardsFrame":showLeaderboards}

# Get all the frames
frames=getFrames(window,changeFrameFunctions)

# Configure the window
configureWindow(title, windowSize)

# Update
window.mainloop()