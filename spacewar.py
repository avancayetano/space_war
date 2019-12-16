

# SPACE WAR

# "The Complex"
# Kevin MacLeod (incompetech.com)
# Licensed under Creative Commons: By Attribution 3.0
# http://creativecommons.org/licenses/by/3.0/

import pygame
import sys 
import random
import time
import math
import json
import os

from pygame.locals import *

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 650
WINDOW_COLOR = (0,0,0)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.set_alpha(None)

GAME_WINDOW_WIDTH = 1100
GAME_WINDOW_HEIGHT = 650

FONT_COLOR = (255, 255, 255)

GAME_WINDOW = pygame.surface.Surface((GAME_WINDOW_WIDTH,
	GAME_WINDOW_HEIGHT), pygame.SRCALPHA, 32)
GAME_WINDOW = GAME_WINDOW.convert_alpha()

GAME_BACKGROUND_LAYER = pygame.surface.Surface((GAME_WINDOW_WIDTH,
	GAME_WINDOW_HEIGHT))
GAME_BACKGROUND_LAYER.set_alpha(None)
GAME_BACKGROUND_COLOR = (0,0,0)#(45, 52, 54)

pygame.display.set_caption("avan")

FPS = 60
clock = pygame.time.Clock()
dead = True
username1 = "ENTER NAME AND SECTION"
username2 = "ENTER NAME AND SECTION"
display_winner = False
winner = ""
bullet_timer1 = 0
bullet_timer2 = 0
def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


font_file_path = find_data_file("good_times_rg.ttf")
font_obj = pygame.font.Font(font_file_path, 15)
music_path = find_data_file("TheComplex.mp3")

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

menu_text_surface = font_obj.render('PRESS ENTER TO PLAY',
	False, FONT_COLOR, WINDOW_COLOR)
menu_surface_rect = menu_text_surface.get_rect()
menu_surface_rect.center = (WINDOW_WIDTH/2.0, WINDOW_HEIGHT/2.0)


username_input_rect1 = pygame.Rect(menu_surface_rect.left - 50,
	menu_surface_rect.bottom + 10, menu_surface_rect.width + 100,
	menu_surface_rect.height + 10)

username_text_surface1 = font_obj.render(username1, False, FONT_COLOR,
	WINDOW_COLOR)
username_surface_rect1 = username_text_surface1.get_rect()
username_surface_rect1.topleft = (username_input_rect1.left + 30,
	username_input_rect1.top + 5)


username_input_rect2 = pygame.Rect(menu_surface_rect.left - 50,
	username_surface_rect1.bottom + 20, menu_surface_rect.width + 100,
	menu_surface_rect.height + 10)

username_text_surface2 = font_obj.render(username2, False, FONT_COLOR,
	WINDOW_COLOR)
username_surface_rect2 = username_text_surface1.get_rect()
username_surface_rect2.topleft = (username_input_rect2.left + 30,
	username_input_rect2.top + 5)

winner_text_surface = font_obj.render('WINNER: ' + winner,
	False, FONT_COLOR, WINDOW_COLOR)
winner_surface_rect = winner_text_surface.get_rect()
winner_surface_rect.center = (WINDOW_WIDTH/2.0, (WINDOW_HEIGHT/2.0) + 110)



class Stars(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.radius = random.randrange(2,10)
		self.color = (random.randrange(200, 256),random.randrange(200, 256),
			random.randrange(200, 256))
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2),
			pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)
		self.rect = self.sprite_surface.get_rect()
		self.rect.topleft = (random.randrange(GAME_WINDOW_WIDTH),
			random.randrange(GAME_WINDOW_HEIGHT))
		self.speed = 1

	def move(self):
		self.rect.top = self.rect.top + self.speed

	def reset(self):
		self.radius = random.randrange(2,10)
		self.color = (random.randrange(200, 256),random.randrange(200, 256),
			random.randrange(200, 256))
		self.rect.topleft = (random.randrange(GAME_WINDOW_WIDTH),
			random.randrange(-4 * self.radius, -2 * self.radius))
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2),
			pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)



