import pygame, random

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width,height))
screen.fill((0,0,0))

#font
pygame.font.init()
invaderHeight = 32
invaderFont = pygame.font.Font("pixel-invaders.ttf",invaderHeight)

invadersX = []
invadersY = []
invadersF = []
rows = 5
columns = 10
xSpc = width // (rows *3)
ySpc = xSpc
for y in range(rows):
    for x in range(columns):
        invadersX.append(x*xSpc+xSpc)
        invadersY.append(y*ySpc+ySpc)
        invadersF.append(random.choice(['a','b','c','d','e','f','g','h','i']))

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
    
    for i in range(len(invadersX)):
        col = (0,255,0)
        #pygame.draw.rect(screen, col, (invadersX[i],invadersY[i],20,20))
        invaderCharacter = invaderFont.render(invadersF[i],True,col)
        invaderRect = invaderCharacter.get_rect()
        invaderRect.topleft = (invadersX[i],invadersY[i])
        screen.blit(invaderCharacter, invaderRect)

    pygame.display.update()
pygame.quit()
quit()