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
        'healFrequency': 101,
        'coins': 0 
    }
    playerCurrentHealth = playerVars['maxHealth']
    global upgrades, keyPrice, hasKey, baseStatUpgrades
    upgrades = {
        'basic attack damage': {'level': 1, 'price': 1, 'increment': 1},
        'basic attack frequency': {'level': 1, 'price': 10, 'increment': 1},
        # 'basic attack speed': {'level': 1, 'price': 10, 'increment': 0.1},
        # goes to level 2 when active
        'all direction attack': {'level': 1, 'price': 50, 'increment': 0},
        'all direction attack damage': {'level': 0, 'price': 10, 'increment': 0.1},
        'all direction attack projectile number': {'level': 0, 'price': 10, 'increment': 12},
        'all direction attack frequency': {'level': 0, 'price': 100, 'increment': 7},

        'aoe attack': {'level': 1, 'price': 50, 'increment': 0},
        'aoe attack damage': {'level': 0, 'price': 10, 'increment': 0.5},
        'aoe attack frequency': {'level': 0, 'price': 100, 'increment': 2},
        'aoe attack radius': {'level': 0, 'price': 20, 'increment': 5},
        
        'speed': {'level': 1, 'price': 10, 'increment': 0.1},
        'health': {'level': 1, 'price': 100, 'increment': 50},
        'heal frequency': {'level': 1, 'price': 5, 'increment': 2}
    }
    baseStatUpgrades = copy.deepcopy(upgrades)
    keyPrice = 100
    hasKey = False

    global playerBasicAttack, playerAllDirectionAttack, playerAoeAttack
    playerBasicAttack = {
        'list': [],
        'size': 5,
        'speed': 20,
        'color': (0, 255, 0),
        'frequency': 60,
        'damage': 20
    }
    playerAllDirectionAttack = {
        'list': [],
        'size': 2,
        'speed': 10,
        'color': (0, 255, 0),
        'frequency': 360,
        'damage': 5,
        'projectile amount': 4
    }
    playerAoeAttack = {
        'active': False,
        'damage': 10,
        'frequency': 120,
        'radius': 50,
        'color': (0, 255, 255)  # Cyan color
    }

    print("Creating enemies variables...")
    global enemiesList, enemySize, enemySpeed, damagingZones
    enemiesList = []
    enemySize = 20
    enemySpeed = 2
    damagingZones = []
    global enemy1, enemy2, enemy3, boss100
    enemy1 = {
        'spawnFrequency': 240,
        'damageAmount': 1,
        'health': 100,
        'speed': 2,
        'size': 20,
        'coinGiven': 5 # 10000 for testing
    }

    # summoner
    enemy2 = {
        'spawnFrequency': 1800,  # How often the summoner appears
        'summonFrequency': 300,  # How often it summons minions
        'damageAmount': 2,
        'health': 500,
        'speed': 1,
        'size': 30,
        'coinGiven': 25
    }

    # Tank
    enemy3 = {
    'spawnFrequency': 1200,  # Spawns less frequently than other enemies
    'damageAmount': 3,
    'health': 800,
    'speed': 1,  # Slower than other enemies
    'size': 35,  # Larger than regular enemies
    'coinGiven': 20
}

    boss100 = {
        'damageAmount': 5,
        'health': 1000,
        'speed': 2,
        'size': 40,
        'coinGiven': 2000
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
    global playerVars, upgrades, hasKey, isPaused, playerCurrentHealth
    levelCap = 50
    # Create a list of available upgrade options (level <= levelCap) and is level 1 or higher (level 0 skills are not active yet) including Boss Key and Back
    
    
    selected = 0  # Initialize the selected option
    
    while True:
        upgradeOptions = [upgrade for upgrade, data in upgrades.items() if data['level'] <= levelCap and data['level'] > 0] + ["Boss Key", "Back"]
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
                            elif upgrade == 'all direction attack':
                                upgrades['all direction attack']['level'] += 50
                                upgrades['all direction attack damage']['level'] += 1
                                upgrades['all direction attack projectile number']['level'] += 1
                                upgrades['all direction attack frequency']['level'] += 1
                                # upgradeOptions = [upgrade for upgrade, data in upgrades.items() if data['level'] <= levelCap and data['level'] > 0] + ["Boss Key", "Back"]
                            elif upgrade == 'all direction attack damage':
                                playerAllDirectionAttack['damage'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['all direction attack damage']['price']
                            elif upgrade == 'all direction attack projectile number':
                                playerAllDirectionAttack['projectile amount'] += 1
                                upgrades[upgrade]['price'] += baseStatUpgrades['all direction attack damage']['price']
                            elif upgrade == 'all direction attack frequency':
                                playerAllDirectionAttack['frequency'] -= upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['all direction attack frequency']['price']
                            elif upgrade == 'aoe attack':
                                playerAoeAttack['active'] = True
                                upgrades['aoe attack']['level'] += 50
                                upgrades['aoe attack damage']['level'] += 1
                                upgrades['aoe attack frequency']['level'] += 1
                                upgrades['aoe attack radius']['level'] += 1
                            elif upgrade == 'aoe attack damage':
                                playerAoeAttack['damage'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['aoe attack damage']['price']
                            elif upgrade == 'aoe attack frequency':
                                playerAoeAttack['frequency'] -= upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['aoe attack frequency']['price']
                            elif upgrade == 'aoe attack radius':
                                playerAoeAttack['radius'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['aoe attack radius']['price']
                            elif upgrade == 'speed':
                                playerVars['speed'] += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['speed']['price']
                            elif upgrade == 'health':
                                playerVars['maxHealth'] += upgrades[upgrade]['increment']
                                playerCurrentHealth += upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['speed']['price']
                            elif upgrade == 'heal frequency':
                                playerVars['healFrequency'] -= upgrades[upgrade]['increment']
                                upgrades[upgrade]['price'] += baseStatUpgrades['heal frequency']['price']
                            if upgrades[upgrade]['level'] > levelCap:
                                upgradeOptions.remove(upgrade)
                                selected = min(selected, len(upgradeOptions) - 1)
                    elif selected == len(upgradeOptions) - 2:  # Boss Key option
                        if not hasKey and playerVars['coins'] >= keyPrice:
                            playerVars['coins'] -= keyPrice
                            hasKey = True
                            enemiesList.clear()
                            generateEnemy(100)
                    else:  # Back option
                        # isPaused = not isPaused
                        #pauseMenu()  # Exit the upgrade menu
                        return

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
    global frameCount, playerCurrentHealth, isPaused, hasKey
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
            print(len(enemiesList))
            print(hasKey)
            if hasKey == True and len(enemiesList) == 0:
                hasKey = False
            if frameCount % terrainFrequency == 0:
                generateTerrain()
            if frameCount % enemy1['spawnFrequency'] == 0 and hasKey == False:
                generateEnemy(1)
                #TODO: Temp code
                if enemy1['spawnFrequency'] > 1:
                    enemy1['spawnFrequency'] -= 1
            if frameCount % enemy2['spawnFrequency'] == 0 and hasKey == False and frameCount >= 5400:
                generateEnemy(2)
                if enemy2['spawnFrequency'] > 1:
                    enemy2['spawnFrequency'] -= 1
            if frameCount % enemy3['spawnFrequency'] == 0 and hasKey == False and frameCount >= 18000:
                generateEnemy(3)
                if enemy3['spawnFrequency'] > 1:
                    enemy3['spawnFrequency'] -= 1
            if frameCount % playerAoeAttack['frequency'] == 0 and playerAoeAttack['active']:
                usePlayerAoeAttack()
            if frameCount % playerVars['healFrequency'] == 0 and playerCurrentHealth < playerVars['maxHealth']:
                playerCurrentHealth += 1
            if len(enemiesList) != 0:
                if frameCount % playerBasicAttack['frequency'] == 0:
                    usePlayerBasicAttack()
            if frameCount % playerAllDirectionAttack['frequency'] == 0 and upgrades['all direction attack']['level'] >= 2:
                usePlayerAllDirectionAttack()
            for enemy in enemiesList:
                if enemy['number'] == 2 and frameCount - enemy['lastSummonTime'] >= enemy2['summonFrequency']:
                    summonMinions(enemy)
                    enemy['lastSummonTime'] = frameCount
            updatePlayerBasicAttackProjectile()
            updatePlayerAllDirectionAttackProjectile()
            manageDamagingZones()
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
    
    # Generate spawn position for all enemy types
    while True:
        x = random.randint(0, screenWidth - enemy1['size'])
        y = random.randint(0, screenHeight - enemy1['size'])
        distance = math.hypot(x - playerVars['position'][0], y - playerVars['position'][1])
        if distance >= minSpawnDistance:
            break

    if enemyNumber == 1:
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
    elif enemyNumber == 2:  # enemy2 (summoner)
        newEnemy = {
            'rect': pygame.Rect(x, y, enemy2['size'], enemy2['size']),
            'speed': enemy2['speed'],
            'health': enemy2['health'],
            'maxHealth': enemy2['health'],
            'size': enemy2['size'],
            'damage': enemy2['damageAmount'],
            'number': 2,
            'coinGiven': enemy2['coinGiven'],
            'lastSummonTime': frameCount
        }
    
    elif enemyNumber == 3:  # Tank enemy
        newEnemy = {
            'rect': pygame.Rect(x, y, enemy3['size'], enemy3['size']),
            'speed': enemy3['speed'],
            'health': enemy3['health'],
            'maxHealth': enemy3['health'],
            'size': enemy3['size'],
            'damage': enemy3['damageAmount'],
            'number': 3,
            'coinGiven': enemy3['coinGiven']
        }

    elif enemyNumber == 100:
        newEnemy = {
            'rect': pygame.Rect(x, y, boss100['size'], boss100['size']),
            'speed': boss100['speed'],
            'health': boss100['health'],
            'maxHealth': boss100['health'],
            'size': boss100['size'],
            'damage': boss100['damageAmount'],
            'number': 100,
            'coinGiven': boss100['coinGiven']
        }
    
    enemiesList.append(newEnemy)

def usePlayerAoeAttack():
    global enemiesList, playerVars, playerAoeAttack
    for enemy in enemiesList[:]:
        distance = math.hypot(enemy['rect'].centerx - playerVars['position'][0],
                              enemy['rect'].centery - playerVars['position'][1])
        if distance <= playerAoeAttack['radius']:
            enemy['health'] -= playerAoeAttack['damage']
            if enemy['health'] <= 0:
                playerVars['coins'] += enemy['coinGiven']
                enemiesList.remove(enemy)

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

def usePlayerAllDirectionAttack():
    global playerAllDirectionAttack
    angles = [i * (360 / playerAllDirectionAttack['projectile amount']) for i in range(playerAllDirectionAttack['projectile amount'])]
    for angle in angles:
        dx = math.cos(math.radians(angle))
        dy = math.sin(math.radians(angle))
        projectile = {
            'position': playerVars['position'].copy(),
            'direction': (dx, dy)
        }
        playerAllDirectionAttack['list'].append(projectile)

def summonMinions(summoner_enemy):
    for _ in range(3):  # Summon 3 minions
        x = summoner_enemy['rect'].centerx + random.randint(-50, 50)
        y = summoner_enemy['rect'].centery + random.randint(-50, 50)
        minion = {
            'rect': pygame.Rect(x, y, enemy1['size'] // 2, enemy1['size'] // 2),
            'speed': enemy1['speed'] * 1.5,
            'health': enemy1['health'] // 4,
            'maxHealth': enemy1['health'] // 2,
            'size': enemy1['size'] // 2,
            'damage': enemy1['damageAmount'],
            'number': 1,
            'coinGiven': 2
        }
        enemiesList.append(minion)

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

def updatePlayerAllDirectionAttackProjectile():
    global playerAllDirectionAttack, enemiesList
    for projectile in playerAllDirectionAttack['list']:
        # Move projectile
        projectile['position'][0] += projectile['direction'][0] * playerAllDirectionAttack['speed']
        projectile['position'][1] += projectile['direction'][1] * playerAllDirectionAttack['speed']
        # Check if projectile is out of bounds
        if (projectile['position'][0] < 0 or projectile['position'][0] > screenWidth or
            projectile['position'][1] < 0 or projectile['position'][1] > screenHeight):
            playerAllDirectionAttack['list'].remove(projectile)
            continue
        # Check for collision with enemies
        projectileRect = pygame.Rect(projectile['position'][0] - playerAllDirectionAttack['size'], projectile['position'][1] - playerAllDirectionAttack['size'], playerAllDirectionAttack['size'] * 2, playerAllDirectionAttack['size'] * 2)
        for enemy in enemiesList:
            if projectileRect.colliderect(enemy['rect']):
                enemy['health'] -= playerAllDirectionAttack['damage']
                if enemy['health'] <= 0:
                    # Add coins to player for kill then remove the enemy
                    playerVars['coins'] += enemy['coinGiven']
                    enemiesList.remove(enemy)
                playerAllDirectionAttack['list'].remove(projectile)
                break

def manageDamagingZones():
    global damagingZones, playerCurrentHealth
    
    # Create new damaging zone if boss 100 exists
    for enemy in enemiesList:
        if enemy['number'] == 100 and random.random() < 0.09:  # 10% chance per frame
            newZone = {
                'position': [random.randint(0, screenWidth), random.randint(0, screenHeight)],
                'radius': 10,
                'max_radius': 100,
                'growth_rate': 0.5,
                'damage': 1,
                'color': (255, 0, 0, 128)  # Red with some transparency
            }
            damagingZones.append(newZone)
    
    # Update existing zones
    for zone in damagingZones[:]:
        zone['radius'] += zone['growth_rate']
        if zone['radius'] >= zone['max_radius']:
            damagingZones.remove(zone)
        else:
            # Check if player is inside the zone
            distance = math.hypot(playerVars['position'][0] - zone['position'][0],
                                  playerVars['position'][1] - zone['position'][1])
            if distance < zone['radius'] + playerVars['size']:
                playerCurrentHealth -= zone['damage']
                print(f"Player in damaging zone! Current health: {playerCurrentHealth}")
                if playerCurrentHealth <= 0:
                    print("Game Over!")
                    quitGame()

def drawGameFrame():
    print("Drawing frame...")
    # Sets background color
    screen.fill(backgroundColor)
    global player
    for terrain in terrainArray:
        pygame.draw.rect(screen, wallColor, terrain)
    for enemy in enemiesList:
        if enemy['number'] == 2:  # Summoner
            pygame.draw.rect(screen, (255, 0, 255), enemy['rect'])  # Purple color for summoner
        elif enemy['size'] < enemy1['size']:  # Minion
            pygame.draw.rect(screen, (255, 165, 0), enemy['rect'])  # Orange color for minions
        elif enemy['number'] == 3:  # Tank enemy
            pygame.draw.rect(screen, (0, 128, 128), enemy['rect'])  # Teal color for tank enemy
        else:
            pygame.draw.rect(screen, enemyColor, enemy['rect'])
        drawEnemyHealthBar(enemy)
    # Draw damaging zones
    for zone in damagingZones:
        pygame.draw.circle(screen, zone['color'], 
                           (int(zone['position'][0]), int(zone['position'][1])), 
                           int(zone['radius']))
    # Draw Playeraaaaaaa
    player = pygame.draw.circle(screen, playerColor, playerVars['position'], playerVars['size'])
    if playerAoeAttack['active']:
        pygame.draw.circle(screen, playerAoeAttack['color'], 
                       (int(playerVars['position'][0]), int(playerVars['position'][1])), 
                       int(playerAoeAttack['radius']), 2)
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
    # Draw projectiles from playerAllDirectionAttack
    for projectile in playerAllDirectionAttack['list']:
        pygame.draw.circle(screen, playerAllDirectionAttack['color'], [int(projectile['position'][0]), int(projectile['position'][1])], playerAllDirectionAttack['size'])
    
    pygame.display.flip()

def playerDamage():
    global playerCurrentHealth
    player_rect = pygame.Rect(playerVars['position'][0] - playerVars['size'], playerVars['position'][1] - playerVars['size'], playerVars['size'] * 2, playerVars['size'] * 2)
    for enemy in enemiesList:
        if player_rect.colliderect(enemy['rect']):
            damage = enemy.get('damage', 0)  # Use 0 as default if 'damage' key doesn't exist
            playerCurrentHealth -= damage
            print(f"Player hit by enemy type {enemy['number']}! Damage: {damage}, Current health: {playerCurrentHealth}")
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