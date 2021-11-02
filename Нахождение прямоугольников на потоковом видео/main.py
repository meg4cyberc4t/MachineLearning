import sys
import numpy as np
import cv2
import math
from PIL import Image

# Получаем кадр с видеокамеры
frame = cv2.VideoCapture(0)


# Находим среди всех контуров только прямоугольники
def getBoxes(contours_list, min_area):
    boxes = []
    for contour in contours_list:
        rect = cv2.minAreaRect(contour)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # ищем четыре вершины у прямоугольника
        box = np.int0(box)  # округляем координаты
        area = cv2.contourArea(box)  # вычисляем площадь, занимаемую прямоугольником
        if (area > min_area):
            boxes.append(box)
    return boxes


# Вычисляем угол поворота прямоугольника
def calcAngle(box):
    # Находим центр фигуры
    center = (
        (int((box[0][0] + box[1][0] + box[2][0] + box[3][0]) / 4)),
        (int((box[0][1] + box[1][1] + box[2][1] + box[3][1]) / 4))
    )

    # Находим две стороны прямоугольника: вертикальную и горизонтальную
    edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
    edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

    # Определяем наиболее длинную сторону прямоугольника
    if cv2.norm(edge2) > cv2.norm(edge1):
        usedEdge = edge2
    else:
        usedEdge = edge1

    # Определем горизонтальную сторону
    reference = (1, 0)

    # Вычисляем угол между самой длинной стороной прямоугольника и горизонтом
    angle = 180.0 / math.pi * math.acos(
        (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))

    return center, angle


# Рисуем на изображении прямоугольники, центр и угол наклона
def drawBoxesAngle(img, box, center, angle):
    img_out = img.copy()

    # Рисуем прямоугольник
    cv2.drawContours(img_out, [box], 0, (255, 0, 0), 2)

    # Рисуем круг в центре прямоугольника
    cv2.circle(img_out, center, 3, (10, 200, 10), 5)

    # Выводим величину угла наклона
    cv2.putText(img_out, "%d" % int(angle), (center[0] + 10, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return img_out


#
#
# Обрабатываем кадры в цикле
#
#
while True:
    status, image = frame.read()
    image = cv2.flip(image, 1)  # 0 – по вертикали, 1 – по горизонтали, (-1) – по вертикали и по горизонтали
    
    hsv_min = np.array((40, 40, 70), np.uint8)
    hsv_max = np.array((50, 50, 100), np.uint8)


    # Меняем цветовую модель с BGR на HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Применяем цветовой фильтр
    image_filter = cv2.inRange(hsv, hsv_min, hsv_max)

    # Найдем контуры всех фигур на изображении
    contours_list, _ = cv2.findContours(image_filter.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Находим среди всех контуров только прямоугольники нужного размера
    boxes = getBoxes(contours_list, 2500)

    image_done = image.copy()
    for box in boxes:
        # Получаем центр прямоугольника и угол наклона
        center, angle = calcAngle(box)
        # Отрисовываем все параметры на изображении
        image_done = drawBoxesAngle(image, box, center, angle)

    cv2.imshow("Boxes", image_done)
    cv2.imshow("Filter", image_filter)
    k = cv2.waitKey(30)
    if k == 27:
        break

frame.release()
cv2.destroyAllWindows()
