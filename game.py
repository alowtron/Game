print("Importing modules...")
import pygame
import sys
import random
import math

def runGame():
    declareVars()
    initGame()
    generateTerrain()
    mainStep()

def declareVars():
    print("Declaring variables...")
    global screenWidth, screenHeight, scaleHeight
    screenWidth = 1200 
    screenHeight = 800 
    scaleHeight = screenHeight

    print("Creating player variables...")
    global playerPosition , playerSize, playerSpeed, playerMaxHealth, playerCurrentHealth, playerHealFrequency
    playerPosition = [screenWidth // 2, screenHeight // 2]
    playerSize = 20
    playerSpeed = 5
    playerMaxHealth = 500
    playerCurrentHealth = playerMaxHealth
    playerHealFrequency = 100
    global playerBasicAttack
    playerBasicAttack = {
        'list': [],
        'size': 5,
        'speed': 20,
        'color': (0, 255, 0),
        'frequency': 60,
        'damage': 10
    }

    print("Creating enemies variables...")
    global enemiesList, enemySize, enemySpeed
    enemiesList = []
    enemySize = 20
    enemySpeed = 2
    global enemy1SpawnFrequency, enemy1DamageAmount, enemy1Health, enemy1Speed, enemy1Size
    enemy1SpawnFrequency = 240
    enemy1DamageAmount = 1
    enemy1Health = 100
    enemy1Speed = 2
    enemy1Size = 20

    print("Creating colors...")
    global playerColor, enemyColor, backgroundColor, wallColor
    playerColor = (0, 0, 255)
    enemyColor = (255, 0, 0)
    backgroundColor = (122, 122, 122)
    wallColor = (255, 255, 255)

    print("Creating terrain variables...")
    global terrainArray, terrainSize, terrainFrequency, terrainDuration
    terrainArray = []
    terrainSize = 40
    terrainFrequency = 360
    terrainDuration = 3600

    print("Creating time variables...")
    global frameCount
    frameCount = 0

def initGame():
    print("Initializing game...")
    pygame.init()  
    global fakeScreen
    global screen
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.SCALED | pygame.RESIZABLE )
    fakeScreen = screen.copy()
    pygame.display.set_caption("Circle vs Squares")
    
def generateTerrain():
    print("Generating terrain...")
    x = random.randint(0, screenWidth - terrainSize)
    y = random.randint(0, screenHeight - terrainSize)
    terrainArray.append(pygame.Rect(x, y, terrainSize, terrainSize))
    if len(terrainArray) >= terrainDuration / terrainFrequency:
        terrainArray.pop(0)
    
def mainStep():
    global frameCount, playerCurrentHealth
    running = True
    clock = pygame.time.Clock()
    while running == True:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False        
        playerMovement()
        moveEnemies()
        if frameCount % terrainFrequency == 0:
            generateTerrain()
        if frameCount % enemy1SpawnFrequency == 0:
            generateEnemy(1)
        if frameCount % playerHealFrequency == 0:
            playerCurrentHealth += 1
        if frameCount % playerBasicAttack['frequency'] == 0:
            usePlayerBasicAttack()
        updatePlayerBasicAttackProjectile()
        drawGameFrame()
        playerDamage()
        frameCount += 1
        print(frameCount)
        clock.tick(60)
            
    quitGame()

def playerMovement():
    global playerPosition
    print("Moving Player...")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerPosition[0] -= playerSpeed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerPosition[0] += playerSpeed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        playerPosition[1] -= playerSpeed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        playerPosition[1] += playerSpeed

    # Keeps player in playing area  
    playerPosition[0] = max(playerSize, min(screenWidth - playerSize, playerPosition[0]))
    playerPosition[1] = max(playerSize, min(screenHeight - playerSize, playerPosition[1]))

def moveEnemies():
    print("Moving Enemies...")
    for enemy in enemiesList:
        # Calculate direction vector
        dx = playerPosition[0] - enemy['rect'].centerx
        dy = playerPosition[1] - enemy['rect'].centery
        distance = math.hypot(dx, dy)
        
        # Normalize direction
        if distance != 0:
            dx, dy = dx / distance, dy / distance
        
        # Add some randomness to movement
        dx += random.uniform(-0.2, 0.2)
        dy += random.uniform(-0.2, 0.2)
        
        # Determine speed (closer enemies move faster)
        speed = enemy['speed'] * (1 + (screenWidth - distance) / screenWidth)
        
        # Move enemy
        enemy['rect'].x += dx * speed
        enemy['rect'].y += dy * speed
        
        # Keep enemy within screen bounds
        enemy['rect'].clamp_ip(screen.get_rect())
        
        # Check for collision with other enemies
        for other_enemy in enemiesList:
            if other_enemy != enemy and enemy['rect'].colliderect(other_enemy['rect']):
                # Move away from colliding enemy
                overlap = enemy['rect'].clip(other_enemy['rect'])
                if overlap.width < overlap.height:
                    enemy['rect'].x += overlap.width * (-1 if enemy['rect'].x < other_enemy['rect'].x else 1)
                else:
                    enemy['rect'].y += overlap.height * (-1 if enemy['rect'].y < other_enemy['rect'].y else 1)

