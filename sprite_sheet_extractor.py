#!/usr/bin/env python
# coding:utf-8

from __future__ import print_function
from PIL import Image
import math
import os                                           # SN 04_09_2020
from tkinter import filedialog                      # SN 04_09_2020
import tkinter as tk                                # SN 04_09_2020


'''
Process each* scan line in turn
  For each scanline, walk from left to right, until you find a non-transparent pixel P.
    If the location of P is already inside a known bounded box
      Continue to the right of the bounded box
    Else
      BBox = ExploreBoundedBox(P)
      Add BBox to the collection of known bounded boxes

Function ExploreBoundedBox(pStart)
  Q = new Queue(pStart)
  B = new BoundingBox(pStart)

  While Q is not empty
    Dequeue the front element as P
    Expand B to include P

    For each of the four neighbouring pixels N
      If N is not transparent and N is not marked
        Mark N
        Enqueue N at the back of Q

  return B
'''


class Sprite:
    def __init__(self):
        self.start_x = -1
        self.start_y = -1
        self.end_x = -1
        self.end_y = -1

    def expand(self, point):
        if (self.start_x < 0 and self.start_y < 0 and self.end_x < 0 and self.end_y < 0):
            self.start_x = point[0]
            self.start_y = point[1]
            self.end_x = point[0]
            self.end_y = point[1]
        else:
            if (point[0] < self.start_x):
                self.start_x = point[0]
            if (point[0] > self.end_x):
                self.end_x = point[0]
            if (point[1] < self.start_y):
                self.start_y = point[1]
            if (point[1] > self.end_y):
                self.end_y = point[1]

    def belongs(self, point):
        result = False
        result = True
        result = result and point[0] >= self.start_x and point[0] <= self.end_x
        result = result and point[1] >= self.start_y and point[1] <= self.end_y
        return result

    def __str__(self):
        result = ""
        result = result + "("
        result = result + str(self.start_x)
        result = result + ", "
        result = result + str(self.start_y)
        result = result + ", "
        result = result + str(self.end_x)
        result = result + ", "
        result = result + str(self.end_y)
        result = result + ")"
        return result


def loadSprite(pos, sprites):
    result = None
    for sprite in sprites:
        if sprite.belongs(pos):
            result = sprite
            break
    return result


'''
Function ExploreBoundedBox(pStart)
  Q = new Queue(pStart)
  B = new BoundingBox(pStart)

  While Q is not empty
    Dequeue the front element as P
    Expand B to include P

    For each of the four neighbouring pixels N
      If N is not transparent and N is not marked
        Mark N
        Enqueue N at the back of Q

  return B
'''


def exploreBoundedBox(pStart, img):
    result = None
    q = []
    q.append(pStart)
    result = Sprite()
    result.expand(pStart)
    marks = []
    while (len(q) > 0):
        p = q.pop(0)
        result.expand(p)
        neighbouring = loadEightNeighbouringPixels(p, img)
        for n in neighbouring:
            if img.getpixel(n)[3] > 0 and not n in marks:
                marks.append(n)
                q.append(n)
    return result


def loadFourNeighbouringPixels(point, img):
    result = None
    result = []

    newPoint = (point[0], point[1] - 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] - 1, point[1])
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] + 1, point[1])
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0], point[1] + 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    return result


def loadEightNeighbouringPixels(point, img):
    result = None
    result = []

    newPoint = (point[0], point[1] - 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] - 1, point[1])
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] + 1, point[1])
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0], point[1] + 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] - 1, point[1] - 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] + 1, point[1] - 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] - 1, point[1] + 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    newPoint = (point[0] + 1, point[1] + 1)
    if (newPoint[0] >= 0 and newPoint[1] >= 0 and newPoint[0] < img.width and newPoint[1] < img.height):
        result.append(newPoint)

    return result


MINIMUM_SPRITE = 8


