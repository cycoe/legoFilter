#!/usr/bin/python

from functools import reduce
from PIL import Image


def grey(image):
    pixdata = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            grey_scale = int(reduce(lambda i, j:i + j, pixdata[x, y]) / 3)
            pixdata[x, y] = (grey_scale, grey_scale, grey_scale, 255)
    return image


def convert(image):
    pixdata = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixdata[x, y] = tuple(map(lambda i:255 - i, pixdata[x, y]))
    return image


def emboss(image):
    pixdata = image.load()
    pre = (128, 128, 128, 255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            current = pixdata[x, y]
            pixdata[x, y] = tuple(map(lambda i: i[1]-i[0]+128, zip(pre, current)))
            pre = current
    return grey(image)


def binarify(image):
    pixdata = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            grey_scale = int(reduce(lambda i, j:i + j, pixdata[x, y]) / 3)
            if grey_scale >= 128:
                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)
    return image

if __name__ == '__main__':
    image =Image.open('ori.png')
    image = grey(image)
    image.save('10.png')
