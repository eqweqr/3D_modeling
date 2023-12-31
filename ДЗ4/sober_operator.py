from PIL import Image
def settle(n):
    return int(max(0, min(255, n)))

def recolor(t):
    r, g, b = t
    max_r, max_g, max_b = 255, 255, 255  # Фиолетовый
    min_r, min_g, min_b = 0, 0, 0  # Черный
    return settle(min_r + r * (max_r - min_r) / 256), settle(min_g + g * (max_g - min_g) / 256), settle(min_b + b * (max_b - min_b) / 256)

def handler_black_n_white(pixels, i, j, painted=False):
    pixels_nearby = []  # Находим список пикселей которые стоят рядом с данным пикселем
    for di in range(-1, 2):
        for dj in range(-1, 2):
            try:
                pixels_nearby.append(pixels[i + di, j + dj])
            except:
                continue

    total_r, total_g, total_b = 0, 0, 0
    for pixel in pixels_nearby:
        current_r, current_g, current_b = pixel
        for other_pixel in pixels_nearby:
            other_r, other_g, other_b = other_pixel  # Выполним обработку
            delta_r = delta_g = delta_b = (abs(other_r - current_r) + abs(other_g - current_g) + abs(other_b - current_b)) / 3
            total_r, total_g, total_b = total_r + delta_r, total_g + delta_g, total_b + delta_b
    n = len(pixels_nearby)
    total_r, total_g, total_b = total_r / n / n, total_g / n / n, total_b / n / n  # Разделим на n **2
    if painted:
        total_r, total_g, total_b = recolor((total_r, total_g, total_b))
    return settle(total_r), settle(total_g), settle(total_b)

with Image.open("lookat.png") as image:
    image_processed = Image.new('RGB', (image.size[0], image.size[1]*2))
    pixels = image.load()
    print(type(pixels))
    pixels_processed = image_processed.load()

    for x in range(image.size[0]):
        for y in range(image.size[1] * 2):
            if y >= image.size[1]:
                pixels_processed[x, y] = handler_black_n_white(pixels, x, y - image.size[1], True)
            else:
                pixels_processed[x, y] = pixels[x, y]

    image_processed.show()
