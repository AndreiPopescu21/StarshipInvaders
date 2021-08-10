# Import Frames
from frames.menuFrame import MenuFrame
from frames.gameFrame import GameFrame
from frames.settingsFrame import SettingsFrame
from frames.leaderboardsFrame import LeaderboardsFrame

# This function returns a dictionary with all the frames
def getFrames(window,changeFrameFunctions):
    # Instantiate frames
    leaderboardsFrame=LeaderboardsFrame(window,changeFrameFunctions["settingsMenuButton"])
    gameFrame=GameFrame(window,changeFrameFunctions["leaderboardsFrame"],leaderboardsFrame)
    menuFrame=MenuFrame(window,changeFrameFunctions["menuPlayButton"],changeFrameFunctions["menuSettingsButton"],gameFrame)
    settingsFrame=SettingsFrame(window,changeFrameFunctions["settingsMenuButton"])
    
    # Return a dictionary of frames
    return {"menuFrame":menuFrame.frame,
        "gameFrame":gameFrame.frame,
        "settingsFrame":settingsFrame.frame,
        "leaderboardsFrame":leaderboardsFrame.frame}

# This function displays the desired frame
def showFrame(frame):
    # Raise the desired frame on top of the others
    frame.tkraise()