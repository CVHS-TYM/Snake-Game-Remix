# Requires PYGAME to run
# Modules
import pygame
import random
import configparser
import os

# Initialization
config = configparser.ConfigParser()
pygame.init()

def limit_value(limit_min,limit_max,value):
    if value < limit_min:
        value = limit_min
    elif value > limit_max:
        value = limit_max
    return value

def game_over():
    global gameOver
    gameOver = True

def average_color(valueOne,valueTwo):
    output = ((valueOne**2 + valueTwo**2)*0.5)**0.5
    return output

def grayscale(redValue, greenValue, blueValue,style='weight'):
    RGBLinear = (float(redValue),
                 float(greenValue),
                 float(blueValue))
    weight = (0.2126,
              0.7152,
              0.0722)
    simpleCalc = (RGBLinear[0]+RGBLinear[1]+RGBLinear[2])/3
    if style == 'weight':
        output = (RGBLinear[0]*weight[0],
                  RGBLinear[1]*weight[1],
                  RGBLinear[2]*weight[2])
    elif style == 'simple':
        output = (simpleCalc,simpleCalc,simpleCalc)
    return output

class enter_directory():
    def __init__(self,directory):
        self.directory = directory
        self.inFolder = False
    def __enter__(self):
        if os.path.exists(self.directory):
            os.chdir(self.directory)
            self.inFolder = True
##            print("Directory reverted successfully %s" % os.getcwd())
    def __exit__(self, type, value, traceback):
        if self.inFolder:
            os.chdir("..")
##            print("Directory reverted successfully %s" % os.getcwd())

def modifyColor(color_tuple, method, valueA=0, valueB=0, valueC=0):
    if method == "invert":
        outputA = 255 - color_tuple[0]
        outputB = 255 - color_tuple[1]
        outputC = 255 - color_tuple[2]
    elif method == "light":
        outputA = color_tuple[0] + valueA
        outputB = color_tuple[1] + valueB
        outputC = color_tuple[2] + valueC
    else:
        outputA = 0
        outputB = 0
        outputC = 0
    return limit_value(0, 255, outputA), limit_value(0, 255, outputB), limit_value(0, 255, outputC)

def update_textures(headName, collectName, iconTextureName):
    global imageHead
    global imageCollectible
    global imageIcon

    with(enter_directory("./Textures")):
        imageHead = pygame.image.load(headName)
        imageCollectible = pygame.image.load(collectName)
        pygame.display.set_icon(pygame.image.load(iconTextureName))

def update_locale(languageCode):
    global string_gameName
    global string_language
    global string_controls
    global string_score
    global string_pause
    global string_titleIntro
    global string_titleDescOne
    global string_titleDescTwo
    global string_titleDescThree
    global string_currentColor
    global string_colorWarning
    global string_gameOver
    global string_coprName
    global string_coprBody
    global string_coprShadow
    global string_coprBackground
    global string_coprPreview

    with(enter_directory("./Languages")):
        config.read_file(open('%s.ini' % languageCode))
        string_gameName = config.get('name', 'gameName')
        string_language = config.get('name', 'language')
        string_controls = config.get('strings_common', 'controls')
        string_score = config.get('strings_common', 'score')
        string_pause = config.get('strings_pause', 'pause_title')
        string_titleIntro = config.get('strings_title', 'title_intro')
        string_titleDescOne = config.get('strings_title', 'title_desc_one')
        string_titleDescTwo = config.get('strings_title', 'title_desc_two')
        string_titleDescThree = config.get('strings_title', 'title_desc_three')
        string_currentColor = config.get('strings_title', 'current_color')
        string_colorWarning = config.get('strings_title', 'color_warning')
        string_gameOver = config.get('strings_gameover', 'gameover')
        string_coprName = config.get('color-preview', 'copr_name')
        string_coprBody = config.get('color-preview', 'copr_body')
        string_coprShadow = config.get('color-preview', 'copr_shadow')
        string_coprBackground = config.get('color-preview', 'copr_bg')
        string_coprPreview = config.get('color-preview', 'copr_preview')

