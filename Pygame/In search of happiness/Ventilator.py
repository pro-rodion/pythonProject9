import pygame
import math


class Vent:
    def __init__(self, canvas, center=101,
                 angle=105, line=70):
        self.start_pos = center
        self.length = line

        self.angle = angle
        self.speed = 0

        self.canvas = canvas

    def update(self):
        self.angle = (self.angle + self.speed) % 360
        left_point = ((self.start_pos + math.cos(self.angle * math.pi / 180) * self.length),
                      (self.start_pos + math.sin(self.angle * math.pi / 180) * self.length))

        right_point = ((self.start_pos + math.cos((self.angle - 30) * math.pi / 180) * self.length),
                       (self.start_pos + math.sin((self.angle - 30) * math.pi / 180) * self.length))
        center_point = (self.start_pos,
                        self.start_pos)

        pygame.draw.polygon(self.canvas, (255, 255, 255),
                            (center_point,
                             left_point,
                             right_point))

    def change_speed(self, event):
        if event.button == 1:
            self.speed += 1

        elif event.button == 3:
            self.speed -= 1


pygame.init()
SIZE = (201, 201)
screen = pygame.display.set_mode(SIZE)
vents = []

for angle in range(105, 361, 120):
    vent = Vent(screen, angle=angle)
    vents.append(vent)
clock = pygame.time.Clock()


if __name__ == '__main__':
    running = True
    while running:
        screen.fill((0, 0, 0))

        pygame.draw.circle(screen, color=(255, 255, 255),
                           center=(101, 101), radius=10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                [vent.change_speed(event) for vent in vents]
        [vent.update() for vent in vents]
        clock.tick(50)
        pygame.display.flip()