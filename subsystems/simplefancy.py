'''This file contains functions related to fancy rendering, but does not import from setting'''

from PIL import Image, ImageDraw
import numpy, random, colorsys

def generateColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color'''
    array = numpy.empty((size[1], size[0], 4), dtype=numpy.uint8)
    array[:, :] = color
    return array

def generateUnrestrictedColorBox(size:list|tuple = (25,25),color:list|tuple = (255,255,255,255)):
    '''Generates a box of (size) size of (color) color without restrictions'''
    array = numpy.empty((size[1], size[0], 4))
    array[:, :] = color
    return array

def generateMask(size:list|tuple = (25,25),transparency:int = 255):
    '''Generates a mask of (size) size of (transparency) transparency'''
    array = numpy.empty((size[1], size[0]), dtype=numpy.uint8)
    array[:, :] = transparency
    return array

def generateBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a bordered box with a transparent inside, with transparent space of (size), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1]+2*outlineW, size[0]+2*outlineW, 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generateInwardsBorderBox(size:list|tuple = (25,25), outlineW:int = 1, color:list|tuple = (255,255,255,255)):
    '''Generates a inwards bordered box with a transparent inside, with transparent space of (size - outline), and an (outlineW) px thick outline of (color) color surrounding it'''
    array = numpy.zeros((size[1], size[0], 4), dtype=numpy.uint8)
    array[:outlineW, :, :] = color
    array[-outlineW:, :, :] = color
    array[:, :outlineW, :] = color
    array[:, -outlineW:, :] = color
    return array

def generatePastelDark():
    '''Randomly generates a dark pastel color'''
    color = [100]
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.insert(random.randrange(0,len(color)), random.randrange(100,200))
    color.append(255)
    return color

def translatePastelLight(color):
    '''Translate a dark pastel color to a light pastel color, given the color in RGBA form'''
    colorC = color[0:3]
    colorC = list(colorsys.rgb_to_hsv(colorC[0]/255,colorC[1]/255,colorC[2]/255))
    colorC[2] = 0.9
    colorC = colorsys.hsv_to_rgb(colorC[0],colorC[1],colorC[2])
    return [round(colorC[0]*255), round(colorC[1]*255), round(colorC[2]*255), color[3]]

def genereateThemedBorderRectangleInstructions(size:list|tuple = (25,25),borderColor:list|tuple = (255,255,255,255)):
    instructions = []
    row = generateColorBox((size[0],3), borderColor)
    col = generateColorBox((3,size[1]), borderColor)
    instructions.append([row, (0,0)])
    instructions.append([col, (0,0)])
    instructions.append([row, (0,size[1]-3)])
    instructions.append([col, (size[0]-3,0)])
    return instructions


def generatePaintBrush(radius, color, strength):
    '''Generates a circle paint brush with given radius (radius), color (RGBA), and strength (0-100, 100 is solid)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.uint8)
    alpha = int((strength / 100) * 255)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            distance = numpy.sqrt((x-center)**2+(y-center)**2)
            if distance <= radius:
                array[y,x] = [color[0], color[1], color[2], min(int(color[3]/255 * alpha * (1 - (distance / radius))), 255)]
            else:
                array[y,x] = (0,0,0,0)
    return array

def generatePencilBrush(radius, color):
    '''Generates a single-colored circle paint brush given the length (length), color (RGBA)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.uint8)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            if numpy.sqrt((x-center)**2+(y-center)**2) <= radius:
                array[y,x] = color
            else:
                array[y,x] = (0,0,0,0)
    return array

def generateEraserBrush(radius, strength):
    '''Generates a negative single-colored eraser paint brush given the length (length), strength (0-100, 100 is solid)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.float64)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            if numpy.sqrt((x-center)**2+(y-center)**2) <= radius:
                array[y,x] = (0,0,0, -round(strength*2.55))
            else:
                array[y,x] = (0,0,0,0)
    return array

def generateCircle(radius, color):
    '''Generates a circle paint brush with given radius (radius) and color (RGBA)'''
    diameter = radius * 2
    array = numpy.empty((diameter, diameter, 4), dtype=numpy.uint8)
    center = radius
    for y in range(diameter):
        for x in range(diameter):
            distance = numpy.sqrt((x-center)**2+(y-center)**2)
            if distance <= radius:
                array[y,x] = color
            else:
                array[y,x] = (0,0,0,0)
    return array

def generateColorPicker(hue, shape = (163,100)):
    array = numpy.empty((shape[1], shape[0], 4), dtype=numpy.uint8)
    for y in range(shape[1]):
        for x in range(shape[0]):
           r,g,b = colorsys.hsv_to_rgb(hue,x/shape[0],1-y/shape[1])
           array[y,x] = (int(r*255), int(g*255), int(b*255), 255)
    return array

def generateRainbowColorPicker(shape = (10,100)):
    array = numpy.empty((shape[1], shape[0], 4), dtype=numpy.uint8)
    for y in range(shape[1]):
        r,g,b = colorsys.hsv_to_rgb(y/shape[1],1,1)
        array[y,:] = (int(r*255), int(g*255), int(b*255), 255)
    return array