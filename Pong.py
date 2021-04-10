import pygame, random
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG (Hot Potato)")
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255,230,0)
red = (255,0,0)
p1Score = 0
p2Score = 0
scoreFont = pygame.font.SysFont("Arial.ttf", 24)
p1Width = 30
p1Height = 200
p1PosY = height/2-p1Height/2
p1PosX = 0
p1VelY = 0

p2Width = 30
p2Height = 200
p2PosY = height/2-p1Height/2
p2PosX = width - p2Width
p2VelY = 0

ballWidth = 20
ballHeight = 20
ballPosX = width/2 - ballWidth/2
ballPosY = height/2 - ballHeight/2
ballVelX = random.choice ([-1, 1]) * random.randint(6, 12)
ballVelY = random.choice ([-1, 1]) * random.randint(6, 12)

clock =  pygame.time.Clock()
gameOver = False 
while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1VelY = -10
            if event.key == pygame.K_s:
                p1VelY =  10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                p1VelY = 0
            if event.key == pygame.K_s:
                p1VelY =  0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p2VelY = -10
            if event.key == pygame.K_DOWN:
                p2VelY =  10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                p2VelY = 0
            if event.key == pygame.K_DOWN:
                p2VelY =  0
    
    if p1PosY < 0 :
        p1PosY = 0

    if p1PosY + p1Height > height :
        p1PosY = height - p1Height

    if p2PosY < 0 :
        p2PosY = 0

    if p2PosY + p2Height > height :
        p2PosY = height - p2Height

    #ball 
    if ballPosY < 0 :
        ballVelY *= -1
    if ballPosY > height :
        ballVelY *= -1
    if ballPosX > width :
        p1Score += 10
        ballPosX = width/2 - ballWidth/2
        ballPosY = height/2 - ballHeight/2
        ballVelX = random.choice ([-1, 1]) * random.randint(6, 12)        
        ballVelY = random.choice ([-1, 1]) * random.randint(6, 12)
    if ballPosX + ballWidth < 0 :
        p2Score += 10
        ballPosX = width/2 - ballWidth/2
        ballPosY = height/2 - ballHeight/2
        ballVelX = random.choice ([-1, 1]) * random.randint(6, 12)
        ballVelY = random.choice ([-1, 1]) * random.randint(6, 12)

    if ballPosX < p1PosX + p1Width and ballPosY > p1PosY and ballPosY < p1PosY + p1Height :
        ballVelX *= -1 

    if ballPosX + ballWidth > p2PosX and ballPosY > p2PosY and ballPosY < p2PosY + p2Height :
        ballVelX *= -1 


    
    screen.fill(black)
    pygame.draw.rect(
        screen, white, (p1PosX, p1PosY, p1Width, p1Height))        
    pygame.draw.rect(
        screen, white, (p2PosX, p2PosY, p2Width, p2Height))        
    p1PosY = p1PosY + p1VelY
    p2PosY = p2PosY + p2VelY
    ballPosX = ballPosX + ballVelX
    ballPosY = ballPosY + ballVelY
    pygame.draw.rect(
        screen, yellow, (ballPosX, ballPosY,ballWidth, ballHeight))

    score1 = scoreFont.render("Score1: " + str (p1Score), True, red) 
    screen.blit(score1,(20,20))  
    score2 = scoreFont.render("Score2: " + str (p2Score), True, red) 
    score2Rect = score2.get_rect()
    screen.blit(score2,(width - 20 - score2Rect.width,20))  
    pygame.display.update()
    
    clock.tick(60)
pygame.quit()
quit()