class Bullet(pygame.sprite.Sprite):

	def __init__(self, pos, angle, color):
		pygame.sprite.Sprite.__init__(self)

		self.angle = angle
		self.pos = pos
		self.radius = 5
		self.speed = 10
		self.color = color
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2), 
			pygame.SRCALPHA, 32).convert_alpha()
		self.rect = self.sprite_surface.get_rect()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, self.radius), self.radius)

	def is_collided_with(self, other):
		if pygame.sprite.collide_rect_ratio(0.9)(self, other):
			other.hitponts -= 1
			return True

	def move(self, group):
		self.pos[0] += math.cos(math.radians(self.angle)) * self.speed
		self.pos[1] -= (math.sin(math.radians(self.angle))) * self.speed
		self.rect.center = (self.pos[0], self.pos[1])

		if self.rect.left > WINDOW_WIDTH or self.rect.right < 0:
			group.remove(self)
		if self.rect.top > WINDOW_HEIGHT or self.rect.bottom < 0:
			group.remove(self)



class Spaceship(pygame.sprite.Sprite):

	def __init__(self, color, pos, number, gun_angle):
		pygame.sprite.Sprite.__init__(self)
		self.number = number
		self.radius = 25
		self.color = color
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2), 
			pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)
		self.rect = self.sprite_surface.get_rect()
		self.rect.center = pos
		self.speed = 5
		self.gun_length = 50
		self.gun_width = 10
		self.gun_angle = gun_angle
		self.gun_rotate = 7
		self.hitponts = 100


	def move_gun_left(self):
		self.gun_angle -= self.gun_rotate

	def move_gun_right(self):
		self.gun_angle += self.gun_rotate

	def draw_gun(self):
		self.gun_point1 = (
			self.rect.centerx + math.cos(math.radians(self.gun_angle + 90)) * (self.gun_width/2.0),
			self.rect.centery - math.sin(math.radians(self.gun_angle + 90)) * (self.gun_width/2.0)
			)
		self.gun_point4 = (
			self.rect.centerx + math.cos(math.radians(self.gun_angle - 90)) * (self.gun_width/2.0),
			self.rect.centery - math.sin(math.radians(self.gun_angle - 90)) * (self.gun_width/2.0)
			)
		self.gun_point2 = (
			self.gun_point1[0] + math.cos(math.radians(self.gun_angle)) * self.gun_length,
			self.gun_point1[1] - math.sin(math.radians(self.gun_angle)) * self.gun_length
			)
		self.gun_point3 = (
			self.gun_point4[0] + math.cos(math.radians(self.gun_angle)) * self.gun_length,
			self.gun_point4[1] - math.sin(math.radians(self.gun_angle)) * self.gun_length			
			)

		self.gun_coord = (self.gun_point1, self.gun_point2, self.gun_point3, self.gun_point4)

		pygame.draw.polygon(GAME_WINDOW, self.color, self.gun_coord)

	def move_left(self):
		self.rect.left = self.rect.left - self.speed

	def move_right(self):
		self.rect.left = self.rect.left + self.speed

	def move_up(self):
		self.rect.top = self.rect.top - self.speed

	def move_down(self):
		self.rect.top = self.rect.top + self.speed


ship = pygame.sprite.GroupSingle()
stars = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()

for i in range(20):
	star  =  Stars()
	stars.add(star)

ship1 = Spaceship((129, 236, 236), (20 + 50, GAME_WINDOW_HEIGHT - 20 - 80), 1, 0)
ship2 = Spaceship((250, 177, 160), (GAME_WINDOW_WIDTH - 20 - 50, 20 + 80), 2, 180)

ship.add(ship1)
ship.add(ship2)