def update_config():
    config.read_file(open(r'CONFIG.ini'))
    languageCode = config.get('game', 'locale')
    #dev
    global enableDebug
    debug_drawPlayerShadowComment = ""
    #game
    global windowSize
    global frameRate
    global collectibleSize
    global playerSize
    global gameFont
    #player color
    global playerColor
    global playerColorFixed
    
    global backgroundColor
    
    global drawPlayerShadow
    global drawPlayerShadowColor
    #internal usage
    global averageColorPlayerBackground
    global customRedColor
    global customGreyColor
    #textures
    global enableHeadTexture
    global enableCollectibleTexture
    global headTextureName
    global collectibleTextureName
    global iconTextureName
    global drawCircleBehindCollectibleTexture
    
    enableDebug = config.getboolean('dev', 'enableDebug')
    enableHeadTexture = config.getboolean('textures', 'enableHeadTexture')
    enableCollectibleTexture = config.getboolean('textures', 'enableCollectibleTexture')
    headTextureName = config.get('textures', 'headTextureName')
    collectibleTextureName = config.get('textures', 'collectibleTextureName')
    iconTextureName = config.get('textures', 'iconTextureName')
    drawCircleBehindCollectibleTexture = config.getboolean('textures', 'drawCircleBehindCollectibleTexture')

    windowSize = (int(config.get('game', 'windowSizeX')),
                  int(config.get('game', 'windowSizeY')))
    frameRate = int(config.get('game', 'frameRate'))
    collectibleSize = int(config.get('game', 'collectibleSize'))
    playerSize = int(config.get('game', 'playerSize'))
    gameFont = config.get('game', 'systemfont')
    
    playerColor = (int(config.get('player-color', 'red')),
                   int(config.get('player-color', 'green')),
                   int(config.get('player-color', 'blue')))
    playerColorFixed = (limit_value(0, 255, playerColor[0]),
                        limit_value(0, 255, playerColor[1]),
                        limit_value(0, 255, playerColor[2]))

    
    if config.getboolean('bg-color', 'automatic'):
        backgroundColor = modifyColor(playerColorFixed, 'invert')
    else:
        backgroundColor = (int(config.get('bg-color', 'red')),
                           int(config.get('bg-color', 'green')),
                           int(config.get('bg-color', 'blue')))
    
    drawPlayerShadow = int(config.get('player-body', 'drawPlayerShadow'))
    averageColorPlayerBackground = (average_color(playerColorFixed[0],backgroundColor[0]),
                                    average_color(playerColorFixed[1],backgroundColor[1]),
                                    average_color(playerColorFixed[2],backgroundColor[2]))
    customRedColor = (255,
                      limit_value(0,255,(averageColorPlayerBackground[1]-30)),
                      limit_value(0,255,(averageColorPlayerBackground[2]-30)))
    customGreyColor = grayscale(playerColorFixed[0],
                                playerColorFixed[1],
                                playerColorFixed[2])
    
    if drawPlayerShadow == 1:
        debug_drawPlayerShadowComment = "Weaker Player Color"
        drawPlayerShadowColor = ((limit_value(0, 255, playerColorFixed[0] - 60)),
                                 (limit_value(0, 255, playerColorFixed[1] - 60)),
                                 (limit_value(0, 255, playerColorFixed[2] - 60)))
    
    elif drawPlayerShadow == 2:
        drawPlayerShadowColor = averageColorPlayerBackground
        debug_drawPlayerShadowComment = "Average Player Color"
    
    elif drawPlayerShadow == 3:
        debug_drawPlayerShadowComment = "User"
        drawPlayerShadowColor = (int(config.get('player-body', 'red')),
                                 int(config.get('player-body', 'green')),
                                 int(config.get('player-body', 'blue')))
    else:
        debug_drawPlayerShadowComment = "Disabled"
        drawPlayerShadow = 0
        drawPlayerShadowColor = (0,0,0)

    update_locale(languageCode)
    update_textures(headTextureName, collectibleTextureName, iconTextureName)
        
    if enableDebug:
        print("==READ FROM CONFIG== (RunTime: "+str(pygame.time.get_ticks()/1000)+")")
        print("Language Selected:",languageCode,":",string_language)
        print("|playerColor|: ",(playerColor))
        print("|playerColorFixed|: ",(playerColorFixed))
        print("|backgroundColor|: ",(config.getboolean('bg-color', 'automatic')),":",backgroundColor)
        print("|drawPlayerShadow|: "+debug_drawPlayerShadowComment+" : ",drawPlayerShadowColor)
        print("|Textures?|: Head=",enableHeadTexture," Collectible: ",enableCollectibleTexture)
    
