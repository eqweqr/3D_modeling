from PIL import Image, ImageOps
import matplotlib.pyplot as plt


imp = list(map(int, input().split(" ")))
x1, x2, y1, y2 = imp
more_45 = 0


if x1 > x2:
    x1, x2, y1, y2 = x2, x1, y2, y1
step = (y2-y1 > 0) if 1 else -1 # определяем убывает ли отрезок по оси Y
if x2-x1 < y2-y1: 
    more_45 = 1
    x1, x2, y1, y2 = y1, y2, x1, x2

val = (y2+10, max(x1, x2) + 10) if more_45 else (max(x1, x2)+10, y2+10)
image = Image.new('RGB', val)

def moder(mod, x, y):
    if mod:
        return y, x
    return x, y
    
def Brezenheim(x0, x1, y0, y1, step, mode):
    deltax = abs(x1 - x0) 
    deltay = abs(y1 - y0)
    err = 0
    deltaerr = deltay + 1
    y = y0
    for x in range(x0, x1):
        image.putpixel((moder(mode, x, y)), (0, 0, 255))
        err = err + deltaerr
        if err >= deltax + 1:
            y = y + step
            err -= deltax + 1

Brezenheim(x1, x2, y1, y2, step, more_45)

image = ImageOps.flip(image)
plt.imshow(image)
plt.show()
