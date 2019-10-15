import pygame
import os
import time
import random


class Sparki:
    def __init__(self):
        self._rows = 4
        self._columns = 4
        self._jewel_size = 50
        self._window_width = (self._jewel_size * self._columns)
        self._window_height = (self._jewel_size * self._rows)
        self.field = [[0 for j in range(self._columns)] for i in range(self._rows)]
        self._colors = ['BLACK',
                        '#800000', 
                        '#FFD700', 
                        '#228B22', 
                        '#008080', 
                        '#191970', 
                        '#9932CC', 
                        '#DB7093']
        pygame.init()
        pygame.display.set_caption('Sparki')

        self._surface = pygame.display.set_mode([self._window_width, self._window_height])
        

    def paint(self):

        size = self._jewel_size
        for i in range(0, self._rows):
            for j in range(0, self._columns):
                # print (self._colors[self.field[i][j]])
                pygame.draw.rect(self._surface, pygame.Color(self._colors[self.field[i][j]]), (j*size, i*size, size, size))

                    # print(self.fallhead[0] - i)
        pygame.display.flip()

    # def move_left(self):
    # def move_right(self):
    # def rotate(self):
    # def event(self):

    def inrange(self, x, y):
        return 0 <= x and x < self._rows and 0 <= y and y < self._columns

    # def check(self):
    def run(self):
        while (self.ison()):
            pygame.time.delay(200);
            if (len(self.fallhead) == 0):
                self.generate_fall()
            self.event();
            if (self.fallhead[0]+1 < self._rows and self.field[self.fallhead[0]+1][self.fallhead[1]] == 0): # zero means black
                print(self.fallhead)
                self.fallhead[0] += 1
            elif (self.fallhead[0]+1 >= self._rows or self.field[self.fallhead[0]+1] != 0):
                for i in range(0, 3):
                    self.field[self.fallhead[0]-i][self.fallhead[1]] = self.fallcolor[i]
                self.fallhead = []

                while (self.check()):
                    self.paint()
                    pygame.time.delay(200);
                    self.fall()
                    self.paint()
                    pygame.time.delay(200);
            self.paint()

        pygame.quit()

        
    def test(self):
        for i in range(0, self._rows):
            for j in range(0, self._columns):
                self.field[i][j] = random.randint(0, len(self._colors)-1)
                print(self.field[i][j], end = ' ')
            print('')
        self.paint()


    


if __name__ == '__main__':
    game = Sparki() 
    game.test()