update_config()


gameDisplay = pygame.display.set_mode(windowSize)
pygame.display.set_caption(string_gameName)

clock = pygame.time.Clock()

direction = "right"

smallfont = pygame.font.SysFont(gameFont, 25)
medfont = pygame.font.SysFont(gameFont, 50)
largefont = pygame.font.SysFont(gameFont, 80)


def quitGame():
    pygame.quit()
    quit()

def outlineText(msg, body_color, outline_color, y_displace=0, x_displace=0, size = "small"): #merge with message_to_screen eventually. IDK how to RN my eyes hurt
    size_val = 0
    offset_mult = 0
    if size == "small":
        offset_mult = 1
        size_val = 25
    elif size == "medium":
        offset_mult = 2.5
        size_val = 50
    elif size == "large":
        offset_mult = 3
        size_val = 80
    offset = [(-1, 1),
               (0, 1),
               (1, 1),
               (1, 0),
               (1, -1),
               (0, -1),
               (-1, -1),
               (-1, 0)]
    
    for i in range(0,7):
        message_to_screen(msg,
                          outline_color,
                          y_displace + offset[i][0]*offset_mult,
                          size,
                          x_displace + (offset[i][1]*offset_mult))
    message_to_screen(msg, body_color, y_displace, size, x_displace)

                          

def menuColors():
    menuOpen = True
    pygame.display.set_caption(string_gameName+' ('+string_coprName+')')

    while menuOpen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    menuOpen = False
                elif event.key == pygame.K_q:
                    quitGame()
                elif event.key == pygame.K_u:
                    update_config()

        gameDisplay.fill(grayscale(backgroundColor[0],
                                   backgroundColor[1],
                                   backgroundColor[2]))
        outlineText(string_coprName,
                    customGreyColor,
                    (0, 0, 0),
                    -250,
                    0,
                    "large")
        outlineText(string_coprBody,
                    playerColorFixed,
                    customGreyColor,
                    -190,
                    0,
                    "medium")
        pygame.draw.rect(gameDisplay, playerColorFixed,
                         (0,
                         int(windowSize[1]/2-160),
                         int(windowSize[0]),
                         30))
        message_to_screen(str(playerColorFixed),
                          modifyColor(playerColorFixed, 'invert'),
                          -145)

        outlineText(string_coprShadow,
                    drawPlayerShadowColor,
                    modifyColor(drawPlayerShadowColor, 'light', -30, -30, -30),
                    -100,
                    0,
                    "medium")
        pygame.draw.rect(gameDisplay, drawPlayerShadowColor,
                         (0,
                         int(windowSize[1]/2-70),
                         int(windowSize[0]),
                         30))
        message_to_screen(str(drawPlayerShadowColor),
                          modifyColor(drawPlayerShadowColor, 'invert'),
                          -55)
        
        outlineText(string_coprBackground,
                    backgroundColor,
                    customGreyColor,
                    -10,
                    0,
                    "medium")
        pygame.draw.rect(gameDisplay, backgroundColor,
                         (0,
                         int(windowSize[1]/2+30),
                         int(windowSize[0]),
                         30))
        message_to_screen(str(backgroundColor),
                          modifyColor(backgroundColor, 'invert'),
                          45)

        outlineText(string_currentColor,
                    playerColorFixed,
                    customGreyColor,
                    90,
                    0,
                    "medium")
        pygame.draw.rect(gameDisplay, playerColorFixed,
                         (0,
                         int(windowSize[1]/2+130),
                         int(windowSize[0]),
                         30))
        message_to_screen(str(playerColorFixed),
                          modifyColor(playerColorFixed, 'invert'),
                          145)

        outlineText(string_controls,
                    playerColorFixed,
                    customGreyColor,
                    260,
                    0)
##      PREVIEW DISABLED BC I DONT HAVE TIME TO ADD IT
##        outlineText(string_coprPreview,
##                    playerColorFixed,
##                    modifyColor(playerColorFixed, 'invert'),
##                    190,
##                    0,
##                    "medium")
        pygame.display.update()
        clock.tick(5)


