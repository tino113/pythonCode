import pygame, random

pygame.init()
screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill((0,0,0))

#font
pygame.font.init()
invaderHeight = 32
invaderFont = pygame.font.Font("PyGames/Invaders.ttf",invaderHeight)

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
playerSpeed = 4
pCol = (0,255,0)

# Bullets
bulletW = 10
bulletH = 30
bulletSpeed = 4
bulletCol = (255,0,0)

# Player Bullet
pBulletX = -100
pBulletY = -100

# Invader Bullets
invBullets = []

# Shields
shields = []
shieldW = 150
shieldH = 80
numShields = 4
shieldSpace = screenWidth // (numShields + 1)
sheildY = screenHeight - shieldH - pHeight - padding * 2
for s in range(numShields):
    shields.append((Multiblock(shieldSpace,sheildY,shieldW,shieldH,nx=shieldW//10,ny=shieldH//10 )))

# Invaders
invaderCol = (0,255,0)
invadersX = []
invadersY = []
invadersF = []
invRows = 5
invCols = 10
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

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
    
    # interactivity ------------



    # Drawing ------------------ 

    # Player
    pygame.draw.rect(screen,pCol,(pX,pY,pWidth,pHeight))

    # Player Bullet
    pygame.draw.rect(screen,bulletCol,(pBulletX,pBulletY,bulletW,bulletH))

    # Invader Bullets
    for bullet in invBullets:
        pygame.draw.rect(screen, bulletCol,bullet)

    # Sheilds
    for shield in shields:
        shield.draw(screen)

    # Invaders
    for i in range(len(invadersX)):
        invaderCharacter = invaderFont.render(invadersF[i],True,invaderCol)
        invaderRect = invaderCharacter.get_rect()
        invaderRect.topleft = (invadersX[i],invadersY[i])
        screen.blit(invaderCharacter, invaderRect)

    pygame.display.update()
pygame.quit()
quit()
