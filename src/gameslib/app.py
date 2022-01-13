import pygame, gameslib

class App():

	def __init__(self, size: gameslib.Size = (600, 300), title: str = 'GamesLib'):
		self._screen = pygame.display.set_mode(size)
		self._scene = None

		pygame.display.set_caption(title)

	@property
	def screen(self) -> pygame.Surface:
		return self._screen

	@property
	def size(self) -> gameslib.Size:
		return self.screen.get_size()

	@property
	def scene(self) -> object:
		return self._scene

	@scene.setter
	def scene(self, scene: object) -> None:

		if self._scene is not None:
			self._scene.stop()

		self._scene = scene

		if self._scene is not None:
			self._scene.start(self)
