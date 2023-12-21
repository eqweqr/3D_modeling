from PIL import Image
import matplotlib.pyplot as plt
import random, time
from math import sqrt

from math import sin, cos, pi


class dot:
    def __init__(self, cordX: float, cordY: float, cordZ: float):
        self.x = cordX
        self.y = cordY
        self.z = cordZ


def ChangeDot(change_matrix: list, vector: list):
    new_vector = [0]*len(vector)

    for i in range(len(change_matrix)):
        for j in range(len(vector)):
            new_vector[i] += change_matrix[i][j] * vector[j]

    return dot(new_vector[0], new_vector[1], new_vector[2])


def get_vector(D: dot):
    return [D.x, D.y, D.z, 1]


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

random.seed(time.time())

class figure:
    def __init__(self, dotA: dot, dotB: dot, dotC: dot, colour: tuple):
        self.dotA = dotA
        self.dotB = dotB
        self.dotC = dotC
        self.colour = colour
        
    def getZ(self, xi: int, yi: int):
        # Ax + By + Cz + D = 0
        coefA = (self.dotB.y - self.dotA.y)*(self.dotC.z - self.dotA.z) - (self.dotB.z - self.dotA.z)*(self.dotC.y - self.dotA.y)
        coefB = (self.dotB.z - self.dotA.z)*(self.dotC.x - self.dotA.x) - (self.dotB.x - self.dotA.x)*(self.dotC.z - self.dotA.z)
        coefC = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)
        coefD = -self.dotA.x*coefA - self.dotA.y*coefB - self.dotA.z*coefC

        if coefC != 0:
            return (-coefA*xi - coefB*yi - coefD)/coefC
        
        return -1

    def in_figure(self, xt: int, yt: int):
        # Проверка будет производиться для обоих обходов
        # Описание векторов фигуры
        abV = tuple([(self.dotB.x - self.dotA.x), (self.dotB.y - self.dotA.y)])
        bcV = tuple([(self.dotC.x - self.dotB.x), (self.dotC.y - self.dotB.y)])
        caV = tuple([(self.dotA.x - self.dotC.x), (self.dotA.y - self.dotC.y)])

        # Описание нормалей векторов фигуры
        Nab = tuple([abV[1], -abV[0]])
        Nbc = tuple([bcV[1], -bcV[0]])
        Nca = tuple([caV[1], -caV[0]])

        # Описание векторов от точек фигуры до исходной точки
        atV = tuple([xt - self.dotA.x, yt - self.dotA.y])
        btV = tuple([xt - self.dotB.x, yt - self.dotB.y])
        ctV = tuple([xt - self.dotC.x, yt - self.dotC.y])

        # Проверка на принадлежность исходной точки данной фигуре
        if ((
            (Nab[0]*atV[0] + Nab[1]*atV[1] >= 0) and 
            (Nbc[0]*btV[0] + Nbc[1]*btV[1] >= 0) and 
            (Nca[0]*ctV[0] + Nca[1]*ctV[1] >= 0)
            )

            or

            (
            (Nab[0]*atV[0] + Nab[1]*atV[1] < 0) and 
            (Nbc[0]*btV[0] + Nbc[1]*btV[1] < 0) and 
            (Nca[0]*ctV[0] + Nca[1]*ctV[1] < 0)
            )):
            
            return True

        return False


dots = []
figures = []

xmin, xmax = 100, 0
ymin, ymax = 100, 0

with open("hum.obj") as file:
    info = file.read().split('\n')

    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            line = list(float(dot) for dot in line)
            D = dot(line[0], line[1], line[2])
            dots.append(D)
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )

    
with Image.new("RGB", (1000, 1000)) as image:

    for i in range(len(dots)):
        dots[i] = ChangeDot(get_scale_matrix(40, 40, 40), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_Z(35), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_X(55), get_vector(dots[i]))
        dots[i] = ChangeDot(get_move_matrix(50, 50), get_vector(dots[i]))
        xmin = int(min(xmin, dots[i].x))
        xmax = int(max(xmax, dots[i].x))
        ymin = int(min(ymin, dots[i].y))
        ymax = int(max(ymax, dots[i].y))

    for i in range(len(figures)):
        figures[i] = figure(dots[figures[i][0]-1], dots[figures[i][1]-1],
                            dots[figures[i][2]-1],
                            tuple([random.randrange(255+1), random.randrange(255+1), random.randrange(255+1)]))
        print(str(i+1) + " = " + str(figures[i].colour))

    # Проход по всей плоскости и вычисление видимой части фигуры
    for X in range(xmin, xmax+1):
        for Y in range(ymin, ymax+1):
            current_fig = None
            current_z = None
            for i in range(len(figures)):
                if figures[i].in_figure(X, Y):
                    fig_z = figures[i].getZ(X, Y)
                    if ((current_fig is None) or (fig_z >= current_z)):
                        current_fig = figures[i]
                        current_z = fig_z


            if current_fig is not None:
                image.putpixel((X, Y), (256, 256, 256))

    plt.imshow(image)
    plt.show()