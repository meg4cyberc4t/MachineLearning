import sys
import numpy as np
import cv2
import math
from PIL import Image
import random

# Получаем кадр с видеокамеры
frame = cv2.VideoCapture(0)
height = int(frame.get(4))
width = int(frame.get(3))

def addcolor(img):
    img = cv2.cvtColor(img, cv2.COLOR)

isFlip = False
isAddColor = False

while True:
    status, image = frame.read()
    image = image.copy()
    if isFlip:
        image = cv2.flip(image, -1)  # 0 – по вертикали, 1 – по горизонтали, (-1) – по вертикали и по горизонтали
        
    # Меняем цветовую модель с BGR на HSV
    if not isAddColor:
        image[(...,2)] = image[(...,2)] * 1.10
        np.clip(image, 0, 255)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    image_done = image.copy()

    cv2.imshow("TV", image_done)
    k = cv2.waitKey(30)

    if k == 100:
        isAddColor = not isAddColor
    if k == 83 or k == 116:
        isFlip = not isFlip
    if k == 27:
        break

frame.release()
cv2.destroyAllWindows()
