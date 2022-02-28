from pygame import *
import blok_ganim
import os
import blok_bloki
import blok_chudiki

MOVE_SPEED = 10
MOVE_EXTRA_SPEED = 9.81 # ускорение как на земле
WIDTH = 32
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 12
JUMP_EXTRA_POWER = 1  # дополнительная сила прыжка
GRAVITY = 0.4 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.09 # скорость смены кадров
ANIMATION_SUPER_SPEED_DELAY = 1 # скорость смены кадров при ускорении
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

ANIMATION_RIGHT = [('%s/efimova/r1.png' % ICON_DIR),
            ('%s/efimova/r2.png' % ICON_DIR),
            ('%s/efimova/r3.png' % ICON_DIR),
            ('%s/efimova/r4.png' % ICON_DIR),
            ('%s/efimova/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/efimova/l1.png' % ICON_DIR),
            ('%s/efimova/l2.png' % ICON_DIR),
            ('%s/efimova/l3.png' % ICON_DIR),
            ('%s/efimova/l4.png' % ICON_DIR),
            ('%s/efimova/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/efimova/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/efimova/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/efimova/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/efimova/0.png' % ICON_DIR, 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   # скорость перемещения 0
        self.startX = x # Начальная позиция Х
        self.startY = y
        self.yvel = 0 # скорость верт. перемещения
        self.onGround = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR))
#        Аним. движ. вправо
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = blok_ganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = blok_ganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
#        Аним.я движ. влево
        boltAnim = []
        boltAnimSuperSpeed = [] 
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = blok_ganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = blok_ganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()
        
        self.boltAnimStay = blok_ganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # По-умолчанию, стоим
        
        self.boltAnimJumpLeft = blok_ganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight = blok_ganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump = blok_ganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False
        

    def update(self, left, right, up, running, platforms):
        
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться
                self.yvel = -JUMP_POWER
                if running and (left or right):
                       self.yvel -= JUMP_EXTRA_POWER
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
                       
        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running: # если уск.
                self.xvel-=MOVE_EXTRA_SPEED # то перед. быстрее
                if not up: # и если не прыг.
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0)) # то отображаем анимацию
            else: # если не бежим
                if not up: # и не прыгаем
                    self.boltAnimLeft.blit(self.image, (0, 0)) # отображаем аним. движ.
            if up: # если же прыгаем
                    self.boltAnimJumpLeft.blit(self.image, (0, 0)) # отображаем аним. прыжка
 
        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if running:
                self.xvel+=MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0)) 
            if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
 
         
        if not(left or right):  # стоим
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False;
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
   
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, blok_bloki.BlockDie) or isinstance(p, blok_chudiki.chudiki):
                       self.die()# умир.
                elif isinstance(p, blok_bloki.BlockTeleport):
                       self.teleporting(p.goX, p.goY)
                elif isinstance(p, blok_bloki.Princess): # если коснулись монеты
                       self.winner = True # победили
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
        
    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY) # перемещаемся в нач. коорд.