def firstNonSprites(sprites):
    result = None
    for sprite in sprites:
        if (sprite.end_x - sprite.start_x + 1) < MINIMUM_SPRITE or (sprite.end_y - sprite.start_y + 1) < MINIMUM_SPRITE:
            result = sprite
            break
    return result


def mergeSprites(sprite1, sprite2):
    result = None
    if (sprite1 != None and sprite2 != None):
        result = Sprite()
        result.start_x = min(sprite1.start_x, sprite2.start_x)
        result.start_y = min(sprite1.start_y, sprite2.start_y)
        result.end_x = max(sprite1.end_x, sprite2.end_x)
        result.end_y = max(sprite1.end_y, sprite2.end_y)
    return result


def findNextSprite(pivot, sprites):
    result = None
    distance = 99999999
    for sprite in sprites:
        if sprite != pivot:
            itemDistance = distanceSprites(pivot, sprite)
            if (itemDistance < distance):
                distance = itemDistance
                result = sprite
    return result


# Pitagoras
def distancePoints(point1, point2):
    result = 99999999
    if (point1 != None and point2 != None):
        a = abs(point2[0] - point1[0])
        b = abs(point2[1] - point1[1])
        result = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
    return result


def distancePointSprite(point, sprite):
    result = 99999999
    if (point != None and sprite != None):
        distance = distancePoints(point, (sprite.start_x, sprite.start_y))
        if (distance < result):
            result = distance
        distance = distancePoints(point, (sprite.end_x, sprite.start_y))
        if (distance < result):
            result = distance
        distance = distancePoints(point, (sprite.start_x, sprite.end_y))
        if (distance < result):
            result = distance
        distance = distancePoints(point, (sprite.end_x, sprite.end_y))
        if (distance < result):
            result = distance
    return result


def distanceSprites(sprite1, sprite2):
    result = 99999999
    if (sprite1 != None and sprite2 != None):
        distance = distancePointSprite((sprite1.start_x, sprite1.start_y), sprite2)
        if (distance < result):
            result = distance
        distance = distancePointSprite((sprite1.end_x, sprite1.start_y), sprite2)
        if (distance < result):
            result = distance
        distance = distancePointSprite((sprite1.start_x, sprite1.end_y), sprite2)
        if (distance < result):
            result = distance
        distance = distancePointSprite((sprite1.end_x, sprite1.end_y), sprite2)
        if (distance < result):
            result = distance
    return result


def fixMergeSprites(sprites):
    result = []
    pivotNonSprite = firstNonSprites(sprites)
    while (pivotNonSprite != None):
        nextSprite = findNextSprite(pivotNonSprite, sprites)
        if nextSprite == None:
            break
        mergeSprite = mergeSprites(pivotNonSprite, nextSprite)
        sprites.remove(nextSprite)
        sprites.remove(pivotNonSprite)
        sprites.append(mergeSprite)
        pivotNonSprite = firstNonSprites(sprites)
    result = sprites
    return result

def rip_sheet():                    # Nissley 04_10_2020 - encapsulated in a function
    im = Image.open(sprite_path)

    print(im.format, im.size, im.mode)
    # PNG (640, 252) RGBA
    # im.show()
    print("width = " + str(im.width))
    print("height = " + str(im.height))

    sprites = []
    for y in range(im.height):
        for x in range(im.width):
            pixel = im.getpixel((x, y))
            haycolor = True if pixel[3] > 0 else False
            if (haycolor):
                pos = (x, y)
                # print("(" + str(x) + ", " + str(y) + ") -> " + str(pixel))
                pixelP = pixel
                sprite = loadSprite(pos, sprites)
                if (sprite != None):
                    x = sprite.end_x
                else:
                    sprite = exploreBoundedBox(pos, im)
                    sprites.append(sprite)
                    print('sprite', len(sprites), 'processed - > ' + str(sprite))   # Nissley 04_10_2020

    sprites = fixMergeSprites(sprites)

    print(str(sprites))
    idx = 1
    for sprite in sprites:
        #print("sprite " + str(idx) + ". -> " + str(sprite))
        imSprite = im.crop((sprite.start_x, sprite.start_y, sprite.end_x + 1, sprite.end_y + 1))
        # imSprite.show()
        imSprite.save(dir_path + '/' + prefix_name + '/' + prefix_name + str(idx) + ".png")
        idx += 1

