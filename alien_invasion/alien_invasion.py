import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
	"""Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry."""

	def __init__(self):
		"""Inicjalizacja gry i utworzenie jej zasobów."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Inwazja obcych")

		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		self.play_button = Button(self, self.screen, "Gra")

		pygame.mouse.set_visible(False)
		
	
	def run_game(self):
		"""rozpoczęcie pętli głównej gry."""
		while True:
			self._check_events()

			if self.stats.game_active:		
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
						
			self._update_screen()

	def _check_events(self):
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP:
					self._check_keyup_events(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)



	def _check_keydown_events(self, event):
					if event.key == pygame.K_RIGHT:
						self.ship.moving_right = True
					elif event.key == pygame.K_LEFT:
						self.ship.moving_left = True
					elif event.key == pygame.K_q:
						sys.exit()
					elif event.key == pygame.K_SPACE:
						self._fire_bullet()


	def _check_keyup_events(self, event):
				
					if event.key == pygame.K_RIGHT:
						self.ship.moving_right = False
					elif event.key == pygame.K_LEFT:
						self.ship.moving_left = False



	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:	
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)



	def _update_bullets(self):
		self.bullets.update()

		for bullet in self.bullets.copy():
				if bullet.rect.bottom <=0:
					self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()



	def _check_bullet_alien_collisions(self):
 		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

 		if not self.aliens:
 			self.bullets.empty()
 			self._create_fleet()	



	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		if not self.stats.game_active:
			self.play_button.draw_button()

		#wyświetlanie ostatnio zmodyfikowanego ekranu.
		
		pygame.display.flip()

	def _create_fleet(self):

		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#ustalenie ile rzędów obcych zmieści się na ekranie
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 3 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)
	

	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width *alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _update_aliens(self):
		"""Sprawdzenie, czy flota obcych znajduje się przy krawędzi, a następnie uaktualnienie położenia wszystkich obcych we flocie"""
		self._check_fleet_edges()
		self.aliens.update()

		#Wykrywanie kolizji między obcym i statkiem
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		self._check_aliens_bottom()



	def _check_fleet_edges(self):
		"""Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Przesunięcie całej floty w dół i zmiana kiedrunku, w którym się porusza"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship

			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _check_play_button(self, mouse_pos):

		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.stats.reset_stats()
			self.stats.game_active = True

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()
			pygame.mouse.set_visible(False)

if __name__ == '__main__':
	#utworzenie egzemplarza gry i jej uruchomienie.
	ai = AlienInvasion()
	ai.run_game()