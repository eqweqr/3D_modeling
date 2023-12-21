from PIL import Image, ImageOps
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



def Cyrus_Beck():
    global dots_axes, polygon_axes

    edited = False
    t_begin, t_end = 0, 1
    AB_vector = [(dots_axes[1][0] - dots_axes[0][0]), (dots_axes[1][1] - dots_axes[0][1])]

    # Обход вершин будет осуществляться по часовой стрелке
    for i in range(-1, len(polygon_axes)-1):
        # xN = (polygon_axes[i+1][0] - polygon_axes[i][0])
        # yN = (polygon_axes[i+1][1] - polygon_axes[i][1])
        normal = [ -(polygon_axes[i+1][1] - polygon_axes[i][1]), (polygon_axes[i+1][0] - polygon_axes[i][0]) ]

        Api_vector = [ (dots_axes[0][0] - polygon_axes[i][0]), (dots_axes[0][1] - polygon_axes[i][1]) ]

        # Скалярное произведение внутренней нормали отрезка и вектора прямой позволят определить
        # как входит прямая в данную сторону: снаружи внутрь или изнутри в наружу
        # Если данный параметр равен нулю, то значит что прямая параллельна данному отрезку
        # и есть 2 возможных варианта:
        # 1) Если прямая лежит внутри фигуры
        # 2) Прямая лежит снаружи фигуры
        Pi = normal[0]*AB_vector[0] + normal[1]*AB_vector[1]

        # Скалярное произведение вектора A_pi на нормаль отрезка, позволяет определить положение прямой
        # относительно отрезка в случае параллельного расположения
        # Если Qi < 0, то это значит что отрезок находится вне фигуры и дальнейшие вычисления не нужны
        Qi = normal[0]*Api_vector[0] + normal[1]*Api_vector[1]

        if Pi == 0:
            if Qi < 0: return None
            continue

        # Вычисляем параметр t. Если он не лежит в промежутке от 0 до 1, то точка пересечения - мнимая
        t = -Qi / Pi

        # Если скалярное произведение вектора нормали и вектора отрезка положительно, то
        # вектор входит внутрь фигуры
        # поэтому считаем начальную точку пересечения
        # Иначе отрезок выходит из фигуры и мы считаем конечную точку пересечения
        if Pi > 0:
            t_begin = max(t_begin, t)
        else:
            t_end = min(t_end, t)
    
    return t_begin, t_end


def get_cords(T: float):
    X = int(dots_axes[1][0] * T + (1 - T) * dots_axes[0][0])
    Y = int(dots_axes[1][1] * T + (1 - T) * dots_axes[0][1])
    return X, Y


# [[xA, yA],
#   xB, yB]]
polygon_axes = [(5, 5), (15, 5), (15, 20), (5, 20), (5, 5)]
dots_axes = [(5, 10), (30, 10)]

with Image.new('RGB', (50, 50)) as image:
    image = ImageOps.flip(image)


    # Прорисовка изначального положения прямой
    Bresenham(image, dots_axes[0][0], dots_axes[0][1], dots_axes[1][0], dots_axes[1][1], (255, 0, 0))

    # Прорисовка многоугольника
    for i in range(-1, len(polygon_axes)-1):
        Bresenham(image, polygon_axes[i][0], polygon_axes[i][1], polygon_axes[i+1][0], polygon_axes[i+1][1], (0, 0, 255))

    answer = Cyrus_Beck()

    if answer is not None:
        if answer[1] < answer[0]:
            print("Отрезок вне окна")
        else:
            x_begin, y_begin, x_end, y_end = 0, 0, 0, 0
            if answer[0] == 0:
                x_begin, y_begin = dots_axes[0][0], dots_axes[0][1]
            else:
                x_begin, y_begin = get_cords(answer[0])
            
            if answer[1] == 1:
                x_end, y_end = dots_axes[1][0], dots_axes[1][1]
            else:
                x_end, y_end = get_cords(answer[1])

            Bresenham(image, x_begin, y_begin, x_end, y_end, (255, 255, 255))        

    plt.imshow(image)
    plt.show()