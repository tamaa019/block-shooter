import pygame
from pygame.locals import *
import random
import requests
import sys

pygame.init()
pygame.font.init()
text = "Play"
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

clock = pygame.time.Clock()
text_color1 = pygame.Color("white")
text_color0 = pygame.Color("cyan")
myfont = pygame.font.SysFont("Arial" , 40)
width , height = 640 , 480
screen = pygame.display.set_mode((width , height))
running = True
pygame.display.set_caption("Block shooter")
button_pos = [50 , 20]
playerpos = [0 , 1]
player = pygame.image.load("img/player.png").convert()
explosion = pygame.image.load("img/explosion.png").convert()
#explosion = pygame.transform.scale(explosion , (80 , 80))
player = pygame.transform.scale(player , (40 , 40))
color = pygame.Color("white")
animation_timer = 10
play_text = myfont.render(text , True , text_color0)
enemy_img = pygame.image.load("img/enemy.png").convert()
enemy_img = pygame.transform.scale(enemy_img , (40 , 40))
arrow_img = ["img/bullet.png" , "img/bullet2.png"]
#arrow_animation_index = 0
gameover_img = pygame.image.load("img/gameover.png").convert()
#arrow = pygame.transform.scale(arrow , (42 , 10))
choice = 1
player_animation_index = 0
player_animation_img = ["img/player.png" , "img/player_shoot.png"]
arrow_pos = []
bounce = False
game_running = True
scores = 0
explosions = []
grass = pygame.image.load("img/grass.png").convert()
exit_text = myfont.render("Exit" , True , text_color1)
enemy_timer = 100
enemies = [[width , 100]]
#index = 0
touched = False
target_score = 1500
score = 50
pygame.mixer.init()

explode_sound = pygame.mixer.Sound("audio/sound_001.wav")
explode_sound.set_volume(0.05)
hit_sound = pygame.mixer.Sound("audio/sound_001.wav")
hit_sound.set_volume(0.05)
fire_sound = pygame.mixer.Sound("audio/sound_008.wav")
fire_sound.set_volume(0.05)