#######################################################################################################################
# ADDED THIS SECTION - Nissley 04_09_2020
#######################################################################################################################

dir_path = None
sprite_path = None
prefix_name = None


def submit_validate():
    global prefix_name
    warn_label['text'] = ''
    e1['background'] = choose_label['background']
    prefix_name = e1.get()
    if directory['text'] == '^ SELECT A SHEET ^':
        selectFileButton['background'] = 'pink'
        warn_label['text'] = 'ERROR: YOU MUST CHOOSE A SPRITE SHEET TO RIP.'
    elif len(prefix_name) == 0:
        e1['background'] = 'pink'
        warn_label['text'] = 'ERROR: YOU MUST ENTER A PREFIX FOR SPRITE FILENAMES.'
    else:
        warn_label['text'] = 'ATTEMPTING TO RIP SPRITE SHEET.  THIS MAY TAKE A MINUTE.'
        selectFileButton['state'] = 'disabled'
        submitButton['state'] = 'disabled'
        e1['state'] = 'disabled'
        win.update_idletasks()
        create_directory()
        rip_sheet()
        win.destroy()

def select_file():
    global sprite_path, dir_path
    warn_label['text'] = ''
    selectFileButton['background'] = choose_label['background']
    sprite_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("png files", "*.png"), ("all files", "*.*")))
    directory['text'] = sprite_path
    # rfind(substring, [,start[,end]]) is a string method that finds the index of the last occurrence of a substring
    last_slash = sprite_path.rfind('/')
    dir_path = sprite_path[0: last_slash]

def create_directory():
    if not os.path.exists(dir_path + '/' + prefix_name):
        os.makedirs(dir_path + '/' + prefix_name)
    print('Creating Directory:', dir_path + '/' + prefix_name)

win_width = 600
win_height = 240
win = tk.Tk()
win.title('Sprite Sheet Ripper')
win.geometry(str(win_width) + 'x' + str(win_height))
dir_label = tk.Label(win, text='This program will attempt to split a Sprite Sheet into individual frame files.  '
                               'The Sprite Sheet \nshould be a .png file and have a transparent background.',
                     justify='left')
dir_label.grid(row=0, column=0, columnspan=3, padx=40, pady=20, sticky='w')


choose_label = tk.Label(win, text="Choose Sprite Sheet.")
choose_label.grid(row=1, column=0, sticky='e')
sprite_label = tk.Label(win, text="Sprite:")
sprite_label.grid(row=2, column=0, sticky='e')
directory = tk.Label(win, text='^ SELECT A SHEET ^')
directory.grid(row=2, column=1, sticky='w', padx=10, columnspan=2)
prefix_label = tk.Label(win, text="Filename prefix:")
prefix_label.grid(row=3, column=0, sticky='e')
e1 = tk.Entry(win, width=32)
e1.grid(row=3, column=1, sticky='w', padx=10)
warn_label = tk.Label(win, text="", foreground='red')
warn_label.grid(row=4, column=1, sticky='w', columnspan=2)

selectFileButton = tk.Button(text='Select Sheet', command=select_file, padx=20)
selectFileButton.grid(row=1, column=1, sticky='w', padx=10)
submitButton = tk.Button(text='RIP that Sheet', command=submit_validate, padx=20, background='#CCFFCC')
submitButton.grid(row=3, column=2, sticky='w', padx=10)


col_count, row_count = win.grid_size()

win.grid_columnconfigure(0, minsize=50)
win.grid_columnconfigure(1, minsize=120)
win.grid_columnconfigure(2, minsize=50)
# for col in range(col_count):
#     win.grid_columnconfigure(col, minsize=80)

for row in range(row_count):
    win.grid_rowconfigure(row, minsize=36)


win.mainloop()
#######################################################################################################################
