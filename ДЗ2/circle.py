from PIL import Image, ImageOps
import matplotlib.pyplot as plt

inp = list(map(int, input().split(" ")))
x, y, r = inp
image = Image.new('RGB', (x + 2*r+1, y + 2*r+1))

def Bre_cir(x0, y0, r):
    f = 1 - 2*r
    x, y = 0, r
    delta = 3 - 2*y
    while x <= y:
        image.putpixel((x0+x, y0+y), (0, 0, 255))
        image.putpixel((x0+x, y0-y), (0, 0, 255))
        image.putpixel((x0-x, y0+y), (0, 0, 255))
        image.putpixel((x0-x, y0-y), (0, 0, 255))
        image.putpixel((x0+y, y0+x), (0, 0, 255))
        image.putpixel((x0+y, y0-x), (0, 0, 255))
        image.putpixel((x0-y, y0+x), (0, 0, 255))
        image.putpixel((x0-y, y0-x), (0, 0, 255))
        if delta < 0:
            delta += 4 * x + 6
        else :
            delta += 4 * (x - y) + 10
            y -= 1
        x += 1

Bre_cir(x, y, r)
image = ImageOps.flip(image)
plt.imshow(image)
plt.show()
