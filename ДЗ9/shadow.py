from PIL import Image
import numpy as np
import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Face:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

class Plane:
    def __init__(self, ABC):
        self.A = (ABC.B.y - ABC.A.y)*(ABC.C.z - ABC.A.z) - (ABC.C.y - ABC.A.y)*(ABC.B.z - ABC.A.z)
        self.B = -1*((ABC.B.x - ABC.A.x)*(ABC.C.z - ABC.A.z) - (ABC.C.x - ABC.A.x)*(ABC.B.z - ABC.A.z))
        self.C = (ABC.B.x - ABC.A.x)*(ABC.C.y - ABC.A.y) - (ABC.C.x - ABC.A.x)*(ABC.B.y - ABC.A.y)
        self.D = -1*ABC.A.x*self.A + ABC.A.y*self.B - ABC.A.z*self.C;

def scalar_product(V1, V2):
    return V1[0]*V2[0]+V1[1]*V2[1]

def is_in(ABC, x, y):
    AB = (ABC.B.x - ABC.A.x, ABC.B.y - ABC.A.y)
    BC = (ABC.C.x - ABC.B.x, ABC.C.y - ABC.B.y)
    CA = (ABC.A.x - ABC.C.x, ABC.A.y - ABC.C.y)
    
    Nab = (-AB[1], AB[0])
    Nbc = (-BC[1], BC[0])
    Nca = (-CA[1], CA[0])

    Ap = (x - ABC.A.x, y - ABC.A.y)
    Bp = (x - ABC.B.x, y - ABC.B.y)
    Cp = (x - ABC.C.x, y - ABC.C.y)

    if scalar_product(Nab, Ap) <= 0 and \
        scalar_product(Nbc, Bp) <= 0 and \
        scalar_product(Nca, Cp) <= 0:
            return True

    return False
def get_3d_normal(ABC):
    return ((ABC.B.y - ABC.A.y)*(ABC.C.z - ABC.A.z) - (ABC.C.y - ABC.A.y)*(ABC.B.z - ABC.A.z), 
            -1*((ABC.B.x - ABC.A.x)*(ABC.C.z - ABC.A.z) - (ABC.C.x - ABC.A.x)*(ABC.B.z - ABC.A.z)), 
            (ABC.B.x - ABC.A.x)*(ABC.C.y - ABC.A.y) - (ABC.C.x - ABC.A.x)*(ABC.B.y - ABC.A.y))

def get_3d_point(plane, x, y):
    if not plane.C == 0:
        z = (-1*plane.D - x*plane.A - y*plane.B)/plane.C;
        return Point(x, y, z)
    else:
        return Point(x, y, np.nan)

def get_vector_length(V):
    return math.sqrt(V[0]*V[0] + V[1]*V[1] + V[2]*V[2])

def get_intensity(ABC, L, x, y):
    plane = Plane(ABC)
    N = (plane.A, plane.B, plane.C)

    P = get_3d_point(plane, x, y)
    LP = (P.x - L.x, P.y - L.y, P.z - L.z)
    Nlen = get_vector_length(N)
    LPlen = get_vector_length(LP)

    return scalar_product(N, LP)/Nlen/LPlen;

def draw_triangle(ABC, L, w, h, kl=1):
    for i in range(0, h):
        for j in range(0, w):
            if is_in(ABC, j, i):
                il = kl * int(round(get_intensity(ABC, L, j, i) * 255))
                img.putpixel((j, i), (il, il, il)) 

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
            D = Point(line[0], line[1], line[2])
            dots.append(D)
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )


A = Point(0, 0, 0)
B = Point(50, 100, 30)
C = Point(100, 50, 10)
A1 = Point(158, 59, 97)
B1 = Point(100, 140, 80)
C1 = Point(190, 50, 40)
D1 = Point(100, 100, 100)

L = Point(70, 10, 50)

f = Face(A, B, C)
f1 = Face(B, A1, C)
f2 = Face(A1, B1, C1)
f3 = Face(A, D1, C1)

img = Image.new('RGB', (200, 200))

draw_triangle(f, L, 100, 100, 5)
draw_triangle(f1, L, 100, 100, 5)
draw_triangle(f2, L, 100, 100, 5)
draw_triangle(f3, L, 100, 100, 5)


img.save("light.png")