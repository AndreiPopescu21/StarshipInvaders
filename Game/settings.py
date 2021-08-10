import os

username=os.getlogin()
windowSize=(1280,720)

keys={
    "Move Up": "w",
    "Move Down": "s",
    "Move Left": "a",
    "Move Right": "d",
    "Shoot": "space",
    "Add Lives Cheat": "1",
    "Clear Enemies Cheat": "2",
    "Add Score Cheat": "3",
    "Boss Key": "b",
    "Pause": "p",
    "Save": "m"
}

def updateUsername(newUsername):
    global username
    username=newUsername

def printUsername():
    print(username)

def getUsername():
    return username