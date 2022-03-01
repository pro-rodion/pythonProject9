from pygame import *

import gnat

import os

skorost = 10

vidkh = 30

khayt = 30
COLOR = "#000000"

zaryadpryzhka = 10
prityazh = 0.1
delat = 60

ikon = os.path.dirname(__file__)

RIGHT = [('%s/efimova/r001.png' % ikon),

            ('%s/efimova/r002.png' % ikon),
            ('%s/efimova/r003.png' % ikon),
            ('%s/efimova/r004.png' % ikon),
            ('%s/efimova/r005.png' % ikon)]

LEFT = [('%s/efimova/l001.png' % ikon),
            ('%s/efimova/l002.png' % ikon),

            ('%s/efimova/l003.png' % ikon),
            ('%s/efimova/l004.png' % ikon),
            ('%s/efimova/l005.png' % ikon)]
JUMP_LEFT = [('%s/efimova/j00l.png' % ikon, 0.1)]

JUMP_RIGHT = [('%s/efimova/j00r.png' % ikon, 0.1)]
JUMP = [('%s/efimova/j00.png' % ikon, 0.1)]
STAY = [('%s/efimova/000.png' % ikon, 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = Surface((vidkh, khayt))

        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, vidkh, khayt)
        self.image.set_colorkey(Color(COLOR))
        bolt = []
        for anim in RIGHT:
            bolt.append((anim, delat))
        self.boltAnimRight = gnat.sdf(bolt)
        self.boltAnimRight.play()
        bolt = []

        for anim in LEFT:
            bolt.append((anim, delat))

        self.boltAnimLeft = gnat.sdf(bolt)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = gnat.sdf(STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        
        self.boltAnimJumpLeft = gnat.sdf(JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight = gnat.sdf(JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump = gnat.sdf(JUMP)
        self.boltAnimJump.play()


    def collide(self, xvel, VV, VB):
        for p in VB:

            if sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if VV > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True

                    self.yvel = 0

                if VV < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        

    def update(self, le, ri, p, forms):
        
        if p:
            if self.onGround:
                self.yvel = - zaryadpryzhka

            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
               
                       
        if le:
            self.xvel = - skorost
            self.image.fill(Color(COLOR))
            if p:

                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
 
        if ri:
            self.xvel = skorost
            self.image.fill(Color(COLOR))
            if p:

                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
         
        if not(le or ri):
            self.xvel = 0
            if not p:

                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel += prityazh
            
        self.onGround = False
        self.rect.y += self.yvel

        self.collide(0, self.yvel, forms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, forms)