import pygame, random

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
ufoLowSnd = pygame.mixer.Sound("ufo_lowpitch.wav")
ufoHighSnd = pygame.mixer.Sound("ufo_highpitch.wav")
ufoSnds = [ufoLowSnd,ufoHighSnd]
#spaceship = pygame.mixer.Sound("")


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
numFlashes = 12
flashTime = 100
flashCount = 0
playerStart = True

# Bullets
bulletW = 3
bulletH = 11
bulletSpeed = 8

# Player Bullet
pBulletX = -100
pBulletY = -100
pBulletCol = (0,0,255)

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
PLAY, END, HIGHSCORE = 0, 1, 2 
gameState = PLAY
score = 0
invaderScore = 100

# UFO
ufoMinTime = 10000
ufoMaxTime = 1000000
ufoChance = 0.001
ufoAlive = False
class UFO():
    def __init__(self, width = 40,height = 30, col = (255,255,255), speed = 4, score = 1000, font = "invaders.ttf"):
        self.w, self.h = width, height
        self.x, self.y = screenWidth + self.w, padding
        self.c = col
        self.font = pygame.font.Font(font,self.h)
        self.f = random.choice(["1","2"])
        self.speed = speed
        self.score = score
        self.sound = random.choice(ufoSnds)
    def move(self):
        self.x -= self.speed
    def hitRect(self,r):
        return rectRectIntersect((r[0],r[1],r[2],r[3]),(self.x,self.y,self.w, self.h))
    def draw(self, surf):
        ufoCharacter = self.font.render(self.f,True,self.c)
        ufoRect = ufoCharacter.get_rect()
        ufoRect.topleft = (self.x,self.y)
        surf.blit(ufoCharacter, ufoRect)

# Invaders
class Invader():
    def __init__(self, x, y, w, h, f, col):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.f = f
        self.c = col
    def hitRect(self,r):
        return rectRectIntersect((r[0],r[1],r[2],r[3]),(self.x,self.y,self.w, self.h))
    def draw(self, surf, font):
        invaderCharacter = font.render(self.f,True,self.c)
        invaderRect = invaderCharacter.get_rect()
        invaderRect.topleft = (self.x,self.y)
        surf.blit(invaderCharacter, invaderRect)

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
        xSpc = screenWidth // (self.invRows *3)
        ySpc = xSpc
        for y in range(self.invRows):
            for x in range(self.invCols):
                self.invaders.append(Invader(x*xSpc+xSpc,y*ySpc+ySpc,self.invaderWidth,self.invaderHeight,random.choice(['a','b','c','d','e','z','g','h','i']),self.invaderCol))
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

clock = pygame.time.Clock()
gameOver = False
moveDir = 0
playerFire = False
timeCounter = 0
ufoCounter = 0
flashCounter = 0
allInvaders = Invaders(5,10,invWidth=30,invHeight=30)
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
            if event.key == pygame.K_LEFTBRACKET:
                allInvaders.invTimer *= 1.1
            if event.key == pygame.K_RIGHTBRACKET:
                allInvaders.invTimer *= 0.9
            if event.key == pygame.K_BACKSLASH:
                allInvaders.invaders.remove(random.choice(allInvaders.invaders))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                moveDir = 0
    
    # deal with play state
    if gameState == PLAY:
        # Player Movement
        pX += moveDir

        # Invaders Movment
        if timeCounter >= allInvaders.invTimer:
            timeCounter -= allInvaders.invTimer
            allInvaders.move()
            
            #Check if invader intersect player
            for inv in allInvaders.invaders:
                if rectRectIntersect((inv.x,inv.y,inv.h,inv.w),(pX,pY,pWidth,pHeight)):
                        playerDeathSnd.play()
                        gameState = END

        #Check if invader intersect shield
        for inv in allInvaders.invaders:
            for shield in shields:
                if shield.destroyOnHit((inv.x,inv.y,inv.h,inv.w)):
                    pass

        # generate UFO randomly
        if ((ufoCounter > ufoMinTime and random.uniform(0,1) < ufoChance) or ufoCounter > ufoMaxTime) and not ufoAlive:
            ufo = UFO()
            ufo.sound.play(-1) # play on repeat
            ufoAlive = True
            ufoCounter = 0
        # UFO movement
        if ufoAlive:
            ufo.move()
            if ufo.x < 0 - ufo.w:
                ufoAlive = False
                ufo.sound.stop()
                ufo = None
        
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
                score += invaderScore
            for shield in shields:
                if shield.destroyOnHit((pBulletX,pBulletY,bulletW,bulletH)):
                    pBulletY = -100
            if ufoAlive:
                if ufo.hitRect((pBulletX,pBulletY,bulletW,bulletH)):
                    pBulletY = -100
                    score += ufo.score
                    ufo.sound.stop() # stop playing the UFO sound
                    ufo = None
                    ufoAlive = False
            
        # Invaders Bullet Movement
        invBullets += allInvaders.fireLastRow(invFireChance)
        for invBull in invBullets:
            try:
                invBull[1] += bulletSpeed
                # if intersect with player
                if rectRectIntersect(invBull,(pX,pY,pWidth,pHeight)) and not playerStart:
                    playerDeathSnd.play()
                    numLives -= 1
                    playerStart = True
                    #pY = -1000
                    pX = screenWidth//2-pWidth//2
                    invBull[1] = screenHeight + 1
                    if numLives <= 0:
                        gameState = END
                # if intersect with sheild
                for shield in shields:
                    if shield.destroyOnHit(invBull):
                        invBull[1] = screenHeight + 1
                if invBull[1] > screenHeight:
                    invBullets.remove(invBull)
            except:
                pass

        # Drawing ------------------ 
    
        # Clear Screen
        screen.fill((0,0,10))

    if gameState == PLAY:
        # Player
        if playerStart and flashCount < numFlashes:
            if flashCount % 2 == 0:
                pygame.draw.rect(screen,pCol,(pX,pY,pWidth,pHeight))
            if flashCounter > flashTime:
                flashCounter = 0
                flashCount += 1
        elif flashCount >= numFlashes:
            playerStart = False
            flashCount = 0
        if not playerStart:
            pygame.draw.rect(screen,pCol,(pX,pY,pWidth,pHeight))

        # playerLives
        if numLives >= 1:
            pygame.draw.rect(screen,pCol,(screenWidth-padding-pWidth/3,padding,pWidth/3,pHeight/3))
        if numLives >= 2:
            pygame.draw.rect(screen,pCol,(screenWidth-padding*1.5-pWidth/3*2,padding,pWidth/3,pHeight/3))
        if numLives >= 3:
            pygame.draw.rect(screen,pCol,(screenWidth-padding*2-pWidth/3*3,padding,pWidth/3,pHeight/3))

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
        if ufoAlive:
            ufo.draw(screen)

        # Scores
        scoreText = arcadeFontSmall.render("SCORE " + str(score),True,menuFontColor)
        scoreRect = scoreText.get_rect()
        scoreRect.topleft = (padding,padding)
        screen.blit(scoreText,scoreRect)

    elif gameState == END:
        gameOverText = arcadeFont.render("GAME     OVER",True,menuFontColor)
        gameOverTextRect = gameOverText.get_rect()
        gameOverTextRect.center = (screenWidth//2,screenHeight//2 - 50)
        screen.blit(gameOverText, gameOverTextRect)
    
    tick = clock.tick(30)
    timeCounter += tick # time since last tick in Milliseconds (attempts to maintain 30FPS)
    ufoCounter += tick
    flashCounter += tick
    pygame.display.update()

pygame.quit()
quit()
#THE END :D