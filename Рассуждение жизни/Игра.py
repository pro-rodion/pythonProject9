
import pygame
from igrok import *
from blocki import *

W = 800
H = 640

ikon = (W, H)
COL = "#000000"

class Camera(object):
    def __init__(self, _f, w, h):

        self.camera_func = _f
        self.state = Rect(0, 0, w, h)

    def apply(self, target):

        return target.rect.move(self.state.topleft)

    def update(self, target):

        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(me, t_r):
    ll, tt, _, _ = t_r
    _, _, www, hhh = me

    l, t = -ll + W / 2, -tt + H / 2

    l = min(0, l)
    l = max(-(me.width - W), l)
    t = max(-(me.height - H), t)
    t = min(0, t)

    return Rect(l, t, www, hhh)


def main():
    pygame.init()
    er = pygame.display.set_mode(ikon)

    pygame.display.set_caption("Рассуждение жизни")
    gh = Surface((W, H))

    gh.fill(Color(COL))
    
    hero = Player(50, 50
                  )
    left = right = False
    up = False
    
    jk = pygame.sprite.Group()
    platforms = []
    
    jk.add(hero)
           
    ty = [
       "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
       "&                                &",
       "&                 &&&            &",
       "&                                &",
       "&                                &",
       "&                                &",
       "&                                &",
       "&         &&                     &",
       "&                                &",
       "&                                &",
       "&                                &",
       "&                    &&          &",
       "&                                &",
       "&            &&                  &",
       "&                       &&       &",
       "&                                &",
       "&                                &",
       "&    &&                &&        &",
       "&                                &",
       "&                                &",
       "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"]
       
    ui = pygame.time.Clock()
    x = y = 0
    for DF in ty:
        for col in DF:
            if col == "&":
                pf = Platform(x, y)
                jk.add(pf)
                platforms.append(pf)

            x += platforma1
        y += platforma2
        x = 0
    fg = len(ty[0]) * platforma1

    hj = len(ty) * platforma2
    
    camera = Camera(camera_configure, fg, hj)
    
    while 1:
        ui.tick(60)
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True

            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True


            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        er.blit(gh, (0, 0))


        camera.update(hero)
        hero.update(left, right, up,platforms)
        for e in jk:

            er.blit(e.image, camera.apply(e))
        
        pygame.display.update()
        

if __name__ == "__main__":
    main()
