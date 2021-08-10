import tkinter as tk
import sys,os
# Go one directory back
sys.path.append("..")
# Import the window size, keys, username and the function that updates the username from the settings
from Game.settings import windowSize,keys,username,updateUsername
from Animations.BackgroundAnimations import BackgroundAnimations

# The class that contains the settings UI
class SettingsFrame:
    # The constructor of the class
    def __init__(self,window,settingsMenuButton):
        self.window=window
        self.settingsMenuButton=settingsMenuButton

        # General variables
        self.lastUsername=username
        self.pressedKey=""
        self.lastClicked=None
        self.margin=160
        self.buttonMargin=150
        
        # The frame of the settings
        self.frame=tk.Frame(self.window)

        # Configure the frame
        self.configureFrame()

        # Bind key pressed an mouse click event
        self.canvas.bind_all("<Button-1>",self.changeKeyBinding)
        self.canvas.bind_all("<KeyPress>", self.keyPressed)

    # The function that configures the frame
    def configureFrame(self):
        self.canvas=tk.Canvas(self.frame, width=windowSize[0], height=windowSize[1])
        self.canvas.pack(fill="x")

        # Create star background
        backgroundAnimations= BackgroundAnimations(self.canvas)
        backgroundAnimations.createStarBackground()

        # Add Settings title
        self.canvas.create_text(windowSize[0]//2,50,fill="#ffff00",font="Arial 40 bold",
                        text="Settings")

        # Add username label
        self.canvas.create_text(self.margin,150,fill="#ffff00",font="Arial 20 bold",
                        text="Username: ")

        self.createUI()

    # The function that creates the UI
    def createUI(self):
        # Create entry widget
        self.entry=tk.Entry(self.canvas, width=15, font="Arial 20")
        self.canvas.create_window(373,150,window=self.entry)
        # Set default value
        self.entry.insert("end",self.lastUsername)

        # Add each key to the menu
        for index,key in enumerate(keys,1):
            # The first half of the buttons will be in the left side
            if index <len(keys)/2:
                self.canvas.create_text(self.margin,150+45*index,fill="#ffff00",font="Arial 20 bold",
                        text=key+": ")
                button=tk.Button(self.canvas,text=keys[key], font="Arial 15",width=10)
                self.canvas.create_window(self.margin+self.margin, 150+45*index, window=button)
            # The second half of the buttons will be in the right side
            else:
                self.canvas.create_text(self.margin*5,150+45*(len(keys)-index),fill="#ffff00",font="Arial 20 bold",
                        text=key+": ")
                button=tk.Button(self.canvas,text=keys[key], font="Arial 15",width=10)
                self.canvas.create_window(self.margin*5+self.margin+50, 150+45*(len(keys)-index), window=button)

        # Create the main menu button
        menuButton=tk.Button(self.canvas,text="Menu",bg="#ffff00", font="Arial 20",command=self.mainMenuButton)
        self.canvas.create_window(windowSize[0]/2,500,window=menuButton)

    # The function that clear the UI
    def clearUI(self):
        # Get the UI components
        listUI=self.canvas.grid_slaves()
        # Get the last username
        self.lastUsername=self.entry.get()
        #Destroy each widget
        for element in listUI:
            element.destroy()

    # The function that saves the username and sends the user to the main menu
    def mainMenuButton(self):
        inputText=self.entry.get()
        updateUsername(inputText)
        # Go to the main menu
        self.settingsMenuButton()

    # The function that triggers when a click event occurs
    def changeKeyBinding(self,event):
        try:
            #Get the widget that was clicked
            pressedBtnText=event.widget.cget("text")
            # Get the wodget that was clicked
            self.lastClicked=self.findEventToBind(pressedBtnText)
        except:
            # Set the variable to None
            self.lastClicked=None

    # The function that bind the clicked widget to a key that was cliced
    def findEventToBind(self,text):
        # If the text is in the keys search it
        if text in keys.values():
            # Set the focus on the canvas
            self.canvas.focus_set()
            # Check if the text is in the keys and return the event key
            for event, key in keys.items():
                if key==text:
                    return event
        return False

     # The function that triggers when a click event occurs
    def keyPressed(self,event):
        # Get the key that was pressed
        pressedKey=event.keysym
        # If there is a valid click update the UI and change the pressed key
        if self.lastClicked in keys and (pressedKey in keys.values())==False:
            keys[self.lastClicked]=pressedKey
            # Update the UI
            self.clearUI()
            self.createUI()