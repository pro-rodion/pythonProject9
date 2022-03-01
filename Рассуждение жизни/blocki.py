from pygame import *
import os

platforma1 = 31
platforma2 = 32

platformatsvet = "#444444"
ICON_DIR = os.path.dirname(__file__)
 
class Platform(sprite.Sprite):
    def __init__(self, iks, igrek):
        sprite.Sprite.__init__(self)

        self.image = Surface((platforma1, platforma2))

        self.image.fill(Color(platformatsvet))

        self.image = image.load("%s/bloki/oblako.png" % ICON_DIR)
        self.rect = Rect(iks, igrek, platforma1, platforma2)
