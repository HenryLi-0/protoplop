import tkinter as tk
import numpy, time, math, random 
from PIL import Image, ImageTk
from subsystems.render import getRegion
from subsystems.point import roundp

class CanvasWrapper:
    def __init__(self, root, size, offset = (0,0), place = (0,0), bg = "white", default:numpy.ndarray = ""):
        self.offset = offset
        self.size = size
        self.canvas = tk.Canvas(root, width=size[0], height=size[1], bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack()
        self.canvas.place(x = place[0], y = place[1])

        self.cache = []
        if type(default) != str:
            self.hasDefault = True
            self.default = [[ImageTk.PhotoImage(Image.fromarray(instruction[0])), (instruction[1][0], instruction[1][1])] for instruction in default]
        else:
            self.hasDefault = False

        self.name = str(random.randint(0,999))


    def placeOver(self, image:numpy.ndarray, position:list|tuple, center = False):
        if center:
            pass
        else:
            copy = getRegion(image, (round(self.offset[0]-position[0]-self.offset[0]),round(self.offset[1]-position[1]-self.offset[1])), (round(self.offset[0]+self.size[0]-position[0]-self.offset[0]), round(self.offset[1]+self.size[1]-position[1]-self.offset[1])))
        
        photo = ImageTk.PhotoImage(Image.fromarray(copy))
        self.canvas.create_image(0, 0, image=photo, anchor=tk.CENTER if center else tk.NW)
        self.cache.append(photo)

    def clear(self):
        self.canvas.delete("all")
        self.cache = []
        if self.hasDefault:
            for instruction in self.default: 
                self.canvas.create_image(instruction[1][0], instruction[1][1], image=instruction[0], anchor=tk.NW)