def pause(playerLength):
    isGamePaused = True
    pygame.display.set_caption(string_gameName+' ('+string_pause+')')
    
    while isGamePaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    isGamePaused = False
                elif event.key == pygame.K_q:
                    quitGame()
                elif event.key == pygame.K_u:
                    update_config()
                elif event.key == pygame.K_p:
                    menuColors()
                    
        gameDisplay.fill(backgroundColor)
        outlineText(string_pause,
                    playerColorFixed,
                    customGreyColor,
                    -50,
                    size = "large")
        outlineText(string_score+str(playerLength - 3),
                    playerColorFixed,
                    customGreyColor,
                    50,
                    size = 'medium')
        outlineText(string_controls,
                    playerColorFixed,
                    customGreyColor,
                    260)
        pygame.display.update()
        clock.tick(5)
    if not isGamePaused:
        pygame.display.set_caption(string_gameName)


def draw_score(score):
##    textScore = smallfont.render(string_score + str(score),
##                                 True,
##                                 customGreyColor)
    textScore = smallfont.render(string_score + str(score),
                                 True,
                                 modifyColor(customGreyColor, 'light', -70, -70, -70))
##    outlineText(string_score + str(score),
##                customGreyColor,
##                modifyColor(customGreyColor, 'light', -70, -70, -70),
##                -(windowSize[0]/2),
##                -(windowSize[1]/2))
                   
    gameDisplay.blit(textScore, [0,0])

def rand_collectible_gen(playerList): #Added code to disallow collectible spawning inside the player body. Still some very slight edge cases, but good enough,
    collectibleRandomX = round(random.randrange(0, windowSize[0] - collectibleSize))
    collectibleRandomY = round(random.randrange(0, windowSize[1] - collectibleSize))
    #Goes through each part of the player
    for eachPart in playerList:
        while ( #X part
            (collectibleRandomX > eachPart[0] and
             collectibleRandomX < eachPart[0] + collectibleSize) or
            (collectibleRandomX + collectibleSize > eachPart[0] and
             collectibleRandomX + collectibleSize < eachPart[0] + collectibleSize)
            ) and ( #Y part
            (collectibleRandomY > eachPart[1] and
             collectibleRandomY < eachPart[1] + collectibleSize) or
            (collectibleRandomY + collectibleSize > eachPart[1] and
             collectibleRandomY + collectibleSize < eachPart[1] + collectibleSize)):
            # If the collectible coincides with any part of the player, keep respawning it until it isnt,
            if enableDebug:
                print("DEBUG: collectible in player. Respawning. \n")
            collectibleRandomX = round(random.randrange(0, int(windowSize[0] - collectibleSize)))
            collectibleRandomY = round(random.randrange(0, int(windowSize[1] - collectibleSize)))
    return collectibleRandomX, collectibleRandomY

                       
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    quitGame()
                elif event.key == pygame.K_u:
                    update_config()
                elif event.key == pygame.K_p:
                    menuColors()
                    
        gameDisplay.fill(backgroundColor)
        outlineText(string_language,
                    customGreyColor,
                    (0, 0, 0),
                    -280,
                    350,
                    "small")
        outlineText(string_titleIntro,
                    playerColorFixed,
                    modifyColor(playerColorFixed, 'light', -50, -50, -50),
                    -100,
                    0,
                    "large")
        outlineText(string_titleDescOne,
                    customGreyColor,
                    modifyColor(customGreyColor, 'light', -70, -70, -70),
                    -30)
        outlineText(string_titleDescTwo,
                    customGreyColor,
                    modifyColor(customGreyColor, 'light', -70, -70, -70),
                    10)
        outlineText(string_titleDescThree,
                    customGreyColor,
                    modifyColor(customGreyColor, 'light', -70, -70, -70),
                    50)
        outlineText(string_currentColor + str(playerColorFixed),
                    playerColorFixed,
                    modifyColor(customGreyColor, 'light', -70, -70, -70),
                    90)
        pygame.draw.rect(gameDisplay,
                         playerColorFixed,
                         (0,
                         int(windowSize[1]/2+120),
                         int(windowSize[0]),
                         30))
        playerColorOutOfBoundsWarning = False
        for each_val in playerColor:
            if each_val < 0 or each_val > 255:
                warning = True
        if playerColorOutOfBoundsWarning:
            message_to_screen(str(playerColor) + string_colorWarning,
            customRedColor,
            160,
            'small')
        outlineText(string_controls,
                    customGreyColor,
                    modifyColor(customGreyColor, 'darken', 20, 20, 20),
                    260)
        pygame.display.update()
        clock.tick(5)

