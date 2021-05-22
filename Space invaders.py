import pygame, random, string

pygame.init()
screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode((screenWidth,screenHeight))

# audio
pygame.mixer.init()
fireSnd = pygame.mixer.Sound("shoot.wav")
invDeathSnd = pygame.mixer.Sound("invaderkilled.wav")
invMove1Snd = pygame.mixer.Sound("fastinvader1.wav")
invMove2Snd = pygame.mixer.Sound("fastinvader2.wav")
invMove3Snd = pygame.mixer.Sound("fastinvader3.wav")
invMove4Snd = pygame.mixer.Sound("fastinvader4.wav")
invMoveSnds = [invMove1Snd,invMove2Snd,invMove3Snd,invMove4Snd]
playerDeathSnd = pygame.mixer.Sound("explosion.wav")
UfoLoopSnd = pygame.mixer.Sound ("UfoSound.wav")
#spaceship = pygame.mixer.Sound("")

class HighScore():
    def __init__(self,filename):
        try:
            self.f = open(filename, 'r+')
        except:
            self.f = open(filename, 'w')
        self.f.close()
        self.fName = filename
        
    def save(self,name,score):
        self.f = open(self.fName, "r+")
        foundSmaller = False
        lineList = self.f.readlines()
        self.f.close()
        i = 0
        while not foundSmaller:
            lnScore = int(lineList[i].split(" ")[1][:-1])
            if lnScore < score:
                foundSmaller = True
            i += 1
        lineList.insert(i-1,name + " " + str(score) + '\n')
        self.f = open(self.fName, "w")
        for line in lineList:
            self.f.write(line)
        self.f.close()

    def drawTop5(self, surf):
        self.f = open(self.fName, "r")
        for i in range(5):
            line = self.f.readline()[:-1]
            highScoreText = arcadeFontSmall.render(line,True,menuFontColor)
            highScoreTextRect = highScoreText.get_rect()
            highScoreTextRect.center = (screenWidth//2,screenHeight//2 - 80 + (i+1) * 40)
            surf.blit(highScoreText, highScoreTextRect)
        self.f.close()


def pointRectIntersect(pt, r):
    rx,ry,rw,rh = r[0],r[1],r[2],r[3]
    ptx, pty = pt[0], pt[1]
    if ptx > rx:
        if ptx < rx + rw:
            if pty > ry:
                if pty < ry + rh:
                    return True
    return False

def rectRectIntersect(a,b):
    ax,ay,aw,ah = a[0],a[1],a[2],a[3]
    bx,by,bw,bh = b[0],b[1],b[2],b[3]

    # test all 4 corners of a inside b?
    if pointRectIntersect((ax,ay),b):
        return True
    elif pointRectIntersect((ax+aw,ay),b):
        return True
    elif pointRectIntersect((ax+aw,ay+ah),b):
        return True
    elif pointRectIntersect((ax,ay+ah),b):
        return True
    # test all 4 corners of b inside a?
    elif pointRectIntersect((bx,by),a):
        return True
    elif pointRectIntersect((bx+bw,by),a):
        return True
    elif pointRectIntersect((bx+bw,by+bh),a):
        return True
    elif pointRectIntersect((bx,by+bh),a):
        return True
    return False

# Dynamic blocks
class Multiblock():
    def __init__(self,x,y,w,h,col = (255,255,255), nx = 5,ny = 5):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.nx, self.ny = nx, ny
        self.bW = self.w / self.nx
        self.bH = self.h / self.ny
        self.col = col
        self.blocks = []
        curY = self.y
        for y in range(self.ny):
            curX = self.x
            for x in range(self.nx):
                self.blocks.append((curX,curY,self.bW,self.bH))
                curX += self.bW
            curY += self.bH
                
    
    def draw(self, surf):
        for block in self.blocks:
            pygame.draw.rect(screen, self.col, block)
        return screen
 
    def checkHit(self, r):
        for block in self.blocks:
            if rectRectIntersect(block,r):
                return block
        return False
    
    def destroyOnHit(self,r):
        block = self.checkHit(r)
        if block != False:
            self.blocks.remove(block)
            return True
        return False

# Game Variables
# General
padding = 20

# Player
pWidth = 60
pHeight = 30
pX = screenWidth//2 - pWidth//2
pY = screenHeight - pHeight - padding
playerSpeed = 10
pCol = (0,255,0)
numLives = 3
playerStart = True
flashTime = 100
numFlashes = 12
flashCount = 0

# Bullets
bulletW = 3
bulletH = 11
bulletSpeed = 8


# Player Bullet
pBulletX = -100
pBulletY = -100
pBulletCol = (0,255,255)

# Invader Bullets
invBullets = []
invFireChance = 0.25 # % of time.
invBulletCol = (255,0,0)

# Shields
shields = []
shieldW = 80
shieldH = 40
numShields = 4
shieldSpace = screenWidth // (numShields + 1)
sheildY = screenHeight - shieldH - pHeight - padding * 2
for s in range(numShields):
    shields.append(Multiblock(shieldSpace*(s+1)-shieldW//2,sheildY,shieldW,shieldH,nx=shieldW//8,ny=shieldH//8 ))

pygame.font.init()
# Menus
arcadeFont = pygame.font.Font("ARCADECLASSIC.TTF",100)
arcadeFontSmall = pygame.font.Font("ARCADECLASSIC.TTF",30)
menuFontColor = (255,255,255)
PLAY, END, HIGHSCORE, VICTORY, NAMESCREEN = 0, 1, 2, 3, 4
gameState = PLAY


# Invaders
class Invader():
    def __init__(self, x, y, w, h, f, col):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.f = f
        self.c = col
        self.oddMove = 0
    def hitRect(self,r):
        return rectRectIntersect((r[0],r[1],r[2],r[3]),(self.x,self.y,self.w, self.h))
    def draw(self, surf, font):
        invaderCharacter = font.render(self.f,True,self.c)
        invaderRect = invaderCharacter.get_rect()
        invaderRect.topleft = (self.x,self.y)
        surf.blit(invaderCharacter, invaderRect)
    def animate(self):
        if self.oddMove == 0:
            self.oddMove = 1
            self.f = chr(ord(self.f)+1)
        else:
            self.oddMove = 0
            self.f = chr(ord(self.f)-1)

class Invaders():
    def __init__(self, numRows, numCols, invHeight = 32, invWidth = 32, invCol = (0,255,0), invTime = 1000, invFont = "invaders.ttf"):
        self.invRows = numRows
        self.invCols = numCols
        self.invaders = []
        self.invDir = 1
        self.invaderHeight = invHeight
        self.invaderWidth = invWidth
        self.invaderCol = invCol
        self.invTimer = invTime# how many milliseconds before they move
        self.lastRow = []
        self.invaderFont = pygame.font.Font(invFont,self.invaderHeight)
        self.soundCount = 0
        self.initInvaders()

    def initInvaders(self):
        #xSpc = screenWidth // (self.invRows *3)
        xSpc = self.invaderWidth * 2
        ySpc = xSpc * 0.8
        invLetters = ['A','C','G','E','I']
        for y in range(self.invRows):
            for x in range(self.invCols):
                self.invaders.append(Invader(x*xSpc+xSpc,y*ySpc+ySpc,self.invaderWidth,self.invaderHeight,invLetters[y],self.invaderCol))
        self.calcLastRow()

    def calcLastRow(self):
        self.lastRow = []
        cols = []
        for i in range(len(self.invaders)):
            found = False
            for col in cols:
                if self.invaders[i].x == self.invaders[col[0]].x:
                    col.append(i)
                    found = True
            if not found:
                cols.append([i])

        for col in cols:
            self.lastRow.append(self.invaders[col[-1]])

    def move(self):
        invMoveSnds[self.soundCount].play()
        self.soundCount += 1
        if self.soundCount > 3:
            self.soundCount = 0
        for invader in self.invaders:
            invader.x += self.invaderWidth * self.invDir
            invader.animate()
        for invader in self.invaders:
            if invader.x >= screenWidth or invader.x <= 0:
                self.invDir *= -1
                self.invTimer *= 0.90 # 10% faster
                for invader in self.invaders:
                    invader.y += self.invaderHeight
                    invader.x += self.invaderWidth * self.invDir
                break
    
    def destroyIfHit(self,r):
        for invader in self.invaders:
            if invader.hitRect(r):
                self.invaders.remove(invader)
                self.calcLastRow()
                invDeathSnd.play()
                return True
        return False

    def fireLastRow(self,chance):
        invBullets = []
        for lRInv in self.lastRow:
            if random.uniform(0,100) < chance:
                invBullets.append([lRInv.x+self.invaderWidth//4,lRInv.y + self.invaderHeight//2,bulletW,bulletH])
        return invBullets

    def draw(self,surf):
        for invader in self.invaders:
            invader.draw(surf,self.invaderFont)

    def num(self):
        return len(self.invaders) 

# UFO VARIABLES
# create the variables for the UFO, position in x, position in y, 
# sound, points, speed, colour, choice between two possible characters
# set a minumum start time and a 'random chance' for UFO to appear
# make a timer to count up to minimum time.
UfoX = -1000
UfoY = 20
UfoHeight = 24
UfoTimer = 0
UfoMinTime = 5000
UfoPercentChance = 0.01
UfoSpeed = 2
UfoMoving = False
UfoFont = pygame.font.Font("Invaders.ttf",UfoHeight)


clock = pygame.time.Clock()
gameOver = False
moveDir = 0
playerFire = False
timeCounter = 0
flashCounter = 0
score = 0
allInvaders = Invaders(4,10,invWidth=25,invHeight=25)
hScore = HighScore("spaceInvadersHS.txt")
scoreSaved = False
nameScreenNumKeysPressed = 0
name = ""
while not gameOver:
    # interactivity ------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moveDir = -playerSpeed
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moveDir = playerSpeed
            if event.key == pygame.K_SPACE:
                playerFire = True
                if gameState == END or gameState == VICTORY:
                    gameState = NAMESCREEN
            if event.key == pygame.K_LEFTBRACKET:
                allInvaders.invTimer *= 1.1
            if event.key == pygame.K_RIGHTBRACKET:
                allInvaders.invTimer *= 0.9
            if event.key == pygame.K_BACKSLASH:
                allInvaders.invaders.remove(random.choice(allInvaders.invaders))
                allInvaders.calcLastRow()
            if gameState == NAMESCREEN:
                if event.unicode in string.ascii_letters:
                    if nameScreenNumKeysPressed < 3:
                        name += event.unicode
                    nameScreenNumKeysPressed += 1
                if nameScreenNumKeysPressed >= 4:
                    gameState = HIGHSCORE
                    nameScreenNumKeysPressed == 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                moveDir = 0
    
    # deal with play state
    if gameState == PLAY:
        # Player Movement
        pX += moveDir
        if pX < 0:
            pX = 0

        if pX + pWidth > screenWidth:
            pX = screenWidth - pWidth
            
        # Invaders Movment
        if timeCounter >= allInvaders.invTimer:
            timeCounter -= allInvaders.invTimer
            allInvaders.move()
            
            #Check if invader intersect player
            for inv in allInvaders.invaders:
                if rectRectIntersect((inv.x,inv.y,inv.h,inv.w),(pX,pY,pWidth,pHeight)):
                    playerDeathSnd.play()
                    gameState = END
        
            if allInvaders.num() == 0:
                gameState = VICTORY
        
        #Check if invader intersect shield
        for inv in allInvaders.invaders:
            for shield in shields:
                if shield.destroyOnHit((inv.x,inv.y,inv.h,inv.w)):
                   pass

        
        # Bullets
        # if player fires and bullet is off screen already
        if playerFire and pBulletY < -bulletH:
            pBulletX = pX + pWidth // 2 - bulletW // 2
            pBulletY = pY - bulletH
            playerFire = False
            fireSnd.play()
        elif playerFire:
            playerFire = False
        # Player Bullet Movement if it's on screen
        if pBulletY > -bulletH:
            pBulletY -= bulletSpeed
            if allInvaders.destroyIfHit((pBulletX,pBulletY,bulletW,bulletH)):
                pBulletY = -100
                score += 100
            for shield in shields:
                if shield.destroyOnHit((pBulletX,pBulletY,bulletW,bulletH)):
                        pBulletY = -100
            
        # Invaders Bullet Movement
        invBullets += allInvaders.fireLastRow(invFireChance)
        for invBull in invBullets:
            try:
                invBull[1] += bulletSpeed
                # if intersect with player
                if rectRectIntersect(invBull,(pX,pY,pWidth,pHeight)) and not playerStart:
                    playerDeathSnd.play()
                    #pY = -1000
                    pX = screenWidth//2 - pWidth//2
                    invBull[1] = screenHeight + 1
                    numLives -= 1
                    playerStart = True
                    if numLives == 0:
                        gameState = END
                # if intersect with sheild
                for shield in shields:
                    if shield.destroyOnHit(invBull):
                        invBull[1] = screenHeight + 1
                if invBull[1] > screenHeight:
                    invBullets.remove(invBull)
            except:
                pass

        # UFO movement
        # after a minimum amount of time
        if UfoTimer >= UfoMinTime and not UfoMoving:
            if random.uniform(0,100) < UfoPercentChance: # on a random chance
                UfoX = screenWidth
                UfoMoving = True
                UfoLoopSnd.play(-1) # start the sound playing (and loop it)
        
        if UfoMoving:
            # start the UFO moving from the right side of the screen (off screen)
            # move towards the left
            UfoX -= UfoSpeed
            # check intersection with the player bullet
            if rectRectIntersect((pBulletX,pBulletY,bulletW,bulletH),(UfoX,UfoY,UfoHeight,UfoHeight)):
                score += 1000# if it hits give 1000 points
                UfoX = -1000 # destroy the UFO
                UfoTimer = 0# reset the timer
                UfoMoving = False
                invDeathSnd.play()# play the destrouyed sound
                UfoLoopSnd.stop()# stop the looped sound
            if UfoX + UfoHeight < 0:
                UfoX = -1000 # destroy the UFO
                UfoTimer = 0# reset the timer
                UfoMoving = False
                UfoLoopSnd.stop()# stop the looped sound

        # Drawing ------------------ 
    
        # Clear Screen
        screen.fill((0,0,10))

    if gameState == HIGHSCORE:
        if not scoreSaved:
            hScore.save(name, score)
            scoreSaved = True

    if gameState == PLAY:
        # Player

        if playerStart:
            if flashCount % 2 == 0:
                pygame.draw.rect(screen,pCol,(pX,pY,pWidth,pHeight))
            if flashCounter > flashTime:
                flashCount += 1
                flashCounter = 0
            if flashCount > numFlashes:
                flashCount = 0
                playerStart = False
        else:
            pygame.draw.rect(screen,pCol,(pX,pY,pWidth,pHeight))

        # Player Bullet
        pygame.draw.rect(screen,pBulletCol,(pBulletX,pBulletY,bulletW,bulletH))

        # Invader Bullets
        for bullet in invBullets:
            pygame.draw.rect(screen, invBulletCol, bullet)

        # Sheilds
        for shield in shields:
            shield.draw(screen)

        # Invaders
        allInvaders.draw(screen)

        # UFO
        # using the invader font, draw the correct character on screen
        UfoCharacter = UfoFont.render("1",True, (255,0,0))
        UfoRect = UfoCharacter.get_rect()
        UfoRect.topleft = (UfoX,UfoY)
        screen.blit(UfoCharacter, UfoRect)

        # Score
        scoreText = arcadeFontSmall.render("score " + str(score),True,menuFontColor)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topleft = (padding,padding)
        screen.blit(scoreText,scoreTextRect)

        # lives
        if numLives >= 1:
            pygame.draw.rect(screen,pCol,(screenWidth-pWidth/3-padding,padding,pWidth/3,pHeight/3))
        if numLives >= 2:
            pygame.draw.rect(screen,pCol,(screenWidth-pWidth/3*2-padding*2,padding,pWidth/3,pHeight/3))
        if numLives >= 3:
            pygame.draw.rect(screen,pCol,(screenWidth-pWidth/3*3-padding*3,padding,pWidth/3,pHeight/3))

    elif gameState == END:
        gameOverText = arcadeFont.render("GAME     OVER",True,menuFontColor)
        gameOverTextRect = gameOverText.get_rect()
        gameOverTextRect.center = (screenWidth//2,screenHeight//2 - 50)
        screen.blit(gameOverText, gameOverTextRect)
    elif gameState == VICTORY:
        gameOverText = arcadeFont.render("VICTORY       :)",True,menuFontColor)
        gameOverTextRect = gameOverText.get_rect()
        gameOverTextRect.center = (screenWidth//2,screenHeight//2 - 50)
        screen.blit(gameOverText, gameOverTextRect)
    elif gameState == NAMESCREEN:
        screen.fill((0,0,10))
        nameScreenText = arcadeFont.render("ENTER NAME",True,menuFontColor)
        nameScreenTextRect = nameScreenText.get_rect()
        nameScreenTextRect.center = (screenWidth//2,screenHeight//2 - 100)
        screen.blit(nameScreenText, nameScreenTextRect)
        nameText = arcadeFontSmall.render(name,True,menuFontColor)
        nameTextRect = nameText.get_rect()
        nameTextRect.center = (screenWidth//2,screenHeight//2 - 50)
        screen.blit(nameText, nameTextRect)
    elif gameState == HIGHSCORE:
        screen.fill((0,0,10))
        highScoreText = arcadeFont.render("HIGH SCORES",True,menuFontColor)
        highScoreTextRect = highScoreText.get_rect()
        highScoreTextRect.center = (screenWidth//2,screenHeight//2 - 100)
        screen.blit(highScoreText, highScoreTextRect)
        hScore.drawTop5(screen)
    
    tick = clock.tick(30) # time since last tick in Milliseconds (attempts to maintain 30FPS)
    timeCounter += tick
    flashCounter += tick
    UfoTimer += tick
    pygame.display.update()

pygame.quit()
quit()
#THE END :D