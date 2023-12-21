from math import sin, cos, pi
from PIL import Image
import matplotlib.pyplot as plt


class dot:
    def __init__(self, cordX: float, cordY: float):
        self.x = cordX
        self.y = cordY


def ChangeDot(change_matrix: list, vector: list):
    new_vector = [0]*len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return dot(new_vector[0], new_vector[1])


def get_vector(D: dot):
    return [D.x, D.y, 1]


def ToRadian(angle: float):
    return (angle * pi) / 180


def get_move_matrix(dx: float = 0, dy: float = 0, dz: float = 0):
    return [[1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]]


def get_scale_matrix(kx: float = 0, ky: float = 0, kz: float = 0):
    return [[kx, 0, 0],
            [0, ky, 0],
            [0, 0, 1]]


def get_rotate_matrix(angle: float, is_radian: bool = False):
    if not is_radian:
        angle = ToRadian(angle)
        
    return  [[cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]]

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

dots = []
figures = []
doto = []

with open("shuttle.obj") as file:
    info = file.read()
    info = info.split('\n')

    for line in info:
        if (line.find("v ") == 0):
            _, *cords = line.split()
            doto.append( list(float(i) for i in cords) )
            for i in range(len(doto)    ):
                dots.append(dot(doto[i][0]*3, doto[i][1]*3))
        elif (line.find("f ") == 0):
            _, vertex = line.split(" ", 1)
            vertex = vertex.strip().split()
            figures.append( list(int(i) for i in vertex) )
    
with Image.new("RGB", (100, 100)) as image:
    for i in range(len(dots)):
        dots[i] = ChangeDot(get_scale_matrix(2, 2), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix(45), get_vector(dots[i]))
        dots[i] = ChangeDot(get_move_matrix(50, 50), get_vector(dots[i]))

    for i in range(len(figures)):
        fig = figures[i]
        for j in range(-1, len(fig)-1):
            Bresenham(image, round(dots[fig[j]-1].x), round(dots[fig[j]-1].y), \
                      round(dots[fig[j+1]-1].x), round(dots[fig[j+1]-1].y))

    plt.imshow(image)
    plt.show()