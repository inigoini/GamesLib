import pygame

class Sprite(pygame.sprite.DirtySprite):

	def __init__(self, source: pygame.Surface, pos: tuple=(0, 0), source_rect: tuple=None, frames: list=[], fps: int=12) -> None:
		pygame.sprite.DirtySprite.__init__(self)

		for i in range(len(frames)):

			if not isinstance(frames[i], pygame.Rect):
				frames[i] = pygame.Rect(frames[i])

		self.image = source

		if source_rect is not None:
			source_rect = source_rect if isinstance(source_rect, pygame.Rect) else pygame.Rect(source_rect)
			self.source_rect = source_rect
			w, h = source_rect.w, source_rect.h

		else:
			_, _, w, h = source.get_rect()

		self.rect = pygame.Rect(pos, (w, h))
		self.dirty = 1

		self._frames = frames
		self._frame = 0
		self._loops = -1
		self._fps = 1000 / fps if fps > 0 else 0
		self._is_animated = False
		self._delta = 0

		self._speed_x = 0
		self._speed_y = 0

		self._on_animation_loop_stop = None

	@property
	def pos(self) -> tuple:
		x, y, _, _ = self.rect
		return (x, y)

	@property
	def size(self) -> tuple:
		_, _, w, h = self.rect
		return (w, h)

	def on_animation_loop_stop(self, func: callable) -> None:
		self._on_animation_loop_stop = func

	def do_animation_loop_stop(self):

		if self._on_animation_loop_stop is not None:
			self._on_animation_loop_stop(self)

	def play_animation(self, loops: int=-1) -> object:
		self._is_animated = True
		self._loops = loops
		return self

	def stop_animation(self) -> object:
		self._is_animated = False
		self._frame = 0

		if len(self._frames) > 0:
			self.source_rect = self._frames[0]
			self.dirty = 1

		return self

	def pause_animation(self) -> object:
		self._is_animated = False
		return self

	def update(self, delta: int, *args) -> None:
		
		if self._is_animated and self._fps > 0:
			self._delta += delta

			if self._delta > self._fps:
				self._delta = 0
				self._frame += 1

				if self._frame >= len(self._frames):
					self._frame = 0
					self._loops -= 1

				if self._loops == 0:
					self._is_animated = False
					self.do_animation_loop_stop()

				self.source_rect = self._frames[self._frame]
				self.dirty = 1

		if self._speed_x != 0 or self._speed_y != 0:
			self.rect.left += self._speed_x * delta
			self.rect.top += self._speed_y * delta
			self.dirty = 1

class SpriteEx(Sprite):

	def __init__(self, source: pygame.Surface, pos: tuple=(0, 0), source_rect: tuple=None, frames: dict={}, fps: int=12) -> None:

		self._frames_ex = frames
		self._frames_key = list(frames.keys())[0]

		for key in list(self._frames_ex.keys()):
			for i in range(len(self._frames_ex[key])):

				if not isinstance(self._frames_ex[key][i], pygame.Rect):
					self._frames_ex[key][i] = pygame.Rect(self._frames_ex[key][i])

		Sprite.__init__(self, source, pos, source_rect, frames[self._frames_key], fps)

	@property
	def frames_key(self) -> int:
		return self._frames_key

	@frames_key.setter
	def frames_key(self, frames_key: str) -> None:

		if frames_key is not None and self._frames_key != frames_key:
			self._frames = self._frames_ex[frames_key]
			self._frames_key = frames_key
			self._frame = 0
			self.source_rect = self._frames[self._frame]
			self.dirty = 1

	def play_animation(self, frames_key: str=None, loops: int=-1) -> object:

		self.frames_key = frames_key
		return Sprite.play_animation(self, loops)
