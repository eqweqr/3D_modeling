from math import sin, cos, pi
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def bresenham_line(x0: int, y0: int, x1: int, y1: int, image):
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    diff = 1

    # Смена координат в случае, если начальная координата дальше по оси х, чем конечная
    if(x0 - x1 > 0):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Проверка на убывание
    if(y0 - y1 > 0):
        diff = -1

    # Если угол меньше или равно 45, то увеличиваем/уменьшаем координату y
    if(delta_x >= delta_y):
        y_i = y0
        for x in range(x0, x1 + 1):
            image.putpixel((x, y_i))
            error = error + 2 * delta_y
            if error >= delta_x:
                y_i += diff
                error -= 2 * delta_x
    # Иначе - по координате x
    elif(delta_x < delta_y):
        # Обработка особого случая
        if(diff == -1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        x_i = x0
        for y in range(y0, y1 + 1):
            image.putpixel((x_i, y))
            error = error + 2 * delta_x
            if error >= delta_y:
                x_i += diff
                error -= 2 * delta_y
            

def ChangeVector(change_matrix: list, vector: list):
    new_vector = [0]*len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return new_vector


def get_vector(dots: list):
    return [dots[0], dots[1], dots[2], 1]


def ToRadian(angle: float):
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0):
    return [[1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0):
    return [[kx, 0, 0, 0],
            [0, ky, 0, 0],
            [0, 0, kz, 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_X(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)
        
    return  [[1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_Y(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)

    return [[cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]]


def get_rotate_matrix_Z(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)

    return [[cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0 , 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

def is_visible(dots, fig: list):
    xa, ya, za = dots[fig[0]-1][0], dots[fig[0]-1][1], dots[fig[0]-1][2]
    xb, yb, zb = dots[fig[1]-1][0], dots[fig[1]-1][1], dots[fig[1]-1][2]
    xc, yc, zc = dots[fig[2]-1][0], dots[fig[2]-1][1], dots[fig[2]-1][2]

    # A = (yb-ya)*(zc-za) - (zb-za)*(yc-ya)
    # B = (xc-xa)*(zb-za) - (xb-xa)*(zc-za)
    C = (xb-xa)*(yc-ya) - (yb-ya)*(xc-xa)

    if (C < 0): return False

    return True

def roggers_clipper(obj_file, image : Image):
# функция отсечения невидимых граней по алгоритму Роджерса
#
# параметры:
#
# возвращаемое значение
#
    def is_plane_visible(pl : list):
        global dots
        global center

        a = np.array([dots[pl[0]][0] - center[0], dots[pl[0]][1] - center[1], dots[pl[0]][2] - center[2]])
        b = np.array([0, 0, -1])

        if (a.dot(b) <= 0):
            return False
        else:
            return True

    dots = []
    center = [0,0,0]
    plane = []

    with open(obj_file) as file:
        info = file.read().split('\n')

    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            dots.append( list(float(dot) for dot in line) )
        elif (line.find("f") == 0):
            _, *line = line.split()
            plane.append( list(int(fig) for fig in line) )


    for i in range(len(dots)):
        center[0] += dots[i][0]
        center[1] += dots[i][1]
        center[2] += dots[i][2]
    center[0] /= len(dots)
    center[1] /= len(dots)
    center[2] /= len(dots)


    for i in range(len(plane)):
        pl = plane[i]
        if (is_plane_visible(pl)):
            for i in range(len(pl) + 1):
                bresenham_line(((int(dots[pl[i]][0]), int(dots[pl[i]][1])), (int(dots[pl[i+1]][0]), int(dots[pl[i+1]][1]))), image)


dots = []
figures = []

image =Image.new("RGB", (2000, 3000))
roggers_clipper("hum.obj", image)

plt.imshow(image)
plt.show()