def player(playerSize, playerlist, lastdir):
    global player_width_mod
    global player_height_mod

    pygame.draw.circle(gameDisplay,
                       playerColor,
                          [int(playerlist[-1][0] + (playerSize/2)),
                           int(playerlist[-1][1] + (playerSize/2))],
                       int(playerSize/2))

    if enableHeadTexture:
        if direction == "right":
            head = pygame.transform.rotate(imageHead, 270)

        elif direction == "left":
            head = pygame.transform.rotate(imageHead, 90)

        elif direction == "up":
            head = imageHead

        elif direction == "down":
            head = pygame.transform.rotate(imageHead, 180)

        gameDisplay.blit(head,
                         (playerlist[-1][0],
                          playerlist[-1][1]))

    if enableDebug: #Draw (x,y) of head
        pygame.draw.rect(gameDisplay,
                         (255, 0, 0),
                         (playerlist[-1][0],
                          playerlist[-1][1],
                          0,
                          0))

    for XnY in playerlist[:-1]:
        if XnY[2] in ['up','down']: #could probably be squashed TBH
            if XnY[2] == 'up':
                player_x_offset = 8
                player_y_offset = 12
            else:
                player_x_offset = 8
                player_y_offset = 8
            player_height_mod = len(playerlist)
            player_width_mod = playerlist.index(XnY)
        elif XnY[2] in ['left','right']:
            if XnY[2] == 'left':
                player_x_offset = 12
                player_y_offset = 8
            else:
                player_x_offset = 8
                player_y_offset = 8
            player_height_mod = playerlist.index(XnY)
            player_width_mod = len(playerlist)

        if (drawPlayerShadow > 0) and (drawPlayerShadow < 4):
            pygame.draw.rect(gameDisplay,
                             ((limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*drawPlayerShadowColor[0]))),
                              (limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*drawPlayerShadowColor[1]))),
                              (limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*drawPlayerShadowColor[2])))),
                             (XnY[0],XnY[1],playerSize,playerSize)
                             )
                               
        pygame.draw.rect(gameDisplay,
                         (
                             (limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*playerColorFixed[0]))),
                             (limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*playerColorFixed[1]))),
                             (limit_value(0, 255,(playerlist.index(XnY) / len(playerlist)*playerColorFixed[2])))
                         ),
                         [int(XnY[0] + playerSize/len(playerlist) -
                              (playerSize*player_width_mod / len(playerlist))/2)+player_x_offset,
                          int(XnY[1] + playerSize/len(playerlist) -
                              (playerSize*player_height_mod / len(playerlist))/2)+player_y_offset,
                              int(playerSize*player_width_mod / len(playerlist)),
                              int(playerSize*player_height_mod / len(playerlist))])
        if enableDebug: #Debugging true coords of body
            pygame.draw.rect(gameDisplay,
                             (255, 0, 0),
                             (XnY[0],
                              XnY[1],
                              0,
                              0)) #Red Pixel for XY position of each body
            pygame.draw.rect(gameDisplay,
                             (0, 155, 0),
                             [int((XnY[0] + 2) - (player_width_mod)/1),
                              int(XnY[1] + 20/len(playerlist) - (player_height_mod)/1),
                                  int(0),
                                  int(0)])
                            #https://stackoverflow.com/questions/12097033/python-index-error-value-not-in-list-on-indexvalue
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0,  size = "small", x_displace=0):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (windowSize[0]/2)+x_displace, (windowSize[1]/2)+y_displace
    gameDisplay.blit(textSurf,textRect)


