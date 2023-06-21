import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import os

pygame.mixer.pre_init(44100, -16,-2, 512)
mixer.init()
pygame.init()
clock =  pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('des')

font = pygame.font.SysFont('Bauhaus 93', 70)
white = (255, 255, 255)
blue = (0, 0, 255)

tile_size = 50
game_over = 0
main_menu = True
level = 4
max_level = 7


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_level(level):
	player.reset(100, screen_height - 130)
	enemy_group.empty()
	platform_group.empty()
	lava_group.empty()
	exit_group.empty()
	

	if path.exists(f'levels/level{level}_data'):
		pickle_in = open(f'levels/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
		world = World(world_data)

	return world












class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False
		position =  pygame.mouse.get_pos()
		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, self.rect)
		return action

# class menu():
# 	def __init__(self, x, y):
# 		BLACK = (0, 0, 0)
# 		WHITE = (255, 255, 255)
# 		PURPLE = (128, 0, 128)

# 		# Create font objects
# 		font = pygame.font.Font(None, 36)
# 		large_font = pygame.font.Font(None, 72)  # Larger font for "DEŠ"

# 		# Create button surfaces
# 		button_width = 200
# 		button_height = 100
# 		button_gap = 20  # Gap between buttons

# 		button_level1 = pygame.Surface((button_width, button_height))
# 		button_level2 = pygame.Surface((button_width, button_height))

# 		# Set button colors
# 		button_level1.fill(WHITE)
# 		button_level2.fill(WHITE)

# 		# Set button positions
# 		button_level1_rect = button_level1.get_rect(center=(screen_width // 2, screen_height // 2 - button_height // 2 - button_gap // 2))
# 		button_level2_rect = button_level2.get_rect(center=(screen_width // 2, screen_height // 2 + button_height // 2 + button_gap // 2))

# 		# Create text surfaces for buttons
# 		text_level1 = font.render("Level 1", True, BLACK)
# 		text_level2 = font.render("Level 2", True, BLACK)

# 		# Set text positions
# 		text_level1_rect = text_level1.get_rect(center=button_level1_rect.center)
# 		text_level2_rect = text_level2.get_rect(center=button_level2_rect.center)

# 		# Create text surface for DEŠ on top (with larger font)
# 		text_des = large_font.render("DEŠ", True, PURPLE)
# 		text_des_rect = text_des.get_rect(center=(screen_width // 2, 50))









bg_img = pygame.image.load('img/sky.jpg')
restart_img = pygame.image.load('img/restart.png')
restart_img = pygame.transform.scale(restart_img,(180, 120))
start_img = pygame.image.load('img/start.png')
start_img = pygame.transform.scale(start_img,(180, 120))
exit_img = pygame.image.load('img/exit.jpg')
exit_img = pygame.transform.scale(exit_img, (180, 120))

death_sx = pygame.mixer.Sound("sounds/death.mp3")
death_sx.set_volume(0.5)
game_sx = pygame.mixer.Sound("sounds/game.mp3")
game_sx.set_volume(0.5)
jump_sx = pygame.mixer.Sound("sounds/jump.mp3")
jump_sx.set_volume(0.5)
menu_sx = pygame.mixer.Sound("sounds/menu.mp3")
menu_sx.set_volume(0.5)






