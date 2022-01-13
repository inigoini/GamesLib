import pygame, sys, gameslib


class Scene(pygame.sprite.LayeredDirty):
	"""Base class for any scene

	Each App can have any number of scenes,
	but only one can be running at a given time

	import gameslib

	app = gameslib.App()
	app.scene = gameslib.Scene()
	"""

	def __init__(self, background: pygame.Surface | gameslib.Color, fps: int=24) -> None:
		self._fps = fps
		self._app = None
		self._layer = pygame.sprite.LayeredDirty()
		self._running = False

		# Events
		self._on_start = None
		self._on_update = None
		self._on_stop = None

		self._on_keys_pressed = None
		self._on_key_down = None
		self._on_key_up = None

		self._on_mouse_down = None
		self._on_mouse_up = None

		self._on_joystick_button_down = None
		self._on_joystick_button_up = None
		self._on_joystick_axis = None
		self._on_joystick_hat = None

		if isinstance(background, pygame.Surface):
			self._background = background
			self._bg_color = None

		# if background is a color
		elif isinstance(background, tuple):
			self._background = None
			self._bg_color = background

		else:
			self._background = None
			self._bg_color = (0, 0, 0)

	@property
	def app(self) -> object:
		return self._app

	@property
	def layer(self) -> int:
		return self._layer

	@property
	def fps(self) -> int:
		return self._fps

	@property
	def background(self) -> pygame.Surface:
		return self._background

	@property
	def is_running(self) -> bool:
		return self._running

	def append(self, sprite: pygame.sprite.DirtySprite) -> pygame.sprite.DirtySprite:
		self._layer.add(sprite)
		return sprite

	def on_update(self, func: callable):
		"""Set on_update event function."""

		self._on_update = func

	def do_update(self, delta: float):
		"""Executes the scene on_update event, if set."""

		if self._on_update:
			self._on_update(delta, self)

	def on_start(self, func: callable):
		"""Set on_start event function."""

		self._on_start = func

	def do_start(self):
		"""Executes the scene on_start event, if set."""

		if self._on_start:
			self._on_start(self)

	def on_stop(self, func: callable):
		"""Set on_stop event function."""

		self._on_stop = func

	def do_stop(self):
		"""Executes on_stop event, if set."""

		if self._on_stop:
			self._on_stop(self)

	def on_keys_pressed(self, func: callable) -> None:
		"""Set on_keys_pressed event function."""

		self._on_keys_pressed = func

	def do_keys_pressed(self, delta: float) -> None:
		"""Executes do_keys_pressed event, if set."""

		if self._on_keys_pressed is not None:
			keys_pressed = pygame.key.get_pressed()
			self._on_keys_pressed(keys_pressed, self, delta)

	def on_key_down(self, func: callable) -> None:
		"""Set on_key_down event function."""

		self._on_key_down = func

	def do_key_down(self, event) -> bool:

		# Ctrl + C -> stops the scene
		if event.key == pygame.K_c:
			mods = pygame.key.get_mods()

			if mods & pygame.KMOD_CTRL:
				self.stop()
				return True

		if self._on_key_down:
			return self._on_key_down(event, self)

		return False

	def on_key_up(self, func: callable) -> None:
		"""Set on_key_up event function."""

		self._on_key_up = func

	def do_key_up(self, event) -> bool:

		if self._on_key_up:
			return self._on_key_up(event, self)

		return False

	def on_mouse_down(self, func: callable) -> None:
		"""Set a function as listener of mouse down event.

		@scene.on_mouse_down
		def on_mouse_down(event, scene):
		"""

		self._on_mouse_down = func

	def do_mouse_down(self, event) -> bool:
		"""Executes the "on mouse down" event.
		Usually called internally, when a mouse button is pressed down.

		return: boolean
			True if the event has been consumed, false in other cases
		"""

		if self._on_mouse_down is not None:
			return self._on_mouse_down(event, self)

		return False

	def on_mouse_up(self, func:callable) -> None:
		"""Set a function as listener of mouse up event.

		@scene.on_mouse_up
		def on_mouse_up(event, scene):
		"""

		self._on_mouse_up = func

	def do_mouse_up(self, event) -> bool:
		"""Executes the "on mouse up" event.
		Usually called internally, when a mouse button is pressed up.

		return: boolean
			True if the event has been consumed, false in other cases
		"""

		if self._on_mouse_up is not None:
			return self._on_mouse_up(event, self)

		return False

	def stop(self) -> object:
		"""Stops scene."""

		self._running = False
		self.do_stop()

		return self

	def update(self, delta: float) -> None:

		self._layer.update(delta)
		rects = self._layer.draw(self.app.screen)
		pygame.display.update(rects)

		self.do_update(delta)

	def manage_events(self, delta: float) -> None:
		"""Manages key, mouse and joystick events."""

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				self.stop()
				return

			self.do_keys_pressed(delta)

			if event.type == pygame.KEYDOWN:
				self.do_key_down(event)

			elif event.type == pygame.KEYUP:
				self.do_key_up(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.do_mouse_down(event)

			elif event.type == pygame.MOUSEBUTTONUP:
				self.do_mouse_up(event)

			'''elif self._running:
				self._manage_joystick(event)'''

	def start(self, app: gameslib.App) -> None:
		self._app = app

		if self._background is None and self._bg_color is not None:
			self._background = pygame.Surface(app.size)
			self._background.fill(self._bg_color)

		self._layer.clear(app.screen, self._background)

		w, h = self.app.size
		self._layer.repaint_rect((0, 0, w, h))

		# calls on_start event
		self.do_start()

		clock = pygame.time.Clock()
		self._running = True

		while self._running:

			delta = clock.tick(self.fps)

			self.update(delta)
			self.manage_events(delta)
