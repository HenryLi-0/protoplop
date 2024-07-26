import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import getRegion

class CanvasWrapper:
    def __init__(self, root, size, offset = (0,0), place = (0,0), bg = "white"):
        self.offset = offset
        self.size = size
        self.canvas = tk.Canvas(root, width=size[0], height=size[1], bg='white', highlightthickness=0, bd=0)
        self.canvas.pack()
        self.canvas.place(x = place[0], y = place[1])

        self.cache = []

    def placeOver(self, image:numpy.ndarray, position:list|tuple, center = False):
        if center:
            pass
        else:
            copy = getRegion(image, (self.offset[0]-position[0]-self.offset[0],self.offset[1]-position[1]-self.offset[1]), (self.offset[0]+self.size[0]-position[0]-self.offset[0], self.offset[1]+self.size[1]-position[1]-self.offset[1]))
            

        photo = ImageTk.PhotoImage(Image.fromarray(copy))

        self.canvas.create_image(0, 0, image=photo, anchor=tk.CENTER if center else tk.NW)
        self.cache.append(photo)

    def clear(self):
        self.cache = []