def gameLoop():
    global direction
    global gameOver
    gameExit = False
    gameOver = False
    direction = "right"
    direction_pressed = False

    lead_x = windowSize[0]/2
    lead_y = windowSize[1]/2

    lead_x_change = 1
    lead_y_change = 0

    playerList = []
    playerLength = 3 #Increased player's length to three to look ok

    lastdir = direction

    collectibleRandomX,collectibleRandomY = rand_collectible_gen(playerList)

    while not gameExit:
        pygame.display.set_caption(string_gameName+' ('+string_gameName+')')
        while gameOver == True:
            pygame.display.set_caption(string_gameName+' ('+string_gameOver+')')
            gameDisplay.fill(backgroundColor)
            outlineText(string_gameOver,
                        customRedColor,
                        modifyColor(customRedColor, 'light', -80, -80, -80),
                        -50,
                        0,
                        'large')
            outlineText(string_score + str(playerLength - 3),
                        customGreyColor,
                        modifyColor(customGreyColor, 'light', -70, -70, -70),
                        50,
                        0,
                        "medium")
            outlineText(string_controls,
                        customGreyColor,
                        modifyColor(customGreyColor, 'light', -70, -70, -70),
                        260,
                        0)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_u:
                        update_config()
                    elif event.key == pygame.K_p:
                        menuColors()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True
            if event.type == pygame.KEYDOWN:
                #Added logic to prevent player from running directly into itself,
                #Also makes it like normal player.
                #Changed the lead_changes to +/-1 to make it easier to edit
                if direction_pressed == False: #To prevent the player from making two simultaneous inputs, which causes an instant suicide
                    if direction in ['up','down']: #!
                        if event.key == pygame.K_LEFT:
                            direction_pressed = True
                            direction = "left"
                            lead_x_change = -1
                            lead_y_change = 0
                        elif event.key == pygame.K_RIGHT:
                            direction_pressed = True
                            direction = "right"
                            lead_x_change = 1
                            lead_y_change = 0
                    elif direction in ['left','right']:#!
                        if event.key == pygame.K_UP: #elif -> if
                            direction_pressed = True
                            direction = "up"
                            lead_y_change = -1
                            lead_x_change = 0
                        elif event.key == pygame.K_DOWN:
                            direction_pressed = True
                            direction = "down"
                            lead_y_change = 1
                            lead_x_change = 0
                if event.key == pygame.K_p: #elif -> if
                      pause(playerLength)
                elif event.key == pygame.K_t:
                      game_intro()

        if (lead_x >= windowSize[0] or
            lead_x < 0 or
            lead_y >= windowSize[1] or
            lead_y < 0):
            game_over()

        #See lead_x_change lead_y_change section
        lead_x += (playerSize * lead_x_change)
        lead_y += (playerSize * lead_y_change)
        gameDisplay.fill(backgroundColor)

        if enableCollectibleTexture:
            if drawCircleBehindCollectibleTexture:
                pygame.draw.circle(gameDisplay,
                                   playerColor,
                                      [int(collectibleRandomX + (collectibleSize/2)),
                                       int(collectibleRandomY + (collectibleSize/2))],
                                   int(collectibleSize/2))
            gameDisplay.blit(imageCollectible,
                             (collectibleRandomX,
                              collectibleRandomY))
        else:
            pygame.draw.circle(gameDisplay,
                               playerColor,
                                  [int(collectibleRandomX + (collectibleSize/2)),
                                   int(collectibleRandomY + (collectibleSize/2))],
                               int(collectibleSize/2))

        playerHead = []
        playerHead.append(lead_x)
        playerHead.append(lead_y)
        playerHead.append(direction)
        #https://stackoverflow.com/questions/17911091/append-integer-to-beginning-of-list-in-pythons
        playerList.append(playerHead)
        direction_pressed = False

        if len(playerList) > playerLength:
            del playerList[0]

        for eachSegment in playerList[:-1]:
            if (eachSegment[0], eachSegment[1]) == (playerHead[0], playerHead[1]):
                game_over()
        player(playerSize,
              playerList,
              lastdir)

        draw_score(playerLength-3)
        pygame.display.update()

        if (lead_x > collectibleRandomX and
            lead_x < collectibleRandomX+collectibleSize) or (
                lead_x + playerSize > collectibleRandomX and lead_x+playerSize <
                collectibleRandomX + collectibleSize):

            if (lead_y > collectibleRandomY and lead_y < collectibleRandomY+collectibleSize):
                collectibleRandomX,collectibleRandomY = rand_collectible_gen(playerList)
                playerLength += 1
            elif (lead_y + playerSize > collectibleRandomY and lead_y + playerSize < collectibleRandomY + collectibleSize):
                collectibleRandomX,collectibleRandomY = rand_collectible_gen(playerList)
                playerLength += 1

        clock.tick(frameRate)
        
    quitGame()
game_intro()
gameLoop()
