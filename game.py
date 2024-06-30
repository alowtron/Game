print("Importing modules...")
import pygame
import sys
import random
import math
import copy 

def runGame():
    declareVars()
    initGame()
    generateTerrain()
    mainStep()

def declareVars():
    print("Declaring variables...")
    global screenWidth, screenHeight, scaleHeight, isPaused
    screenWidth = 1200 
    screenHeight = 800 
    scaleHeight = screenHeight
    isPaused = False

    print("Creating player variables...")
    global playerVars, playerCurrentHealth
    playerVars = {
        'position': [screenWidth // 2, screenHeight // 2],
        'size': 20,
        'speed': 5,
        'maxHealth': 500,
        'healFrequency': 100,
        'coins': 0 
    }
    playerCurrentHealth = playerVars['maxHealth']
    global upgrades, keyPrice, hasKey, baseStatUpgrades
    upgrades = {
        'basic attack damage': {'level': 1, 'price': 1, 'increment': 1},
        'basic attack frequency': {'level': 1, 'price': 10, 'increment': 1},
        'basic attack speed': {'level': 1, 'price': 10, 'increment': 1},
        'speed': {'level': 1, 'price': 10, 'increment': 0.1},
        'health': {'level': 1, 'price': 100, 'increment': 50}
    }
    baseStatUpgrades = copy.deepcopy(upgrades)
    keyPrice = 100
    hasKey = False

    global playerBasicAttack
    playerBasicAttack = {
        'list': [],
        'size': 5,
        'speed': 20,
        'color': (0, 255, 0),
        'frequency': 60,
        'damage': 20
    }

    print("Creating enemies variables...")
    global enemiesList, enemySize, enemySpeed
    enemiesList = []
    enemySize = 20
    enemySpeed = 2
    global enemy1
    enemy1 = {
        'spawnFrequency': 240,
        'damageAmount': 1,
        'health': 100,
        'speed': 2,
        'size': 20,
        'coinGiven': 1000
    }

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

def pauseMenu():
    global isPaused
    pauseFont = pygame.font.Font(None, 74)
    optionFont = pygame.font.Font(None, 50)
    
    pauseText = pauseFont.render("PAUSED", True, (255, 255, 255))
    resumeText = optionFont.render("Resume", True, (255, 255, 255))
    upgradesText = optionFont.render("Upgrades", True, (255, 255, 255))
    quitText = optionFont.render("Quit", True, (255, 255, 255))
    
    pauseRect = pauseText.get_rect(center=(screenWidth//2, screenHeight//2 - 100))
    resumeRect = resumeText.get_rect(center=(screenWidth//2, screenHeight//2 + 50))
    upgradesRect = upgradesText.get_rect(center=(screenWidth//2, screenHeight//2 + 120))
    quitRect = quitText.get_rect(center=(screenWidth//2, screenHeight//2 + 190))
    
    options = ["Resume", "Upgrades", "Quit"]
    selected = 0
    
    while isPaused:
        screen.fill(backgroundColor)
        screen.blit(pauseText, pauseRect)
        
        for i, option in enumerate([resumeText, upgradesText, quitText]):
            if i == selected:
                pygame.draw.rect(screen, (100, 100, 100), option.get_rect(center=(screenWidth//2, screenHeight//2 + 50 + i*70)).inflate(20, 10))
            screen.blit(option, option.get_rect(center=(screenWidth//2, screenHeight//2 + 50 + i*70)))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isPaused = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Resume
                        isPaused = False
                    elif selected == 1:  # Upgrades
                        handleUpgradeMenu()
                    elif selected == 2:  # Quit
                        quitGame()

def generateTerrain():
    print("Generating terrain...")
    x = random.randint(0, screenWidth - terrainSize)
    y = random.randint(0, screenHeight - terrainSize)
    terrainArray.append(pygame.Rect(x, y, terrainSize, terrainSize))
    if len(terrainArray) >= terrainDuration / terrainFrequency:
        terrainArray.pop(0)

def handleUpgradeMenu():
    global playerVars, upgrades, hasKey
    levelCap = 50
    # Create a list of available upgrade options (level <= levelCap) and is level 1 or higher (level 0 skills are not active yet) including Boss Key and Back
    upgradeOptions = [upgrade for upgrade, data in upgrades.items() if data['level'] <= levelCap and data['level'] >= 0] + ["Boss Key", "Back"]
    selected = 0  # Initialize the selected option
    
    while True:
        drawUpgradeMenu(selected, upgradeOptions)  # Pass upgradeOptions to drawUpgradeMenu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit the upgrade menu
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Move selection up, wrapping around to bottom if at top
                    selected = (selected - 1) % len(upgradeOptions)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Move selection down, wrapping around to top if at bottom
                    selected = (selected + 1) % len(upgradeOptions)
                elif event.key == pygame.K_RETURN:
                    if selected < len(upgradeOptions) - 2:  # -2 for Boss Key and Back options
                        # Handle upgrade selection
                        upgrade = upgradeOptions[selected]
                        if playerVars['coins'] >= upgrades[upgrade]['price']:

                            # Apply the upgrade
                            playerVars['coins'] -= upgrades[upgrade]['price']
                            upgrades[upgrade]['level'] += 1
                            if upgrade == 'basic attack damage':
                                playerBasicAttack['damage'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['basic attack damage']['price']
                                print(baseStatUpgrades)
                            elif upgrade == 'basic attack frequency':
                                playerBasicAttack['frequency'] -= upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['basic attack frequency']['price']
                            elif upgrade == 'basic attack speed':
                                playerBasicAttack['speed'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['basic attack speed']['price']
                            # elif upgrade == 'speed':

                            # Apply upgrade effects (damage, speed, health, etc.)
                            # ...
                            # upgrades[upgrade]['price'] *= 2  # Increase price for next upgrade
                            # If upgrade reached level 6, remove it from options
                            if upgrades[upgrade]['level'] > levelCap:
                                upgradeOptions.remove(upgrade)
                                selected = min(selected, len(upgradeOptions) - 1)
                    elif selected == len(upgradeOptions) - 2:  # Boss Key option
                        if not hasKey and playerVars['coins'] >= keyPrice:
                            playerVars['coins'] -= keyPrice
                            hasKey = True
                    else:  # Back option
                        return  # Exit the upgrade menu

def drawUpgradeMenu(selected, upgradeOptions):
    upgradeFont = pygame.font.Font(None, 36)
    screen.fill(backgroundColor)
    
    y = 100  # Starting y-position for drawing options
    # Draw upgrade options
    for i, upgrade in enumerate(upgradeOptions[:-2]):  # Exclude Boss Key and Back
        data = upgrades[upgrade]
        text = f"{upgrade.capitalize()}: Level {data['level']} - Cost: {data['price']} coins"
        textSurface = upgradeFont.render(text, True, (255, 255, 255))
        textRect = textSurface.get_rect(center=(screenWidth // 2, y))
        if i == selected:
            # Highlight the selected option
            pygame.draw.rect(screen, (100, 100, 100), textRect.inflate(20, 10))
        screen.blit(textSurface, textRect)
        y += 50  # Move down for next option
    
    # Draw Boss Key option
    keyText = f"Boss Key: {'Owned' if hasKey else f'Cost: {keyPrice} coins'}"
    keySurface = upgradeFont.render(keyText, True, (255, 255, 0))
    keyRect = keySurface.get_rect(center=(screenWidth // 2, y + 50))
    if selected == len(upgradeOptions) - 2:
        # Highlight if selected
        pygame.draw.rect(screen, (100, 100, 100), keyRect.inflate(20, 10))
    screen.blit(keySurface, keyRect)
    
    # Draw Back option
    backText = "Back"
    backSurface = upgradeFont.render(backText, True, (200, 200, 200))
    backRect = backSurface.get_rect(center=(screenWidth // 2, screenHeight - 50))
    if selected == len(upgradeOptions) - 1:
        # Highlight if selected
        pygame.draw.rect(screen, (100, 100, 100), backRect.inflate(20, 10))
    screen.blit(backSurface, backRect)
    
    pygame.display.flip()  # Update the display
def mainStep():
    global frameCount, playerCurrentHealth, isPaused
    running = True
    clock = pygame.time.Clock()
    while running == True:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isPaused = not isPaused
                    if isPaused:
                        pauseMenu()
                elif event.key == pygame.K_u:
                    handleUpgradeMenu()
                elif event.key == pygame.K_b and hasKey:
                    startBossFight()

        if not isPaused:                
            playerMovement()
            moveEnemies()
            if frameCount % terrainFrequency == 0:
                generateTerrain()
            if frameCount % enemy1['spawnFrequency'] == 0:
                generateEnemy(1)
            if frameCount % playerVars['healFrequency'] == 0 and playerCurrentHealth < playerVars['maxHealth']:
                playerCurrentHealth += 1
            if len(enemiesList) != 0:
                if frameCount % playerBasicAttack['frequency'] == 0:
                    usePlayerBasicAttack()
            updatePlayerBasicAttackProjectile()
            drawGameFrame()
            playerDamage()
            frameCount += 1
            print(frameCount)
        clock.tick(60)
            
    quitGame()

def startBossFight():
    global hasKey
    if hasKey:
        print("Starting boss fight!")
        # Add boss fight logic here
        hasKey = False
    else:
        print("You need a key to start the boss fight!")

def playerMovement():
    global playerVars
    print("Moving Player...")
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerVars['position'][0] -= playerVars['speed']
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerVars['position'][0] += playerVars['speed']
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        playerVars['position'][1] -= playerVars['speed']
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        playerVars['position'][1] += playerVars['speed']

    # Keeps player in playing area  
    playerVars['position'][0] = max(playerVars['size'], min(screenWidth - playerVars['size'], playerVars['position'][0]))
    playerVars['position'][1] = max(playerVars['size'], min(screenHeight - playerVars['size'], playerVars['position'][1]))

def moveEnemies():
    print("Moving Enemies...")
    for enemy in enemiesList:
        # Calculate direction vector
        dx = playerVars['position'][0] - enemy['rect'].centerx
        dy = playerVars['position'][1] - enemy['rect'].centery
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
    minSpawnDistance = 200
    # x, y, size, size, speed,
    if enemyNumber == 1:
        # Finds a place to spawn the enemy that is not to close to the player
        while True:
            x = random.randint(0, screenWidth - enemy1['size'])
            y = random.randint(0, screenHeight - enemy1['size'])
            distance = math.hypot(x - playerVars['position'][0], y - playerVars['position'][1])
            if distance >= minSpawnDistance:
                break
        newEnemy = {
            'rect': pygame.Rect(x, y, enemy1['size'], enemy1['size']),
            'speed': enemy1['speed'],
            'health': enemy1['health'],
            'maxHealth': enemy1['health'],
            'size': enemy1['size'],
            'damage': enemy1['damageAmount'],
            'number': 1,
            'coinGiven': enemy1['coinGiven']
        }
        enemiesList.append(newEnemy)

def usePlayerBasicAttack():
    global playerBasicAttack
    nearestEnemy = min(enemiesList, key=lambda e: math.hypot(e['rect'].centerx - playerVars['position'][0], e['rect'].centery - playerVars['position'][1]))
    # Calculate direction vector
    dx = nearestEnemy['rect'].centerx - playerVars['position'][0]
    dy = nearestEnemy['rect'].centery - playerVars['position'][1]
    distance = math.hypot(dx, dy)
    # Normalize direction
    if distance != 0:
        dx = dx / distance
        dy = dy / distance
    # Create Projectile
    projectile = {
        'position': playerVars['position'].copy(),
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
                    # Add coins to player for kill then remove the enemy
                    playerVars['coins'] += enemy['coinGiven']
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
    player = pygame.draw.circle(screen, playerColor, playerVars['position'], playerVars['size'])
    # Draw health bar
    bar_width = 200
    bar_height = 20
    bar_x = (screen.get_width() - bar_width) // 2
    bar_y = screen.get_height() - bar_height - 10
    # Background of health bar
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    # Calculate health percentage
    health_percentage = playerCurrentHealth / playerVars['maxHealth']
    health_width = int(bar_width * health_percentage)
    # Foreground of health bar
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
    # Optional: Add a border to the health bar
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
    # Draw coins amount
    font = pygame.font.Font(None, 36)
    coinText = font.render(f"Coins: {playerVars['coins']}", True, (255, 255, 255))
    screen.blit(coinText, (10, 10))
    # Draw Projectiles from playerBasicAttack
    for projectile in playerBasicAttack['list']:
        pygame.draw.circle(screen, playerBasicAttack['color'], [int(projectile['position'][0]), int(projectile['position'][1])], playerBasicAttack['size'])
    
    pygame.display.flip()

def playerDamage():
    global playerCurrentHealth
    player_rect = pygame.Rect(playerVars['position'][0] - playerVars['size'], playerVars['position'][1] - playerVars['size'], playerVars['size'] * 2, playerVars['size'] * 2)
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