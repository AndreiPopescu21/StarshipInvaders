import tkinter as tk
from .Player import Player
# Import the window size, the keys and the username from the settings + the function that
# returns the username 
from .settings import windowSize, keys, username,getUsername
import sys,time,os
# Import the bullet class
from .Bullet import Bullet
# Import the enemy class
from .Enemy import Enemy
from random import randint, choice

# The class that controls the game
class Game:
    # the constructor of the class
    def __init__(self,canvas,leaderboardsMenu,leaderboardsFrame):
        self.canvas=canvas
        self.leaderboardsMenu=leaderboardsMenu
        self.leaderboardsFrame=leaderboardsFrame

        # Load resources
        self.loadResources()

        # Bind keyboard events
        self.keyPressed={}
        self.bindKeys()

        # The general variables
        self.run=True
        self.loaded=False
        self.paused=False
        self.bossMenu=False
        self.score=0

        self.numberOfEnemies=5
        self.shootDelay=1
        self.lastShootTime=2

        # The lists of objects
        self.Bullets=[]
        self.Enemies=[]

    # ---------- The Loop of the Game ---------------

    # The function that controls the game
    def gameLoop(self):
        if not self.loaded:
            self.setup()

        # Loop until the game ends
        while self.run:
            self.draw()
            self.getInput()
            self.handleEvents()

        self.handleEndGame()

    # ---------- Main Control Functions of The Game ----------------
    
    # The function that puts the game to an initial state
    def setup(self):
        # Set the variables to the initial state
        self.run=True
        self.paused=False

        # Create the player 
        self.player=Player(self.canvas)

    # The function that displays the game on the canvas
    def draw(self):
        # Clear the canvas
        self.canvas.delete('all')

        # Draw the canvas background
        self.setBackground()

        # Update the UI text
        self.drawText()

        # Draw the player
        self.player.drawPlayer()

        # Draw the enemies
        self.drawEnemies()

        # Draw the bullets
        self.drawBullets()

        # Update the canvas
        self.canvas.update()

    # The function that manages the input from the keyboard
    def getInput(self):
        if not self.paused:
            if self.keyPressed[keys["Move Up"]]:
                self.player.movePlayer([0,-1])
            if self.keyPressed[keys["Move Down"]]: 
                self.player.movePlayer([0,1])
            if self.keyPressed[keys["Move Left"]]: 
                self.player.movePlayer([-1,0])
            if self.keyPressed[keys["Move Right"]]: 
                self.player.movePlayer([1,0])
            if self.keyPressed[keys["Shoot"]]: 
                self.handleShoot()
            if self.keyPressed[keys["Add Lives Cheat"]]:
                self.addLivesCheat()
            if self.keyPressed[keys["Clear Enemies Cheat"]]:
                self.clearEnemiesCheat()
            if self.keyPressed[keys["Add Score Cheat"]]:
                self.addScoreCheat()
            if self.keyPressed[keys["Save"]]:
                self.saveGame()
            
                
        if self.keyPressed[keys["Boss Key"]]:
            self.bossKey()
        if self.keyPressed[keys["Pause"]]: 
            self.pauseGame()

    # The function that handles the events of the game
    def handleEvents(self):
        if self.handlePlayerCollision():
            self.run=False
        self.handleBullets()
        self.handleEnemies()
        self.handleEnemyCollision()
        self.handleWaves()

    # The function that handle the end of the game
    def handleEndGame(self):
        # Update the leaderboards
        self.updateLeaderboards()
        # Create the leaderboards and go to the leaderboards menu
        self.leaderboardsFrame.createLeadearboards()
        self.leaderboardsMenu()

    # --------- Handle UI -----------------------------

    # The function that sets the background
    def setBackground(self):
        self.canvas.create_image(windowSize[0]/2,windowSize[1]/2,image=self.backgroundImage)

    # The function that add text to the canvas
    def drawText(self):
        scoreText="Score: " + str(self.score)
        livesText="Lives: " + str(self.player.lives)

        # Add the score and the number of lives
        self.canvas.create_text(70,20,fill="#ffff00",font="Arial 20 bold",
                        text=scoreText)
        self.canvas.create_text(70,50,fill="#ffff00",font="Arial 20 bold",
                        text=livesText)

    # --------------- Handle Game Interrupts --------------

    # The function that pause the game
    def pauseGame(self):
        # Flip paused's value
        self.paused^=True
        # Clear the key pressed
        for key in self.keyPressed:
            self.keyPressed[key]=False
        
        # Loop while the game is paused
        while self.paused:
            # If the boss menu is activated, display the image
            if self.bossMenu:
                self.canvas.create_image([windowSize[0]//2,windowSize[1]//2],image=self.bossImage)
            # Get the input and update the canvas 
            self.getInput()
            self.canvas.update()

    # The function that displays the boss image
    def bossKey(self):
        # Flip bossMenu's value
        self.bossMenu^=1
        #Pause the game
        self.pauseGame()    

    # -------------- Add Cheat Events -------------------

    # The function that adds lives to the player
    def addLivesCheat(self):
        # Clear the key pressed
        for key in self.keyPressed:
            self.keyPressed[key]=False
        
        # Add lives
        self.player.addLives()

    # The function that clears the enemies
    def clearEnemiesCheat(self):
        self.Enemies.clear()

    # The function that adds points to score
    def addScoreCheat(self):
        # Clear the key pressed
        for key in self.keyPressed:
            self.keyPressed[key]=False

        # Add points to score
        self.score+=10

    # --------------- Handle Enemy Waves --------------

    # The function that handle
    def handleWaves(self):
        # If there are no enemies in the list generate a new wave
        if len(self.Enemies)==0:
            self.generateWave()

    # The function that generate enemy waves
    def generateWave(self):
        # Create a new enemy on each iteration
        for i in range(0,self.numberOfEnemies):
            enemy=Enemy(self.canvas,min(2,0.4*(1+self.score//10)))
            # Decrease the shooting delay
            enemy.shootDelay=max(1,enemy.shootDelay-self.score//10)
            self.shootDelay=max(1,self.shootDelay-self.score//10)
            
            # Add the enemy to the list of enemies
            self.Enemies.append(enemy)

    # ---------- Handle Keyboard Input ----------------

    # The function that bind the key events
    def bindKeys(self):
        # Go through all the keys from the settings
        for character in keys:
            # Set the event for key pressed
            self.canvas.bind_all("<KeyPress-%s>" % keys[character], self.keyPressedEvent)
            # Set the event for key released
            self.canvas.bind_all("<KeyRelease-%s>" % keys[character], self.keyReleasedEvent)
            # Update the key pressed in dictionary
            self.keyPressed[keys[character]] = False

    # The function that takes action when a key is pressed
    def keyPressedEvent(self, event):
        self.keyPressed[event.keysym] = True

    # The function that takes action when a key is released
    def keyReleasedEvent(self, event):
        self.keyPressed[event.keysym] = False
    
    # ----------- Handle Player Events ------------------

    # The function that handles the player collisions
    def handlePlayerCollision(self):
        collided=False
        # Loop through all the bullet and take action if they collided
        for bullet in self.Bullets:
            if bullet.direction==1:
                collided=self.player.playerCollision(bullet)
                if collided==True:
                    self.Bullets.remove(bullet)
        # If there are no remaining lives return True
        if self.player.lives<=0:
            return True
        return False

    # The function that handles the player shoot
    def handleShoot(self):
        bullet=self.player.playerShoot()
        if bullet!=False:
            self.Bullets.append(bullet)

    # ------------ Handle Enemies ----------------------

    # The function that draws the enemies
    def drawEnemies(self):
        for enemy in self.Enemies:
            enemy.drawEnemy()

    # The function that handles the enemies
    def handleEnemies(self):
        # Trigger enemy shoot event
        self.enemyShoot()

        # Loop through each enemy and move it
        for enemy in self.Enemies:
            enemy.moveEnemyRandom()

        # Handle Collision event
        self.handleEnemyCollision()

    # The function that handles the enemy shoot event
    def enemyShoot(self):
        # If it passed enough time since the last shoot
        if time.time()-self.lastShootTime>self.shootDelay and len(self.Enemies)>0:
            # Get a list of random enemies
            enemiesShoot=[choice(self.Enemies) for i in range(0,randint(0,len(self.Enemies))//2)]
        
            # Loop through the list of random enemies and shoot
            for enemy in enemiesShoot:
                bullet=enemy.enemyShoot()
                if bullet!=False:
                    self.Bullets.append(bullet)

            # Update the last shoot time
            self.lastShootTime=time.time()

    # The function that takes action when the enemy collides with another object
    def handleEnemyCollision(self):
        # Loop through all enemies
        for enemy in self.Enemies:
            # If the enemy collides with the player
            if enemy.enemyCollision(self.player):
                self.player.handleCollision()
                try:
                    self.Enemies.remove(enemy)
                except:
                    pass
            # Loop through the bullets
            for bullet in self.Bullets:
                # If the enemy collided with an enemy bullet remove it and update score
                if enemy.enemyCollision(bullet) and bullet.direction==-1:
                    try:
                        self.Enemies.remove(enemy)
                    except:
                        pass
                    self.Bullets.remove(bullet)
                    self.score+=1
            # If the enemy collided with another enemy take actions
            for otherEnemy in self.Enemies:
                if enemy.enemyCollision(otherEnemy) and enemy!=otherEnemy:
                    enemy.enemyCollidedOtherEnemy()           

    # ----------- Handle Bullets -----------------------

    # The function that handle the bullets on the screen
    def handleBullets(self):
        for bullet in self.Bullets:
            bullet.updateBullet()
            if bullet.position[1]< 0 or bullet.position[1]>windowSize[1]:
                self.Bullets.remove(bullet)

    # The function that draw the bullets on the screen
    def drawBullets(self):
        for bullet in self.Bullets:
            bullet.drawBullet()


    # ----------- Save Game ---------------------------

     # The function that saves the game
    def saveGame(self):
        # Clear all the pressed keys
        for key in self.keyPressed:
            self.keyPressed[key]=False

        # Get the save data
        saveData=self.saveGameData()

        # Write the save data in the file
        path=os.path.join(os.path.dirname( __file__ ),"..","files","save.txt")
        with open(path,'w') as f:
            f.write(saveData) 

    # The function that formats the save file
    def saveGameData(self):
        saveData=""
        # Add the score to the data save
        saveData+="Score "+str(self.score)+'\n'
        # Add the player to the data save
        saveData+="Player "+str(self.player.position[0])+" "+str(self.player.position[1])+" "+str(self.player.lives)+'\n'
        # Add the enemies to the data save
        for enemy in self.Enemies:
            save="Enemy "+str(enemy.position[0])+" "+str(enemy.position[1])+" "+str(0.2*(1+self.score//10))+" "+str(enemy.lastShootTime)+" "+str(enemy.imageType+1)+"\n"
            saveData+=save
        # Add the bullets to the data save
        for bullet in self.Bullets:
            save="Bullet "+str(bullet.position[0])+" "+str(bullet.position[1])+" "+str(bullet.direction)+" "+str(bullet.color)+'\n'
            saveData+=save
        return saveData

    # ----------- Update the Leaderboards --------------
    
    # The function that updates the leaderboards
    def updateLeaderboards(self):
        # Get the path to the leaderboards
        leaderboardsPath=os.path.join(os.path.dirname( __file__ ), '..', 'files','leaderboards.txt')
        # Create the leaderboards text
        text=getUsername()+" "+str(self.score)

        # Update the leaderboards file
        if(os.path.exists(leaderboardsPath)==False):
            with open(leaderboardsPath,'w') as f:
                f.write(text+'\n')
        else:
            with open(leaderboardsPath, 'a') as f:
                f.write(text+'\n')    

    # ----------- Game Start or Load ------------------

    # The function that starts the game
    def startGame(self):
        self.loaded=False

        # Call the game loop
        self.canvas.after(1,self.gameLoop())

    # The function that loads the game
    def loadGame(self):
        self.loaded=True

        loadedData=[]
        # Load data from the file
        try:
            path=os.path.join(os.path.dirname(__file__),"..","files","save.txt")
            with open(path,'r') as f:
                loadedData=f.read().split('\n')
        except:
            print("error")

        # If there is data in the file load the game
        if len(loadedData)>1 or (len(loadedData)==1 and loadedData[0]!=''):
            # Loop through all the data in the file
            for data in loadedData:
                data=data.split()
                # If there is an empty row ignore it
                if len(data)==0:
                    continue
                # Update the score from the file
                if data[0]=="Score":
                    self.score=int(data[1])
                # Update the player from the file
                elif data[0]=="Player":
                    self.player=Player(self.canvas)
                    self.player.position=[float(data[1]),float(data[2])]
                    self.player.lives=int(data[3])
                # Update the enemy from the file
                elif data[0]=="Enemy":
                    enemy=Enemy(self.canvas,float(data[3]))
                    enemy.position=[float(data[1]),float(data[2])]
                    enemy.lastShootTime=float(data[4])
                    enemy.setImage(int(data[5]))
                    self.Enemies.append(enemy)
                # Update the bullet from the file
                elif data[0]=="Bullet":
                    bullet=Bullet(self.canvas,[float(data[1]),float(data[2])],int(data[3]),data[4])
                    self.Bullets.append(bullet)
        # Else start a new game
        else:
            self.loaded=False

        # Start the game
        self.canvas.after(1,self.gameLoop())


    # -------------------- Load Resources -----------------

    # The function that loads the resources
    def loadResources(self):
        # Load Boss Image
        imagePath=os.path.join(os.path.dirname( __file__ ), '..', 'Assets','UI','bossImage.png')
        self.bossImage=tk.PhotoImage(file = imagePath)

        # Load Background Image
        backgroundPath=os.path.join(os.path.dirname( __file__ ), '..', 'Assets','UI','Background.png')
        self.backgroundImage=tk.PhotoImage(file = backgroundPath)