def gamewin():
	global game_running
	game_running = False
	while running:
		game_win = pygame.image.load("img/win.png").convert()
		pygame.display.flip()

		screen.blit(game_win , (0 , 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					main_menu()

def gameover():
	global game_running
	game_running = False
	while running:
		
		screen.blit(gameover_img ,(0 , 0))
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


keys = {"top" : False , "bottom" : False , "right" : False , "left" : False , "fire" : False , "pause" : False}


def pause_game():
	screen.fill(0)

	

def game():
	global score
	global scores
	global enemy_timer
	global animation_timer
	global playerpos
	global arrow_pos
	global enemies
	global index
	global player_animation_index
	global player_animation_img
	global explosions
	global touched
	global game_running
	game_running = True
	while game_running:

		if keys["pause"]:
			pause_game()
		#print(index)
		#if index == len(enemies)-1:
		#	index = 0
		if score == 0:
			gameover()
			break
		if scores >= target_score:
			gamewin()
			break
		arrow = pygame.image.load(arrow_img[random.randint(0 , 1)])
		arrow = pygame.transform.scale(arrow , (42 , 30))
	#screen.fill(0)
		#text = myfont.render(text_[random.randint(0 , len(text_)) - 1] , False , (0 , 0 , 0 , 0))
		player = pygame.image.load(player_animation_img[player_animation_index]).convert()
		player = pygame.transform.scale(player , (40 , 40))
		text = myfont.render("Lives : {}".format(score) , False , (255 , 255 , 255 , 255))
		text_score = myfont.render("Score : {}/{}".format(scores , target_score) , False, pygame.Color("white"))

		for x in range(int(width/grass.get_width()+1)):
			for y in range(int(height/grass.get_height()+1)):
				screen.blit(grass, (x*100, y*100))
		
		screen.blit(player , playerpos)
		enemy_timer -= 1
		if enemy_timer == 0:
			enemies.append([width , random.randint(50 , height-32)])
			enemy_timer = 20

		
		screen.blit(text ,(0 , 1))
		screen.blit(text_score , (0 , 41))



		for enemy in enemies:
			enemy[0] -= 5
			if enemy[0] < -64:
				index1 = enemies.index(enemy)

				enemies.pop(index1)
				#ndex = index + 1
				#score -= 5
		arrow_index = 0
		for enemy in enemies:
			screen.blit(enemy_img , enemy)
			#screen.blit(text , enemy)
			enemy_rect = pygame.Rect(enemy_img.get_rect())
			enemy_rect.top = enemy[1]
			enemy_rect.left = enemy[0]
			player_rect = pygame.Rect(player.get_rect())
			player_rect.top = playerpos[1]
			player_rect.left = playerpos[0]
			if player_rect.colliderect(enemy_rect):
			#screen.blit(gameover , (0 , 0))
			
				touched = True
				if touched:
					score -= 5
					#screen.fill((255, 0, 0))
					hit_sound.play()
					touched = False
					index1 = enemies.index(enemy)
					enemies.pop(index1)
			for i in arrow_pos:
				arrow_rect = pygame.Rect(arrow.get_rect())
				arrow_rect.top = i[1]
				arrow_rect.left = i[0]
				if enemy_rect.colliderect(arrow_rect):
					#enemy = pygame.transform.scale(player , (40 ,40))
					#enemies.pop(index)
					try:
						index1 = enemies.index(enemy)
						#screen.blit(explosion , enemies[index1])
						explosions.append(enemies[index1])
						#print(enemies[enemy])
						enemies.pop(index1)
						arrow_pos.pop(arrow_index)
						explode_sound.play()
					except ValueError as e:
						print(e)

					scores += 10
					arrow_index += 1
					#index += 1
					
				#pygame.display.flip()
				#score += 30
		for j in arrow_pos:
			j[0] += 10
			for i in arrow_pos:
				screen.blit(arrow , i)
			if j[0] >= width:
				arrow_pos.pop(arrow_index)
			arrow_index = arrow_index

		if arrow_index == len(arrow_pos):
			arrow_index = 0
		explosion = pygame.image.load("img/explosion.png")
		for xy in explosions:
			explosion = pygame.transform.scale(explosion , (30 , 30))
			screen.blit(explosion , (xy[0] - 40 , xy[1] - 40))
			explosion = pygame.transform.scale(explosion , (50 , 50))
			screen.blit(explosion , (xy[0] - 40 , xy[1] - 40))
			explosion = pygame.transform.scale(explosion , (80 , 80))
			screen.blit(explosion , (xy[0] - 40 , xy[1] - 40))
			exp_index = explosions.index(xy)
			#clock.tick(4)
			explosions.pop(exp_index)


		if keys["top"] and playerpos[1] > 0:
			playerpos[1] -= 10
		elif keys["bottom"] and playerpos[1] < 480-40:
			playerpos[1] += 10
		elif keys["right"] and playerpos[0] < 640-40:
			playerpos[0] += 10
		elif keys["left"] and playerpos[0] > 0:
			playerpos[0] -= 10

		pygame.display.flip()
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_w:
					player_animation_index = 1
					keys["top"] = True
				elif event.key == K_s:
					player_animation_index = 1
					keys["bottom"] = True
				elif event.key == K_a:
					player_animation_index = 1
					keys["left"] = True
				elif event.key == K_d:
					player_animation_index = 1
					keys["right"] = True
				elif event.key == K_f:
					player_animation_index = 1
					keys["fire"] = True
					fire_sound.play()
					arrow1 = playerpos[0]
					arrow2 = playerpos[1]
					x = [arrow1 , arrow2]
					player_animation_index = 1
					arrow_pos.append(x)

				elif event.key == pygame.K_RETURN:
					if keys["pause"] == False:
						keys["pause"] = True
					else:
						keys["pause"] = False
			if event.type == pygame.KEYUP:
				if event.key == K_w:
					player_animation_index = 0
					keys["top"] = False
				elif event.key == K_s:
					player_animation_index = 0
					keys["bottom"] = False
				elif event.key == K_a:
					player_animation_index = 0
					keys["left"] = False
				elif event.key == K_d:
					player_animation_index = 0
					keys["right"] = False
				elif event.key == K_f:
					#keys["fire"] = False
					#arrow1 = playerpos[0]
					#arrow2 = playerpos[1]
					#x = [arrow1 , arrow2]
					player_animation_index = 0
					#arrow_pos.append(x)

			if event.type == pygame.MOUSEBUTTONDOWN:
				keys["fire"] = False
				arrow1 = playerpos[0]
				arrow2 = playerpos[1]
				x = [arrow1 , arrow2]
				arrow_pos.append(x)
			#player_animation_index = 0

def main_menu():
	global play_text
	global text
	global button_pos
	global text_color0
	global text_color1
	global color
	global target_score
	global choice
	global playerpos
	global exit_text
	global text_color
	global keys
	global scores
	global enemies
	global score
	global arrow_pos
	#target_score = 10
	score = 50
	scores = 0
	keys["top"]= False
	keys["bottom"] = False
	keys["left"] = False
	keys["right"] = False
	del arrow_pos[:]
	playerpos = [100 , 100]
	del enemies[:]
	while running:
		#play_text = myfont.render(text , True , color)
		screen.fill(pygame.Color("green"))
		screen.blit(play_text , button_pos)
		screen.blit(exit_text , (50 , 70))

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				sys.exit(0)

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				button_rect = pygame.Rect(play_text.get_rect())
				button_rect.top = button_pos[1]
				button_rect.left = button_pos[0]
				if button_rect.collidepoint(mouse_pos):
					#hit_sound.play()
					text = "[Play]"
					screen.fill(pygame.Color("black"))

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					#play_text = myfont.render("Play" , True , color)
					if choice == 0:
						text_color0 = pygame.Color("cyan")
						text_color1 = pygame.Color("white")
						play_text = myfont.render("Play" , True , text_color0)
						exit_text = myfont.render("Exit" , True , text_color1)
						choice = 1
					elif choice == 1:
						text_color0 = pygame.Color("white")
						text_color1 = pygame.Color("cyan")
						play_text = myfont.render("Play" , True , text_color0)
						exit_text = myfont.render("Exit" , True , text_color1)
						choice = 0
					print(choice)

				elif event.key == pygame.K_RETURN:
					if choice == 1:
						game()
						
					elif choice == 0:
						sys.exit()

				elif event.key == pygame.K_DOWN:
					print("pressed")
					if choice == 1:
						text_color0 = pygame.Color("white")
						text_color1 = pygame.Color("cyan")
						play_text = myfont.render("Play" , True , text_color0)
						exit_text = myfont.render("Exit" , True , text_color1)
						choice = 0
					elif choice == 0:
						text_color0 = pygame.Color("cyan")
						text_color1 = pygame.Color("white")
						play_text = myfont.render("Play" , True , text_color0)
						exit_text = myfont.render("Exit" , True , text_color1)
						choice = 1



		mouse_pos = pygame.mouse.get_pos()
		button_rect = pygame.Rect(play_text.get_rect())
		button_rect.top = button_pos[1]
		button_rect.left = button_pos[0]
		pygame.display.flip()


main_menu()