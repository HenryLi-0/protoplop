import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import *
from subsystems.label import LabelWrapper
from subsystems.simplefancy import generatePaintBrush
from settings import *

# bigImage1 = generateColorBox((1024,658))
# bigImage2 = generateColorBox((1024,658), (50,50,50,50))

# total = 0
# for i in range(100):
#     start = time.time()
#     placeOver(bigImage1, bigImage2, (0,0))
#     end = time.time()
#     total += end-start
#     print(f"{i+1} tests | {total/(i+1)}s each")

# print(ALL_REGIONS)

# from subsystems.simplefancy import generateColorPicker
# Image.fromarray(generateColorPicker(0.1,(162,100))).show()

# from subsystems.simplefancy import generateRainbowColorPicker
# Image.fromarray(generateRainbowColorPicker()).show()

# import colorsys
# h = 0
# s = 1
# v = 1
# r, g, b = colorsys.hsv_to_rgb(h, s, v)
# print([round(r*255), round(g*255), round(b*255), 255])

# '''taken from window.py'''
        # timer = 0
        # for i in range(1000):
        #     start = time.time()
        #     arrayToImage(self.interface.processFetchSketchSector(0,0))
        #     end = time.time()
        #     timer += (end-start)
        #     print(f"{i+1} tests | {timer/(i+1)}s each")
        # print(timer/1000)
        # while True:
        #     pass

# from subsystems.simplefancy import generateColorBox, generateUnrestrictedColorBox
# from subsystems.render import applyMask

# mask = numpy.ones([100,100], dtype=numpy.uint8)
# mask *= 25
# applyMask(PLACEHOLDER_IMAGE_2_ARRAY, mask)
# # Image.fromarray(mask).show()
# print(numpy.array(Image.fromarray(mask).resize((50, 50), Image.Resampling.NEAREST)).shape)



def fill(image:numpy.ndarray, pixel:tuple|list, color:tuple|list, tolerance:int):
    target_color = image[pixel[1], pixel[0]]
    fill_color = numpy.array(color)
    images = []
    
    mask = numpy.zeros(image.shape[:2], dtype=bool)
    mask[pixel[1], pixel[0]] = True

    i=0
    while True:
        expanded_mask = numpy.zeros_like(mask)
        
        expanded_mask[:-1, :] |= mask[1:, :]
        expanded_mask[1:, :] |= mask[:-1, :]
        expanded_mask[:, :-1] |= mask[:, 1:]
        expanded_mask[:, 1:] |= mask[:, :-1]
        
        color_diff = numpy.abs(image[:, :, :] - target_color)
        within_tolerance = numpy.all(color_diff <= tolerance, axis=2)

        new_mask = expanded_mask & within_tolerance & ~mask

        if not numpy.any(new_mask):
            break

        mask |= new_mask
        print(f"los skibidos {i}")
        i+=1
        imageC = image.copy()
        imageC[mask] = color
        if i%5==0: images.append(Image.fromarray(imageC))

    imageC = image.copy()
    imageC[mask] = color
    images.append(Image.fromarray(imageC))

    print("saving")
    images[0].save("C:/Users/henry/Desktop/Projects/GitHub Repositories/protoplop/test.gif", format='gif', append_images=images[1:], save_all=True, duration=1000/50, loop=0)

    
    image[mask] = color
    
    return image


Image.fromarray(fill(PLACEHOLDER_IMAGE_ARRAY, (50,65), (255,127,0,255), 0)).show()