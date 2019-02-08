==Base game by syntdex, remix by Timothy Marpaung

==Requires the following modules to run:
pygame, random, configparser, os

==Minimum Required Layout
./Textures
	>name of head image (20x20px)
	>name of collectible image (30x30px)
./Languages
	>name of config file (ini)

==Backups: If the following files are missing, create them.
========CONFIG.ini==========
[dev]
enableDebug = False

[game]
locale = en_us
frameRate = 30
windowSizeX = 800
windowSizeY = 600
collectibleSize = 30
playerSize = 20
systemfont = comicsansms

[player-color]
red	= 80
green	= 160
blue	= 30

[bg-color]
automatic	=True
red	= 70
green	= 70
blue	= 70

[player-body]
; Draws a gradient rectangle behind the trailing body
; (0 = False, 1 = Modified Player color, 2 = Average, 3 = user defined)
drawPlayerShadow = 1
red	= 255
green	= 25
blue	= 25

[textures]
enableHeadTexture = False
enableCollectibleTexture = False
headTextureName = head.png
iconTextureName = head.png
collectibleTextureName = collectible.png
drawCircleBehindCollectibleTexture= True

========"./Languages/en_us.ini"=========
[name]
gameName = Beam
language = English

[strings_common]
controls = [C] Play/Continue, [Q] Quit, [U] Reload Config, [P] Check Colors
score = Score: 

[strings_pause]
pause_title = Paused

[strings_title]
title_intro = Welcome to Beam
title_desc_one = The objective of the game is to collect the energy balls
title_desc_two = More energy = Longer light
title_desc_three = If you run into your beam, or the edges, you die!
current_color = Currently selected color: 
color_warning = <- outside of acceptable color range

[strings_gameover]
gameover = Game Over

[color-preview]
copr_name = Color Preview
copr_body = Current Color
copr_shadow = Shadow Color
copr_bg = Background Color
copr_preview = Preview