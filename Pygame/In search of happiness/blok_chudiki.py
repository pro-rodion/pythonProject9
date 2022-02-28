from pygame import *
import blok_ganim
import os

ChUDIKOV_ShIRINA = 2 ** 5
ChUDIKOV_VYSOTA = 2 ** 5
ChUDIKOV_TsVET = "#0000ff"
ICON_DIR = os.path.dirname(__file__)  # путь к каталогу


ANIMATION_MONSTERHORYSONTAL = [('%s/zlyuki/zlyuka001.png' % ICON_DIR),
                               ('%s/zlyuki/zlyuka002.png' % ICON_DIR )]

class chudiki(sprite.Sprite):
    def __init__(self, x, y,
                 leviy, up,
                 Maksimalnaya_dlina_sleva,
                 Maksimalnaya_dlina_Vverkh):
        sprite.Sprite.__init__(self)

        self.image = Surface((ChUDIKOV_ShIRINA,
                              ChUDIKOV_VYSOTA))
        self.image.fill(Color(ChUDIKOV_TsVET))

        self.rect = Rect(x, y, ChUDIKOV_ShIRINA,
                         ChUDIKOV_VYSOTA)
        self.image.set_colorkey(Color(ChUDIKOV_TsVET))

        self.startX = x # начальные координаты
        self.startY = y

        self.maxLengthLeft = Maksimalnaya_dlina_sleva
        self.maxLengthUp = Maksimalnaya_dlina_Vverkh
        self.velx = leviy
        self.vely = up

        boltAnim = []

        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))

        self.boltAnim = blok_ganim.PygAnimation(boltAnim)
        self.boltAnim.play()
         
    def update(self, platformy):
        self.image.fill(Color(ChUDIKOV_TsVET))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.vely
        self.rect.x += self.velx

        self.stalkivatsya(platformy)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.velx =- self.velx

        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.vely =- self.vely

    def stalkivatsya(self, platformy):
        for t in platformy:
            if sprite.collide_rect(self, t) and self != t:
               self.velx =- self.velx
               self.vely =- self.vely
