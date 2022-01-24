import pygame, gameslib

class Score(pygame.sprite.DirtySprite):

	def __init__(self, source: pygame.Surface, pos: gameslib.Pos=(0, 0), value: int=0, digits: int=2, lead_zeros: bool=True, frames: gameslib.Rects=[], colorkey: gameslib.Color=None, bg_color: gameslib.Color=(0, 0, 0, 0), scale: int=1) -> None:
		pygame.sprite.DirtySprite.__init__(self)

		self._source = source
		self._pos = pos
		self._value = 0
		self._digits = digits
		self._lead_zeros = lead_zeros
		self._frames = frames
		self._colorkey = colorkey
		self._bg_color = bg_color
		self._scale = scale

		self.value = value

	@property
	def value(self) -> int:
		return self._value

	@value.setter
	def value(self, value:int) -> None:

		if self._value == value:
			return

		self._value = value

		w, h = 0, 0
		str_value = str(value).zfill(self._digits) if self._lead_zeros else str(value)
		rects = []
		for c in str_value:
			i = int(c)
			_, _, fw, fh = self._frames[i]
			rects.append(self._frames[i])

			if fh > h:
				h = fh

			w += fw

		x= 0
		self.image = gameslib.create_image((w, h), self._colorkey, self._bg_color)
		for rect in rects:
			_, _, fw, _ = rect
			self.image.blit(self._source, (x, 0), rect)
			x += fw

		self.image = gameslib.scale_image(self.image, self._scale)
		self.rect = pygame.Rect(gameslib.scale_pos(self._pos, self._scale), self.image.get_size())
		self.dirty = 1



