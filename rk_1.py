from PIL import Image
from random import randint


img = Image.open('Mushroom_1.jpeg')
pixels = img.load()
for y in range(img.height):
    for x in range(img.width):
        r, g, b = pixels[x, y]
        if not ((r < 250 and g > 100 and b > 0) or (r > 250 and g > 250 and b > 250)):
            pixels[x, y] = (0, 0, 0)


def pixel_permutation(img, x, y, mas):
    mid = len(mas) // 2
    total = sum([sum(el) for el in mas])
    total_color = [0, 0, 0]
    if total <= 0:
        total = 1
    for row in range(len(mas)):
        for el in range(len(mas[row])):
            x_n = x + (el - mid)
            y_n = y + (row - mid)
            if 0 <= x_n < img.width and 0 <= y_n < img.height:
                c = img.getpixel((x_n, y_n))
                total_color[0] += c[0] * mas[row][el]
                total_color[1] += c[1] * mas[row][el]
                total_color[2] += c[2] * mas[row][el]
    total_color = [int(abs(el) / total) for el in total_color]
    return tuple(total_color)


def prewitt(img):
    prewitt_x = [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]
    prewitt_y = [
        [1, 1, 1],
        [0, 0, 0],
        [-1, -1, -1]
    ]
    w, h = img.size
    res_img = Image.new("RGB", (w, h))
    for y in range(h):
        for x in range(w):
            gx = pixel_permutation(img, x, y, prewitt_x)
            gy = pixel_permutation(img, x, y, prewitt_y)
            mag = [int(min((gx[i]**2 + gy[i]**2)**0.5, 255)) for i in range(3)]
            r = int(mag[0] * 0.1)
            g = int(mag[1] * 1.0)
            b = int(mag[2] * 1.0)
            res_img.putpixel((x, y), (r, g, b))
    return res_img


def erosion(img, threshold):
    w, h = img.size
    pixels = img.load()
    result = Image.new("RGB", (w, h), "black")
    result_pixels = result.load()
    for y in range(h):
        for x in range(w):
            count_similar = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        pr = pixels[nx, ny]
                        brightness = sum(pr) / 3
                        if brightness > threshold:
                            count_similar += 1
            if count_similar >= 8:
                result_pixels[x, y] = pixels[x, y]
            else:
                result_pixels[x, y] = (0, 0, 0)
    return result


def dilation(img, threshold):
    w, h = img.size
    pixels = img.load()
    result = Image.new("RGB", (w, h), "black")
    result_pixels = result.load()
    for y in range(h):
        for x in range(w):
            count_similar = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        pr = pixels[nx, ny]
                        brightness = sum(pr) / 3
                        if brightness > threshold:
                            count_similar += 1
            if count_similar > 0:
                result_pixels[x, y] = pixels[x, y]
            else:
                result_pixels[x, y] = (0, 0, 0)
    return result


def compare(color1, color2):
    return sum(abs(color1[i] - color2[i]) for i in range(3))


def k_means(img, k, iterations):
    w, h = img.size
    pixels = img.load()
    centers = [(
        randint(0, 100),
        randint(200, 255),
        randint(150, 255)
    ) for _ in range(k)]

    for _ in range(iterations):
        clusters = [[0, 0, 0, 0] for _ in range(k)]
        for y in range(h):
            for x in range(w):
                c = pixels[x, y]
                distances = [compare(c, center) for center in centers]
                min_idx = distances.index(min(distances))
                clusters[min_idx][0] += c[0]
                clusters[min_idx][1] += c[1]
                clusters[min_idx][2] += c[2]
                clusters[min_idx][3] += 1
        for i in range(k):
            if clusters[i][3] != 0:
                centers[i] = (
                    clusters[i][0] // clusters[i][3],
                    clusters[i][1] // clusters[i][3],
                    clusters[i][2] // clusters[i][3]
                )
    new_img = Image.new("RGB", (w, h))
    new_pixels = new_img.load()
    for y in range(h):
        for x in range(w):
            c = pixels[x, y]
            distances = [compare(c, center) for center in centers]
            min_idx = distances.index(min(distances))
            new_pixels[x, y] = centers[min_idx]

    return new_img


# Фильтрация цвета
img.save('filt_1.jpeg')
filt_img = Image.open('filt_1.jpeg')
# Открывающий фильтр
otk_img = erosion(filt_img, threshold=50)
otk_img = dilation(otk_img, threshold=20)
otk_img.save('morph_1.jpeg')
# Метод k-средних
clust_img = Image.open('morph_1.jpeg')
clust_img = k_means(clust_img, k=3, iterations=20)
clust_img.save('clust_1.jpeg')
# Фильтр Прюитта
pr_img = Image.open('clust_1.jpeg')
pr_img = prewitt(pr_img)
pr_img.save('prewitt_1.jpeg')
res_img = Image.open('prewitt_1.jpeg')
res_img = erosion(res_img, threshold=100)
res_img = dilation(res_img, threshold=0)
pixels = res_img.load()
for y in range(res_img.height):
    for x in range(res_img.width):
        r, g, b = pixels[x, y]
        if not (r < 80 and (g > 190 or b > 190)):
            pixels[x, y] = (0, 0, 0)
res_img.save('res_1.jpeg')
