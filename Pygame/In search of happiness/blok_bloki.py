from pygame import *
import os
import blok_ganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__) # Полный путь к каталогу с файлами

ANIMATION_BLOCKTELEPORT = [
            ('%s/bloki/Teleport001.png' % ICON_DIR),
            ('%s/bloki/Teleport002.png' % ICON_DIR)]
            
ANIMATION_PRINCESS = [
            ('%s/bloki/Coin001.png' % ICON_DIR),
            ('%s/bloki/Coin002.png' % ICON_DIR)]
            
 
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/bloki/oblako.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/bloki/vonyuchka.png" % ICON_DIR)

class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения
        boltAnim = []
        for anim in ANIMATION_BLOCKTELEPORT:
            boltAnim.append((anim, 0.3))
        self.boltAnim = blok_ganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        
class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_PRINCESS:
            boltAnim.append((anim, 0.8))
        self.boltAnim = blok_ganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        
    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))