def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class Player():
	def __init__(self, x, y):
		self.images_p = []
		self.images_l = []
		self.index = 0
		self.counters = 0
		for i in range(1, 5):
			img_p = pygame.image.load(f"img/player{i}.png")

			img_p =pygame.transform.scale(img_p,(40,80))
			img_l = pygame.transform.flip(img_p, True,False)

			self.images_p.append(img_p)
			self.images_l.append(img_l)
		self.ghost = pygame.image.load("img/ghost.jpg")
		self.ghost = pygame.transform.scale(self.ghost,(40,80))
		self.image = self.images_p[self.index]
		self.rect = self.image.get_rect()




		img = pygame.image.load("img/player1.png")
		self.image = pygame.transform.scale(img, (40, 80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0


	def update(self, game_over):
		dx = 0
		dy = 0
		cooldown = 5
		col_threshold = 20

		if game_over == 0:
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_sx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
				
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_p[self.index]
				if self.direction == -1:
					self.image = self.images_l[self.index]


			if self.counter > cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_p):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_p[self.index]
				if self.direction == -1:
					self.image = self.images_l[self.index]




			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			self.in_air =  True

			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
						
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False




			if pygame.sprite.spritecollide(self, enemy_group, False):
				game_over = -1
				death_sx.play()

			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				death_sx.play()

			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = +1

			for platform in platform_group:
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_threshold:
						self.vel_y = 0
						dy = platform.rect.bottom - platform.rect.top
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_threshold:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					if platform.move_x != 0:
						self.rect.x += platform.move_direction
				





			self.rect.x += dx
			self.rect.y += dy

		elif game_over == -1:
			self.image = self.ghost
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 0:
				self.rect.y -= 5

		screen.blit(self.image, self.rect)

		return game_over
	



	def reset(self, x, y):
		self.images_p = []
		self.images_l = []
		self.index = 0
		self.counters = 0
		for i in range(1, 5):
			img_p = pygame.image.load(f"img/player{i}.png")

			img_p =pygame.transform.scale(img_p,(40,80))
			img_l = pygame.transform.flip(img_p, True,False)

			self.images_p.append(img_p)
			self.images_l.append(img_l)
		self.ghost = pygame.image.load("img/ghost.jpg")
		self.ghost = pygame.transform.scale(self.ghost,(40,80))
		self.image = self.images_p[self.index]
		self.rect = self.image.get_rect()




		img = pygame.image.load("img/player1.png")
		self.image = pygame.transform.scale(img, (40, 80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_airs = True

		






class World():
	def __init__(self, data):
		self.tile_list = []

		dirt_img = pygame.image.load('img/obsidian.png')
		grass_img = pygame.image.load('img/end.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					enemy = Enemy(col_count * tile_size, row_count * tile_size)
					enemy_group.add(enemy)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)

					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size)
					lava_group.add(lava)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - tile_size// 2)
					exit_group.add(exit)





				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])





class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/enemy.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y + 14
		self.move_direction = 1
		self.move_count = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_count += 1
		if abs(self.move_count) > 50:
			self.move_direction *= -1
			self.move_count *= -1

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/platform.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect =self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.count = 0
		self.move_x = move_x
		self.move_y = move_y

	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.count += 1
		if abs(self.count) > 50:
			self.move_direction *= -1
			self.count *= -1










class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava_bucket.png')
		self.image = pygame.transform.scale(img, (tile_size , tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit_door.jpg')
		self.image = pygame.transform.scale(img, (tile_size , int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y





# world_data = [
# [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
# [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
# [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
# [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
# [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
# [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
# [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
# [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]



player = Player(100, screen_height - 130)

enemy_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()




if path.exists(f'levels/level{level}_data'):
	pickle_in = open(f'levels/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))
	if main_menu == True:
		menu_sx.play()
		if start_button.draw():
			main_menu = False
		if exit_button.draw():
			run = False
		
	else:
		menu_sx.stop()
		game_sx.play()




		world.draw()

		if game_over == 0:
			enemy_group.update()
			platform_group.update()
		
		
		enemy_group.draw(screen)
		lava_group.draw(screen)
		exit_group.draw(screen)
		platform_group.draw(screen)

		game_over = player.update(game_over)


		if game_over == -1:
			if restart_button.draw():
				death_sx.play()
				world_data = []
				world = reset_level(level)
				game_over = 0
				print("restart")



		if game_over == 1:
			level += 1
			if level <= max_level:
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
				if restart_button.draw():
					level = 1
					world_data = []
					world = reset_level(level)
					game_over = 0
				





	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
