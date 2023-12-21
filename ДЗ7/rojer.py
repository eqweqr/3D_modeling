from math import sin, cos, pi
from PIL import Image
import matplotlib.pyplot as plt

def Bresenham(image, x0: int, y0: int, x1: int, y1: int, color: tuple = (255, 255, 255)):
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
            image.putpixel((x, y_i), color)
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
            image.putpixel((x_i, y), color)
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


dots = []
figures = []

with open("hum.obj") as file:
    info = file.read().split('\n')

    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            dots.append( list(float(dot) for dot in line) )
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )


with Image.new("RGB", (300, 300)) as image:
    for i in range(len(dots)):
        dots[i] = ChangeVector(get_scale_matrix(15, 15, 15), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Z(35), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(55), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(13, 13), get_vector(dots[i]))[:-1]

    for i in range(len(figures)):
        fig = figures[i]
        if (is_visible(dots, fig)):
            for j in range(-1, len(fig)-1):
                Bresenham(image, int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))

    plt.imshow(image)
    plt.show()