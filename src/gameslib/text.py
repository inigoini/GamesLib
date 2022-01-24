import pygame, gameslib

class Text(pygame.sprite.DirtySprite):

	def __init__(self, source: pygame.Surface, pos: gameslib.Pos=(0, 0), text: str='', frames: dict[str: gameslib.Rect]={}, space_width: int=8, colorkey: gameslib.Color=None, bg_color: gameslib.Color=(0, 0, 0, 0), scale: int=1) -> None:
		pygame.sprite.DirtySprite.__init__(self)

		self._source = source
		self._pos = pos
		self._text = None
		self._frames = frames
		self._space_width = space_width
		self._colorkey = colorkey
		self._bg_color = bg_color
		self._scale = scale

		self.text = text

	@property
	def text(self) -> int:
		return self._text

	@text.setter
	def text(self, text:int) -> None:

		if self._text == text:
			return

		self._text = text

		w, h = 0, 0
		rects = []
		for c in text:

			if c in self._frames:
				_, _, fw, fh = self._frames[c]
				rects.append(self._frames[c])

				if fh > h:
					h = fh

			else:
				rects.append(' ')
				fw = self._space_width

			w += fw

		x= 0
		self.image = gameslib.create_image((w, h), self._colorkey, self._bg_color)
		for rect in rects:

			if rect == ' ':
				fw = self._space_width

			else:
				_, _, fw, _ = rect
				self.image.blit(self._source, (x, 0), rect)
			x += fw

		self.image = gameslib.scale_image(self.image, self._scale)
		self.rect = pygame.Rect(gameslib.scale_pos(self._pos, self._scale), self.image.get_size())
		self.dirty = 1
