import pygame, random

pygame.init()
screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill((0,0,0))

# audio
'''
pygame.mixer.init()
fireSound = pygame.mixer.Sound("")
invDeath = pygame.mixer.Sound("")
invMove1 = pygame.mixer.Sound("")
invMove2 = pygame.mixer.Sound("")
invMove3 = pygame.mixer.Sound("")
invMove4 = pygame.mixer.Sound("")
invMoveSnds = [invMove1,invMove2,invMove3,invMove4]
spaceship = pygame.mixer.Sound("")
'''

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

    def checkHit(self, other):
        for block in self.blocks:
            pass
        return False
    
    def destroyOnHit():
        pass

# Game Variables
# General
padding = 20

# Player
pWidth = 80
pHeight = 40
pX = screenWidth//2 - pWidth//2
pY = screenHeight - pHeight - padding
playerSpeed = 10
pCol = (0,255,0)

# Bullets
bulletW = 3
bulletH = 11
bulletSpeed = 4


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
    shields.append(Multiblock(shieldSpace,sheildY,shieldW,shieldH,nx=shieldW//10,ny=shieldH//10 ))

# Invaders
invaderHeight = 32
invaderWidth = int(invaderHeight)
invaderCol = (0,255,0)
invTimer = 1000# how many milliseconds before they move

#font
pygame.font.init()
invaderFont = pygame.font.Font("pixel-invaders.ttf",invaderHeight)

# layout invaders
invadersX = []
invadersY = []
invadersF = []
invRows = 5
invCols = 10
invDir = 1
xSpc = screenWidth // (invRows *3)
ySpc = xSpc
for y in range(invRows):
    for x in range(invCols):
        invadersX.append(x*xSpc+xSpc)
        invadersY.append(y*ySpc+ySpc)
        invadersF.append(random.choice(['a','b','c','d','e','z','g','h','i']))

lastRow = []
cols = []
for i in range(len(invadersX)):
    found = False
    for col in cols:
        if invadersX[i] == invadersX[col[0]]:
            col.append(i)
            found = True
    if not found:
        cols.append([i])

for col in cols:
    lastRow.append(col[-1])

clock = pygame.time.Clock()
gameOver = False
moveDir = 0
playerFire = False
timeCounter = 0
while not gameOver:
    # interactivity ------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveDir = -playerSpeed
            if event.key == pygame.K_RIGHT:
                moveDir = playerSpeed
            if event.key == pygame.K_SPACE:
                playerFire = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moveDir = 0
    
    # Player Movement
    pX += moveDir

    # Invaders Movment
    if timeCounter >= invTimer:
        timeCounter -= invTimer
        for i in range(len(invadersX)):
            invadersX[i] += invaderWidth * invDir
        for i in range(len(invadersX)):
            if invadersX[i] >= screenWidth or invadersX[i] <= 0:
                invDir *= -1
                invTimer *= 0.90 # 10% faster
                for i in range(len(invadersY)):
                    invadersY[i] += invaderHeight
                    invadersX[i] += invaderWidth * invDir
                break
    # Bullets
    # Player Bullet Movement
    if playerFire and pBulletY < -bulletH:
        pBulletX = pX + pWidth // 2 - bulletW // 2
        pBulletY = pY - bulletH
        playerFire = False
    
    if pBulletY > -bulletH:
        pBulletY -= bulletSpeed

    # Invaders Bullet Movement
    for lRInv in lastRow:
        if random.uniform(0,100) < invFireChance:
            invBullets.append([invadersX[lRInv]+invaderWidth//4,invadersY[lRInv] + invaderHeight//2,  bulletW,bulletH])

    for invBull in invBullets:
        try:
            invBull[1] += bulletSpeed
            # if intersect with player
            # TODO: make intersection code
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
        pygame.draw.rect(screen, invBulletCol,bullet)

    # Sheilds
    for shield in shields:
        shield.draw(screen)

    # Invaders
    for i in range(len(invadersX)):
        invaderCharacter = invaderFont.render(invadersF[i],True,invaderCol)
        invaderRect = invaderCharacter.get_rect()
        invaderRect.topleft = (invadersX[i],invadersY[i])
        screen.blit(invaderCharacter, invaderRect)

    
    timeCounter += clock.tick(30) # time since last tick in Milliseconds (attempts to maintain 30FPS)
    pygame.display.update()
pygame.quit()
quit()
#THE END :D