import pygame

class Score(pygame.sprite.DirtySprite):

	def __init__(self, source: pygame.Surface, frames: list, pos: tuple=(0, 0), value: int=0, digits: int=2, leading_zeros: bool=True, scale: int = 1) -> None:
		pygame.sprite.DirtySprite.__init__(self)

		self._source = source
		self._frames = frames
		self._value = 0
		self._digits = digits
		self._leading_zeros = leading_zeros
		self._scale = scale

		self.image = source
		_, _, w, h = source.get_rect()
		self.rect = pygame.Rect(pos, (w, h))

		self.value = value

	@property
	def value(self) -> int:
		return self._value

	@value.setter
	def value(self, value:int) -> None:
		self._value = value

		frame_digits = []
		score = str(value).zfill(self.digits) if self.leading_zeros else str(value)
		for c in score:
			i = int(c)
			frame_digits.append(self._frames[i])

		w, h = 0
		for frame in frame_digits:
			_, _, fw, fh = frame
			w += fw

			if fh > h:
				h = fh

		image = gameslib.create_image((w, h))
		x = 0
		for frame in frame_digits:
			image.blit(self._source, (x, 0), frame)
			_, _, fw, _ = frame
			x += fw

		self.image = image
		self.rect = pygame.Rect(self._pos, (w, h))

	@property
	def digits(self) -> int:
		return self._digits

	@property
	def leading_zeros(self) -> bool:
		return self._leading_zeros
