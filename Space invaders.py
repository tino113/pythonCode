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

# Invaders
pygame.font.init()
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                moveDir = 0
    
    # Player Movement
    pX += moveDir

    # Invaders Movment
    if timeCounter >= allInvaders.invTimer:
        timeCounter -= allInvaders.invTimer
        allInvaders.move()
    
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
        for shield in shields:
            if shield.destroyOnHit((pBulletX,pBulletY,bulletW,bulletH)):
                    pBulletY = -100
        
    # Invaders Bullet Movement
    invBullets += allInvaders.fireLastRow(invFireChance)
    for invBull in invBullets:
        try:
            invBull[1] += bulletSpeed
            # if intersect with player
            if rectRectIntersect(invBull,(pX,pY,pWidth,pHeight)):
                playerDeathSnd.play()
                pY = -1000
                invBull[1] = screenHeight + 1
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

    # Player
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
    
    timeCounter += clock.tick(30) # time since last tick in Milliseconds (attempts to maintain 30FPS)
    pygame.display.update()

pygame.quit()
quit()
#THE END :D