def generateEnemy(enemyNumber):
    print("Generating enemy...")
    
    # x, y, size, size, speed,
    if enemyNumber == 1:
        x = random.randint(0, screenWidth - enemy1Size)
        y = random.randint(0, screenHeight - enemy1Size)
        newEnemy = {
            'rect': pygame.Rect(x, y, enemy1Size, enemy1Size),
            'speed': enemy1Speed,
            'health': enemy1Health,
            'maxHealth': enemy1Health,
            'size': enemy1Size,
            'damage': enemy1DamageAmount,
            'number': 1
        }
        enemiesList.append(newEnemy)

def usePlayerBasicAttack():
    global playerBasicAttack
    nearestEnemy = min(enemiesList, key=lambda e: math.hypot(e['rect'].centerx - playerPosition[0], e['rect'].centery - playerPosition[1]))
    # Calculate direction vector
    dx = nearestEnemy['rect'].centerx - playerPosition[0]
    dy = nearestEnemy['rect'].centery - playerPosition[1]
    distance = math.hypot(dx, dy)
    # Normalize direction
    if distance != 0:
        dx = dx / distance
        dy = dy / distance
    # Create Projectile
    projectile = {
        'position': playerPosition.copy(),
        'direction': (dx, dy)
    }
    playerBasicAttack['list'].append(projectile)

def updatePlayerBasicAttackProjectile():
    global playerBasicAttack, enemiesList
    for projectile in playerBasicAttack['list']:
        # Move projectile
        projectile['position'][0] += projectile['direction'][0] * playerBasicAttack['speed']
        projectile['position'][1] += projectile['direction'][1] * playerBasicAttack['speed']
        # Check if projectile is out of bounds
        if (projectile['position'][0] < 0 or projectile['position'][0] > screenWidth or
            projectile['position'][1] < 0 or projectile['position'][1] > screenHeight):
            playerBasicAttack['list'].remove(projectile)
            continue
        # Check for collision with enemies
        projectileRect = pygame.Rect(projectile['position'][0] - playerBasicAttack['size'], projectile['position'][1] - playerBasicAttack['size'], playerBasicAttack['size'] * 2, playerBasicAttack['size'] * 2)
        for enemy in enemiesList:
            if projectileRect.colliderect(enemy['rect']):
                enemy['health'] -= playerBasicAttack['damage']
                if enemy['health'] <= 0:
                    enemiesList.remove(enemy)
                playerBasicAttack['list'].remove(projectile)
                break

def drawGameFrame():
    print("Drawing frame...")
    # Sets background color
    screen.fill(backgroundColor)
    global player
    for terrain in terrainArray:
        pygame.draw.rect(screen, wallColor, terrain)
    for enemy in enemiesList:
        pygame.draw.rect(screen, enemyColor, enemy['rect'])
        drawEnemyHealthBar(enemy)
    player = pygame.draw.circle(screen, playerColor, playerPosition, playerSize)
    # Draw health bar
    bar_width = 200
    bar_height = 20
    bar_x = (screen.get_width() - bar_width) // 2
    bar_y = screen.get_height() - bar_height - 10
    # Background of health bar
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    # Calculate health percentage
    health_percentage = playerCurrentHealth / playerMaxHealth
    health_width = int(bar_width * health_percentage)
    # Foreground of health bar
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
    # Optional: Add a border to the health bar
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
    # Draw Projectiles from playerBasicAttack
    for projectile in playerBasicAttack['list']:
        pygame.draw.circle(screen, playerBasicAttack['color'], [int(projectile['position'][0]), int(projectile['position'][1])], playerBasicAttack['size'])
    pygame.display.flip()

def playerDamage():
    global playerCurrentHealth
    player_rect = pygame.Rect(playerPosition[0] - playerSize, playerPosition[1] - playerSize, playerSize * 2, playerSize * 2)
    for enemy in enemiesList:
        if player_rect.colliderect(enemy['rect']):
            playerCurrentHealth -= enemy['damage']
            print(f"Player hit! Current health: {playerCurrentHealth}")
            if playerCurrentHealth <= 0:
                print("Game Over!")
                quitGame()

def quitGame():
    pygame.quit()
    sys.exit()

def drawEnemyHealthBar(enemy):
    barWidth = enemy['size']
    barHeight = 5
    barX = enemy['rect'].x
    barY = enemy['rect'].y - 10
    # Background of health bar
    pygame.draw.rect(screen, (150, 150, 150), (barX, barY, barWidth, barHeight))
    # Calculate health percentage
    healthPercentage = enemy['health'] / enemy['maxHealth']
    healthWidth = int(barWidth * healthPercentage)
    # Foreground of health bar
    pygame.draw.rect(screen, (255, 150, 0), (barX, barY, healthWidth, barHeight))
    # Health bar border
    # pygame.draw.rect(screen, (0, 0, 0), (barX, barY, barWidth, barHeight), 1)


runGame()