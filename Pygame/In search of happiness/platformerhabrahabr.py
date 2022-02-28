import pygame
from pygame import *
from blok_igrok import *
from blok_bloki import *
from blok_chudiki import *


WIN_WIDTH = 1080  # Ширина
WIN_HEIGHT = 720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)# Не дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)# Не дальше левой границы

    t = max(-(camera.height-WIN_HEIGHT), t)# Не дальше левой границы
    t = min(0, t)# Не дальше левой границы

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY#координаты героя

    levelFile = open('%s/uroven.txt' % FILE_DIR)
    line = " "
    commands = []

    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":

            while line[0] != "]":
                line = levelFile.readline()

                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])

        if line[0] != "":
            commands = line.split()

            if len(commands) > 1:
                if commands[0] == "Koordinaty_igroka":
                    playerX = int(commands[1])
                    playerY = int(commands[2])

                if commands[0] == "Teleport":
                    tp = BlockTeleport(int(commands[1]), int(commands[2]),
                                       int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)
                    animatedEntities.add(tp)

                if commands[0] == "Zlyuki":
                    mn = chudiki(int(commands[1]), int(commands[2]),
                                 int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


def main():
    loadLevel()
    pygame.init()  # Инициация PyGame

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("В поисках счастья")

    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    left = right = False  # изночально - стоим
    up = False
    running = False

    hero = Player(playerX, playerY)
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "/":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            if col == "?":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)

            if col == "C":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH

        y += PLATFORM_HEIGHT
        x = 0

    total_level_width = len(level[0])*PLATFORM_WIDTH#Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:
        timer.tick(60)

        for n in pygame.event.get():
            if n.type == KEYDOWN and n.key == K_UP:
                up = True

            if n.type == KEYDOWN and n.key == K_LEFT:
                left = True

            if n.type == KEYDOWN and n.key == K_RIGHT:
                right = True

            if n.type == KEYDOWN and n.key == K_LSHIFT:
                running = True

            if n.type == KEYUP and n.key == K_UP:
                up = False

            if n.type == KEYUP and n.key == K_RIGHT:
                right = False

            if n.type == KEYUP and n.key == K_LEFT:
                left = False

            if n.type == KEYUP and n.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))

        animatedEntities.update()
        monsters.update(platforms)

        camera.update(hero)
        hero.update(left, right, up, running, platforms)

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()# обновление и вывод на экран


level = []
entities = pygame.sprite.Group()

animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()

platforms = []

if __name__ == "__main__":
    main()
