import numpy as np
import pygame
import matplotlib.image as plt

pygame.init()
pygame.font.init()

img = plt.imread("Mistère 2.png")

font_offset = 3


class Grid():

    def __init__(self, rows, cols, width, height, screen, img):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.grid = np.array((width, height))
        self.screen = screen
        self.maxy = 0
        self.maxx = 0
        self.marge = -20
        self.infoRows = ["" for i in range(max(rows, img.shape[0]))]
        self.infoCols = ["" for i in range(max(cols, img.shape[1]))]
        self.NumRows = [0 for i in range(len(self.infoRows))]
        self.NumCols = [0 for i in range(len(self.infoCols))]
        self.convert(img)
        self.fontsize = 15
        self.offsetx = 50
        self.offsety = 0

    def is_maxx(self, lenght):
        if lenght >= self.maxx:
            self.maxx = lenght

    def is_maxy(self, height):
        if height >= self.maxy:
            self.maxy = height

    def draw(self):
        self.gap = min((self.width - self.maxx) / self.rows,
                       (self.height - self.maxy) / self.cols)

        if self.fontsize*1.333 > self.gap:
            self.fontsize -= 1
            self.maxx, self.maxy = 0, 0
        elif self.fontsize*1.333 < self.gap/2:
            self.fontsize += 1
        font = pygame.font.SysFont("Arial", self.fontsize + font_offset)
        size = (0, 0)

        # Dessine la Grille
        for i in range(self.rows):
            if i % 5 == 0:
                thick = 2
            else:
                thick = 1
            self.NumRows[i] = font.render(
                str(self.infoRows[i]+" "), 1, (0, 0, 0))
            size = self.NumRows[i].get_size()
            self.is_maxx(size[0])
            self.screen.blit(self.NumRows[i], (int(self.offsetx +
                                                   self.maxx - size[0]), int(self.offsety + self.maxy + i*self.gap)))
            pygame.draw.line(self.screen, (0, 0, 0), (int(self.maxx + self.offsetx), int(
                self.offsety + self.maxy + i*self.gap)), (int(self.offsetx + self.cols * self.gap + self.maxx), int(self.offsety + self.maxy + i*self.gap)), thick)

        pygame.draw.line(self.screen, (0, 0, 0), (int(self.offsetx + self.maxx), int(
            self.offsety + self.maxy + self.rows*self.gap)), (int(self.offsetx + self.cols * self.gap + self.maxx), int(self.offsety + self.maxy + self.rows*self.gap)), thick)

        for i in range(self.cols):
            if i % 5 == 0:
                thick = 2
            else:
                thick = 1
            Slignes, y = saut_ligne(self.fontsize, self.screen, self.infoCols[i], int(self.offsetx +
                                                                                      self.maxx + i * self.gap + self.gap/2), int(self.offsety + self.maxy))
            self.is_maxy(y)
            pygame.draw.line(self.screen, (0, 0, 0), (int(self.offsetx + self.maxx + i * self.gap), int(self.offsety + self.maxy)),
                             (int(self.offsetx + self.maxx + i * self.gap), int(self.rows * self.gap + self.maxy + self.offsety)), thick)
        pygame.draw.line(self.screen, (0, 0, 0), (int(self.offsetx + self.maxx + self.cols * self.gap), int(self.maxy + self.offsety)),
                         (int(self.offsetx + self.maxx + self.cols * self.gap), int(self.rows * self.gap + self.maxy + self.offsety)), thick)

    def read_row(self, row, id):
        bloc = False
        lenght = 0
        n = len(row)
        for i in range(n):

            if row[i, 0] == 0:
                bloc = True
                lenght += 1
            elif bloc == True:
                self.infoRows[id] += " " + str(lenght)
                lenght = 0
                bloc = False
            if i == n - 1 and lenght != 0:
                self.infoRows[id] += " " + str(lenght)

    def read_cols(self, col, id):
        bloc = False
        lenght = 0
        n = len(col)
        for i in range(n):
            if col[i, 0] == 0:
                bloc = True
                lenght += 1
            elif bloc == True:
                self.infoCols[id] += "\n" + str(lenght)
                lenght = 0
                bloc = False
            if i == n - 1 and lenght != 0:
                self.infoCols[id] += " " + str(lenght)

    def convert(self, img):
        for i in range(img.shape[0]):
            self.read_row(img[i], i)
        for j in range(img.shape[1]):
            self.read_cols(img[:, j], j)


def saut_ligne(fontsize, screen, text, x0, y0):
    lignes = text.split("\n")
    font = pygame.font.SysFont("Arial", fontsize + font_offset)
    Surflignes = [font.render(str(lignes[i]), 1, (0, 0, 0))
                  for i in range(len(lignes))]
    size = (0, 0)
    x, y = x0, y0
    for ligne in Surflignes:
        size = ligne.get_size()
        # x = x0 - size[0]/2 + 2
        y += size[1]
    d = y - y0
    y = y0 - d
    for ligne in Surflignes:
        size = ligne.get_size()
        screen.blit(ligne, (x - size[0]/2, y))
        y += size[1]
    return Surflignes, d


def redraw_window(screen, board, clock):
    screen.fill((255, 255, 255))
    board.draw()


def main(width, height, rows, cols, img):
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    FPS = 60
    clock.tick(FPS)
    run = True

    board = Grid(rows, cols, width, height, screen, img)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.image.save(screen, "screenshot.jpeg")
                    print("Saved !")
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
                pygame.display.set_mode(
                    (width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

        redraw_window(screen, board, clock)
        pygame.display.update()


main(1366, 1000, 53, 129, img)

pygame.quit()
