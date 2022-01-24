##	GamesLib - Games library, based on PyGame
##
##	This program is free software: you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation, either version 3 of the License, or
##	(at your option) any later version.
##
##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.
##
##	You should have received a copy of the GNU General Public License
##	along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Library with basic objects to make Games

This library is based on pygame <https://github.com/pygame>.
"""

# Python dependencies:
# if proxy: set https_proxy=http://xxxx.xxxxxx.xxxx:8080
# pip install pygame
# or
# python -m pip install -U pygame --user

import pygame

pygame.init()
#pygame.font.init()
#pygame.mixer.init()
#pygame.joystick.init()

# Library defined types
RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
Color = RGB | RGBA

Pos = tuple[int, int]
Size = tuple[int, int]
Rect = tuple[int, int, int, int]
Rects = list[Rect]

from .tools import *

from .app import *
from .scene import *
from .sprite import *
from .score import *
from .text import *

print('GamesLib 1.0')
