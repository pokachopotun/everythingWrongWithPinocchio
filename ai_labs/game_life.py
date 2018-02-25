from cv2 import *
import os
import numpy as np

class gameLife:
    def __init__(self):
        self.height, self.width = self.init_dialogue()
        self.adjust_header = "Game Life. q - start; wasd - navigate; enter - set cell/remove"
        self.play_header = "Game Life. q - quit; space - pause/start"
        self.delay = 1
        self.pixels_per_cell = 20
        self.pixels_border = 4
        self.species_count = 3
        self.creature_colors = [0, 150, 255]
        self.cell_selector_color = 127
        self.border_color = 64
        #print( self.height, self.width )
        self.create_field()
        self.create_field_image()
        self.adjust()
        self.play()

    def create_field(self):

        self.field = np.zeros((self.height, self.width, 1), np.uint8)

    def create_field_image(self):
        self.image_height = self.height * self.pixels_per_cell + self.pixels_border * (self.height + 1)
        self.image_width = self.width * self.pixels_per_cell + self.pixels_border * (self.width + 1)

        self.field_image = np.zeros((self.image_height, self.image_width, 1), np.uint8)

        self.draw_cells()

        # self.set_cell(20, 20, 255)
        # self.set_cell_selector(10, 10, 127)





    def set_cell(self, x, y, val):
        if(val < 0 or val >= 256):
            raise("value should be of [0, 255] range")
        x_st = x * (self.pixels_border + self.pixels_per_cell) + self.pixels_border
        x_f = (x + 1) * (self.pixels_border + self.pixels_per_cell)
        y_st = y * (self.pixels_border + self.pixels_per_cell) + self.pixels_border
        y_f = (y + 1) * (self.pixels_border + self.pixels_per_cell)
        self.field_image[x_st : x_f, y_st : y_f] = val

    def set_cell_selector(self, x, y, val):
        if(val < 0 or val > 255):
            raise("value should be of [0, 255] range")
        #left
        x_st = x * (self.pixels_border + self.pixels_per_cell)
        x_f = (x + 1) * (self.pixels_border + self.pixels_per_cell) + self.pixels_border

        y_st = y * (self.pixels_border + self.pixels_per_cell)
        y_f = y_st + self.pixels_border

        self.field_image[x_st : x_f, y_st : y_f] = val

        # upper
        x_st = x * (self.pixels_border + self.pixels_per_cell)
        x_f = x_st + self.pixels_border

        y_st = y * (self.pixels_border + self.pixels_per_cell)
        y_f = (y + 1) * (self.pixels_border + self.pixels_per_cell) + self.pixels_border

        self.field_image[x_st: x_f, y_st: y_f] = val

        # lower
        x_st = (x + 1) * (self.pixels_border + self.pixels_per_cell)
        x_f = x_st + self.pixels_border

        y_st = y * (self.pixels_border + self.pixels_per_cell)
        y_f = (y + 1) * (self.pixels_border + self.pixels_per_cell) + self.pixels_border

        self.field_image[x_st: x_f, y_st: y_f] = val

        # right
        x_st = x * (self.pixels_border + self.pixels_per_cell)
        x_f = (x + 1) * (self.pixels_border + self.pixels_per_cell) + self.pixels_border

        y_st = (y + 1) * (self.pixels_border + self.pixels_per_cell)
        y_f = y_st + self.pixels_border

        self.field_image[x_st: x_f, y_st: y_f] = val

    def draw_cells(self):
        for i in range(self.height + 1):
            for j in range(self.pixels_border):
                self.field_image[i * (self.pixels_per_cell + self.pixels_border) + j, :] = self.border_color

        for i in range(self.width + 1):
            for j in range(self.pixels_border):
                self.field_image[: , i * (self.pixels_per_cell + self.pixels_border) + j] = self.border_color


    def move_cell_selector(self, x, y, dx, dy):
        if(dx >= self.height or dx < 0):
            return False
        if (dy >= self.width or dy < 0):
            return False
        self.set_cell_selector(x,y, self.border_color)
        self.set_cell_selector(dx, dy, self.cell_selector_color)
        return True

    def adjust(self):
        x,y = (0, 0)
        self.set_cell_selector(x,y, self.cell_selector_color)
        while(True):
            imshow(self.adjust_header, self.field_image)
            c = waitKey(self.delay)
            #print("key " + str(c))
            if(c == 13):
                self.field[x][y] = (self.field[x][y] + 1) % self.species_count
                #print(self.creature_colors[int(self.field[x][y])])
                self.set_cell(x, y, self.creature_colors[int(self.field[x][y])])
            if(c == ord('w') or c == ord('W')):
                if( self.move_cell_selector(x,y, x - 1, y)):
                    x = x - 1

            if (c == ord('s') or c == ord('S')):
                if(self.move_cell_selector(x, y, x + 1, y)):
                    x = x + 1

            if (c == ord('a') or c == ord('A')):
                if(self.move_cell_selector(x, y, x, y - 1)):
                    y = y - 1

            if (c == ord('d') or c == ord('D')):
                if(self.move_cell_selector(x, y, x, y + 1)):
                    y = y + 1

            if(c == ord('q') or c == ord('Q')):
                self.set_cell_selector(x,y, self.border_color)
                destroyWindow(self.adjust_header)
                break
            # if(c == ord(' ')):
            #     self.delay = ( self.delay + 1 ) % 2

    def select_rule(self, val, cnt):
        if(val == 2):
            return 2
        if(val == 1):
            if(cnt < 2 or cnt > 3):
                return 0
            else:
                return 1
        if(val == 0):
            if(cnt == 3):
                return 1
            return 0

    def update_field(self):
        new_field = np.zeros((self.height, self.width, 1), np.uint8)
        for x in range(self.height):
            for y in range(self.width):
                st_x = x - 1
                f_x = x + 1
                st_y = y - 1
                f_y = y + 1

                for i in range(st_x, f_x + 1):
                    for j in range(st_y, f_y + 1):
                        if(st_x + 1 == i and st_y + 1 == j):
                            continue
                        new_field[x][y] += int(self.field[(i + self.height) % self.height][(j + self.width) % self.width] > 0)
                #print(x, y, st_x, f_x, st_y, f_y)
        for x in range(self.height):
            for y in range(self.width):
                new_field[x][y] = self.select_rule(self.field[x][y], new_field[x][y])
        self.field = new_field


    def update_field_image(self):
        for x in range(self.height):
            for y in range(self.width):
                self.set_cell(x,y, self.creature_colors[int(self.field[x][y])])

    def play(self):
        while(True):
            self.update_field()
            self.update_field_image()
            imshow(self.play_header, self.field_image)
            c = waitKey(self.delay)
            #print("key " + str(c))
            if(c == ord('q') or c == ord('Q')):
                destroyWindow(self.play_header)
                break
            if(c == ord(' ')):
                self.delay = ( self.delay + 1 ) % 2




    def init_dialogue(self):
        print("Specify field size in format height width")
        h,w = input().strip().split()
        return (int(h), int(w))


if __name__ == "__main__":
    game = gameLife()