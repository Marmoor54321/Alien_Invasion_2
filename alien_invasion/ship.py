import  pygame 

class Ship:
	def __init__(self, ai_game):
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#wczytanie obrazu s tatku kosmicznego i pobranie jego prostokąta
		self.image = pygame.image.load('ship.bmp')
		self.rect = self.image.get_rect()

		#każdy nowy statek pojawia się na dole ekranu
		self.rect.midbottom = self.screen_rect.midbottom

		self.x = float(self.rect.x)

		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left>0:
			self.x -= self.settings.ship_speed

		self.rect.x = self.x


	def blitme(self):
		#wyświetlanie statku kosmicznego w jego aktualnym położeniu
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		self.rect.midbottom  = self.screen_rect.midbottom
		self.x = float(self.rect.x)