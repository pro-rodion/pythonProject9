import pygame


class Board:
    def __init__(self, height, width):
        self.board = [[0] * width for _ in range(height)]

        self.width = width
        self.height = height

        self.left = 10
        self.top = 10

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self, scr):
        new_board = [[0] * self.width for _ in range(self.height)]
        for i in range(len(self.board)):

            for j in range(len(self.board[i])):
                a = self.nine_([i, j])

                if self.board[i][j] == 0:
                    if a == 3:

                        new_board[i][j] = 1
                else:

                    if a in [2, 3]:
                        new_board[i][j] = 1

        self.board = new_board
        self.upd(scr)

    def upd(self, scr):
        scr.fill((0, 0, 0))

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):

                pygame.draw.rect(scr, (60, 60, 60), (i * self.left, j * self.top, self.left + 1, self.top + 1), 1)
                if self.board[i][j] == 1:

                    pygame.draw.rect(scr, (0, 255, 0), (1 + i * self.left, 1 + j * self.top, self.left - 1, self.top - 1))

    def get_cell(self, pos):
        x, y = pos

        x, y = x // self.left, y // self.top
        return (x, y)

    def get_click(self, mouse_pos, scr):
        try:
            scr.fill((0, 0, 0))

            cell = self.get_cell(mouse_pos)
            self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2
        except IndexError:

            pass

    def nine_(self, pos):
        l = 0
        for i in range(3):

            for j in range(3):
                if not i == j == 1:
                    x, y = pos[0] + i - 1, pos[1] + j - 1
                    if x >= 50:
                        x = x - 50

                    if y >= 50:
                        y = y - 50
                    if x < 0:
                        x = 49
                    if y < 0:

                        y = 49
                    if (x >= 0 and y >= 0) and (x < 50 and y < 50):
                        if self.board[x][y] == 1:
                            l += 1
        return l


pygame.init()
ty = pygame.display.set_mode((501, 501))
board = Board(50, 50)
pygame.display.set_caption("Тренировка с созданием карты")

board.set_view(10, 10)
er = True

board.render(ty)
tick = pygame.time.Clock()
q = 1
speed = 100
while er:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            er = False
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            q = (q + 1) % 2
        if q and event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                board.get_click(event.pos, ty)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                speed *= 1.5

                if speed > 60:
                    speed = 60
            if event.button == 5:
                speed = speed // 1.5

                if speed < 1:
                    speed = 1
    if not q:
        board.render(ty)
        pygame.display.flip()
        tick.tick(int(speed // 2))

    else:
        board.upd(ty)
        pygame.display.flip()

        tick.tick(int(speed))