import tkinter as tk
import sys,os
# Go one directory back
sys.path.append("..")
# Import the window size from the settings
from Game.settings import windowSize

# The class that contains the leaderboards UI
class LeaderboardsFrame:
    # The constructor of the class
    def __init__(self,window,mainMenuButton):
        self.window=window
        self.mainMenuButton=mainMenuButton

        # The leaderboards frame
        self.frame=tk.Frame(self.window)

        # Create the canvas
        self.canvas=tk.Canvas(self.frame)
        self.canvas.pack(side="left",fill='both',expand=1)

        # Create the scrollbar
        self.scrollBar=tk.Scrollbar(self.frame,orient='vertical',command=self.canvas.yview)
        self.scrollBar.pack(side="right",fill="y")

        # Configure the frame
        #self.configureFrame()

    # The function that configures the frame
    def configureFrame(self):
        # Configure the canvas and bind the scrollbar to it
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind_all('<Configure>',lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Start from the top
        self.canvas.yview_moveto(0)
        self.canvas.yview_scroll(0,"units")

        # Add a frame inside the canvas
        self.labelFrame=tk.Frame(self.canvas)
        self.canvas.create_window((0,0),width=windowSize[0],window=self.labelFrame,anchor="nw")

    # Clear all the widgets
    def clearUI(self):
        # Get the UI components
        listUI=self.canvas.grid_slaves()
        if len(listUI)>0:
            # Destroy each widget
            for element in listUI:
                element.destroy()

    # The function that creates and displays the leaderboards
    def createLeadearboards(self):
        self.clearUI()
        self.configureFrame()
        self.getScores()
        self.displayLeaderboards()

    # The function that displays the leaderboards
    def displayLeaderboards(self):
        # Add leaderboards title
        tk.Label(self.labelFrame,text="Leaderboards", bg="#101010",fg="#ffff00",font="Arial 40").pack(fill="x")

        # Add a row in the leaderboards for each value from the file
        for index,position in enumerate(self.leaderboards,1):
            # Add the row
            leaderboardPosition=str(index)+". " + position[0]+ ": "+position[1]
            label=tk.Label(self.labelFrame,fg="white",text=leaderboardPosition,font="Arial 20")
            
            # Set the background color
            if index%2==0:
                label.config(bg="#282828")
            else:
                label.config(bg="#505050")
            
            # Display the label
            label.pack(fill="x")
        
        # Add the menu button
        menuBtn=tk.Button(self.labelFrame,text="Go to the main menu",command=self.mainMenuButton,height=5,bg="#101010",fg="#ffff00",font="Arial 20",activebackground="#101010",activeforeground="#ffff00")
        menuBtn.pack(fill="x")

    # The function that calculates the scores
    def getScores(self):
        # get the path
        path=os.path.join(os.path.dirname( __file__ ), '..', 'files','leaderboards.txt')
        positions=[]

        # Read the file
        with open(path,'r') as f:
            positions=f.read().split('\n')
        
        # Sort the scores
        self.sortScores(positions)

    # The function that sorts the scores
    def sortScores(self,positions):
        leaderboards=[]
        for item in positions:
            # Delete empty rows
            if item == "":
                positions.remove(item)
            else:
                # Add each record to the lise
                position=item.split()
                leaderboards.append((position[0],position[1]))

        # Sort and reverse the list
        self.leaderboards=sorted(leaderboards,key=lambda x: int(x[1]))
        self.leaderboards.reverse()
        print(self.leaderboards)