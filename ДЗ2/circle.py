from PIL import Image, ImageOps
import matplotlib.pyplot as plt

r = int(input())
image = Image.new('RGB', (20, 20))

def Bre_cir(r):
    f = 1 - 2*r
    x, y = 0, r
    delta = 3 - 2*y
    while x <= y:
        image.putpixel((x, y), (0, 0, 255))
        image.putpixel((x, y), (0, 0, 255))
        image.putpixel((x, y), (0, 0, 255))
        image.putpixel((x, y), (0, 0, 255))
        image.putpixel((y, x), (0, 0, 255))
        image.putpixel((y, x), (0, 0, 255))
        image.putpixel((y, x), (0, 0, 255))
        image.putpixel((y, x), (0, 0, 255))
        print(x, y, delta)
        if delta < 0:
            delta += 4 * x + 6
        else :
            delta += 4 * (x - y) + 10
            y -= 1
        x += 1

Bre_cir(r)
image = ImageOps.flip(image)
plt.imshow(image)
plt.show()