cursor = False
while True:
	
	pressed = pygame.key.get_pressed()
	clicked = pygame.mouse.get_pressed()[0]
	mouse_pos = pygame.mouse.get_pos()
	if clicked:
		if username_input_rect1.collidepoint(mouse_pos):
			cursor = "usr1"
			username1 = ""
		elif username_input_rect2.collidepoint(mouse_pos):
			cursor = "usr2"
			username2 = ""
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if cursor == "usr1":
			if (event.type == pygame.KEYDOWN and dead):
				if event.key == pygame.K_BACKSPACE:
					if username1 == "ENTER NAME AND SECTION":
						username1 = ""
					else:
						username1 = username1[:-1]
						if username1 == "" or len(username1) <= 0:
							username1 = "ENTER NAME AND SECTION"
				elif event.key == pygame.K_RETURN:
					pass
				else:
					if username1 == "ENTER NAME AND SECTION":
						username1 = ""
					username1 = username1 + event.unicode
					username1 = username1.upper()
		elif cursor == "usr2":
			if (event.type == pygame.KEYDOWN and dead):
				if event.key == pygame.K_BACKSPACE:
					if username2 == "ENTER NAME AND SECTION":
						username2 = ""
					else:
						username2 = username1[:-1]
						if username2 == "" or len(username2) <= 0:
							username2 = "ENTER NAME AND SECTION"
				elif event.key == pygame.K_RETURN:
					pass
				else:
					if username2 == "ENTER NAME AND SECTION":
						username2 = ""
					username2 = username2 + event.unicode
					username2 = username2.upper()


	if dead:
		WINDOW.fill(GAME_BACKGROUND_COLOR)

		winner_text_surface = font_obj.render(winner,
			False, FONT_COLOR, WINDOW_COLOR)

		username_text_surface1 = font_obj.render(username1, False, FONT_COLOR,
			WINDOW_COLOR)
		username_text_surface2 = font_obj.render(username2, False, FONT_COLOR,
			WINDOW_COLOR)

		winner_surface_rect = winner_text_surface.get_rect()
		winner_surface_rect.center = (WINDOW_WIDTH/2.0, (WINDOW_HEIGHT/2.0) + 110)

		GAME_WINDOW.blit(winner_text_surface, winner_surface_rect)
		GAME_WINDOW.blit(username_text_surface1, username_surface_rect1)
		GAME_WINDOW.blit(username_text_surface2, username_surface_rect2)
		GAME_WINDOW.blit(menu_text_surface, menu_surface_rect)
		ship1.gun_angle = 0
		ship2.gun_angle = 180
		ship1.draw_gun()
		ship2.draw_gun()
		GAME_WINDOW.blit(ship1.sprite_surface, ship1.rect)
		GAME_WINDOW.blit(ship2.sprite_surface, ship2.rect)
		bullet_timer1 += 1
		bullet_timer2 += 1

		if  bullet_timer1 > 5:
			bullet_timer1 = 0
			bullet_pos = [
				(ship1.gun_point2[0] + ship1.gun_point3[0])/2.0,
				(ship1.gun_point2[1] + ship1.gun_point3[1])/2.0
				]
			bullet = Bullet(bullet_pos, ship1.gun_angle, ship1.color)

			bullets1.add(bullet)

		for bullet in bullets1:
			bullet.move(bullets1)
			GAME_WINDOW.blit(bullet.sprite_surface, bullet.rect)

		if  bullet_timer2 > 5:
			bullet_timer2 = 0
			bullet_pos = [
				(ship2.gun_point2[0] + ship2.gun_point3[0])/2.0,
				(ship2.gun_point2[1] + ship2.gun_point3[1])/2.0
				]
			bullet = Bullet(bullet_pos, ship2.gun_angle, ship2.color)

			bullets2.add(bullet)

		for bullet in bullets2:
			bullet.move(bullets2)
			GAME_WINDOW.blit(bullet.sprite_surface, bullet.rect)

		pygame.draw.rect(GAME_WINDOW, (255, 255, 255), username_input_rect1, 2)
		pygame.draw.rect(GAME_WINDOW, (255, 255, 255), username_input_rect2, 2)

		if pressed[K_RETURN] and (username1 != "" and username2 != "" and
				username1 != "ENTER NAME AND SECTION" and username2 != "ENTER NAME AND SECTION"):
			bullet_strg1 = 500
			bullet_strg2 = 500
			dead = False
			bullet_timer1 = 0
			bullet_timer2 = 0
			ship1.hitponts = 100
			ship2.hitponts = 100
			username_surface_rect1 = (10, GAME_WINDOW_HEIGHT - 60)
			username_surface_rect2 = (GAME_WINDOW_WIDTH - 140, 10)

	else:

		bullet_strg1_surface = font_obj.render("BULLETS: " + str(bullet_strg1), 
			False, FONT_COLOR, WINDOW_COLOR)
		GAME_WINDOW.blit(bullet_strg1_surface, (10, GAME_WINDOW_HEIGHT - 20))
		bullet_strg2_surface = font_obj.render("BULLETS: " + str(bullet_strg2), 
			False, FONT_COLOR, WINDOW_COLOR)
		GAME_WINDOW.blit(bullet_strg2_surface, (GAME_WINDOW_WIDTH - 140, 50))

		ship1_hp_surface = font_obj.render("HP: " + str(ship1.hitponts), 
			False, FONT_COLOR, WINDOW_COLOR)
		GAME_WINDOW.blit(ship1_hp_surface, (10, GAME_WINDOW_HEIGHT - 40))

		ship2_hp_surface = font_obj.render("HP: " + str(ship2.hitponts), 
			False, FONT_COLOR, WINDOW_COLOR)
		GAME_WINDOW.blit(ship2_hp_surface, (GAME_WINDOW_WIDTH - 140, 30))

		GAME_WINDOW.blit(username_text_surface1, username_surface_rect1)
		GAME_WINDOW.blit(username_text_surface2, username_surface_rect2)

		bullet_timer1 += 1
		bullet_timer2 += 1
		ship1.draw_gun()
		ship2.draw_gun()
		GAME_WINDOW.blit(ship1.sprite_surface, ship1.rect)
		GAME_WINDOW.blit(ship2.sprite_surface, ship2.rect)


		if pressed[K_a] and ship1.rect.left > 0:
			ship1.move_left()
		if pressed[K_d] and ship1.rect.right < WINDOW_WIDTH:
			ship1.move_right()
		if pressed[K_w] and ship1.rect.top > 0:
			ship1.move_up()
		if pressed[K_s] and ship1.rect.bottom < WINDOW_HEIGHT:
			ship1.move_down()
		if pressed[K_k]:
			ship1.move_gun_left()
		if pressed[K_j]:
			ship1.move_gun_right()
		if pressed[K_SPACE] and bullet_strg1 > 0 and  bullet_timer1 > 5:
			bullet_timer1 = 0
			bullet_pos = [
				(ship1.gun_point2[0] + ship1.gun_point3[0])/2.0,
				(ship1.gun_point2[1] + ship1.gun_point3[1])/2.0
				]
			bullet = Bullet(bullet_pos, ship1.gun_angle, ship1.color)
			bullet_strg1 -= 1

			bullets1.add(bullet)


		if pressed[K_LEFT] and ship2.rect.left > 0:
			ship2.move_left()
		if pressed[K_RIGHT] and ship2.rect.right < WINDOW_WIDTH:
			ship2.move_right()
		if pressed[K_UP] and ship2.rect.top > 0:
			ship2.move_up()
		if pressed[K_DOWN] and ship2.rect.bottom < WINDOW_HEIGHT:
			ship2.move_down()
		if pressed[K_1]:
			ship2.move_gun_left()
		if pressed[K_3]:
			ship2.move_gun_right()
		if pressed[K_2] and bullet_strg2 > 0  and bullet_timer2 > 5:
			bullet_timer2 = 0
			bullet_pos = [
				(ship2.gun_point2[0] + ship2.gun_point3[0])/2.0,
				(ship2.gun_point2[1] + ship2.gun_point3[1])/2.0
				]
			bullet = Bullet(bullet_pos, ship2.gun_angle, ship2.color)

			bullet_strg2 -= 1
			bullets2.add(bullet)

		for bullet in bullets1:
			if bullet.is_collided_with(ship2):
				bullets1.remove(bullet)
				continue
			else:
				bullet.move(bullets1)

			GAME_WINDOW.blit(bullet.sprite_surface, bullet.rect)

		for bullet in bullets2:
			if bullet.is_collided_with(ship1):
				bullets2.remove(bullet)
				continue
			else:
				bullet.move(bullets2)
			GAME_WINDOW.blit(bullet.sprite_surface, bullet.rect)




		if ship1.hitponts == 0 or bullet_strg1 == 0:
			winner = "WINNER: " + username2
			dead = True
		elif ship2.hitponts == 0 or bullet_strg2 == 0:
			winner = "WINNER: " + username1
			dead = True

		if dead:
			username1 = "ENTER NAME AND SECTION"
			username2 = "ENTER NAME AND SECTION"
			pygame.time.delay(2000)

			ship1.rect.center = (20 + 50, GAME_WINDOW_HEIGHT - 20 - 80)
			ship2.rect.center = (GAME_WINDOW_WIDTH - 20 - 50, 20 + 80)

			username_surface_rect1 = (username_input_rect1.left + 30,
				username_input_rect1.top + 5)

			username_surface_rect2 = (username_input_rect2.left + 30,
				username_input_rect2.top + 5)

			for bullet in bullets2:
				bullets2.remove(bullet)
			for bullet in bullets1:
				bullets1.remove(bullet)

	for star in stars:
		star.move()
		if star.rect.top > GAME_WINDOW_HEIGHT:
			star.reset()
		GAME_BACKGROUND_LAYER.blit(star.sprite_surface, star.rect)
	WINDOW.blit(GAME_BACKGROUND_LAYER, (0, 0))


	GAME_BACKGROUND_LAYER.fill(GAME_BACKGROUND_COLOR)
	WINDOW.blit(GAME_WINDOW, (0, 0))
	GAME_WINDOW.fill((0, 0, 0, 0))


	pygame.display.update()
	clock.tick(FPS)