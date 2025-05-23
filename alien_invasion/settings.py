class Settings:

	"""Klasa przeznaczona do przechowywania wszystkich ustawień gry"""

	def __init__(self):
		"""Inicjalizacja ustawień gry"""
		#ustawienia  ekranu
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230,230)
		self.ship_speed = 1.0
		self.ship_limit = 2

		self.bullet_speed = 1.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3

		self.alien_speed = 0.6
		self.fleet_drop_speed = 10
		self.fleet_direction = 1