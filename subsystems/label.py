import tkinter as tk
import numpy, time, math, random 
from PIL import Image, ImageTk
from subsystems.render import getRegion
from subsystems.point import roundp
from subsystems.simplefancy import generateColorBox
from settings import PLACEHOLDER_IMAGE, hexColorToRGBA
from subsystems.render import placeOver

class LabelWrapper:
    def __init__(self, root, size, offset = (0,0), place = (0,0), bg = "#ffffff", instructions = None):
        self.offset = offset
        self.size = size
        self.section = tk.Label(root, width=size[0], height=size[1], bg=bg, highlightthickness=0, bd=0, image = ImageTk.PhotoImage(PLACEHOLDER_IMAGE))
        self.section.pack()
        self.section.place(x = place[0], y = place[1])
        self.blank = generateColorBox(self.size, hexColorToRGBA(bg))
        if type(instructions) == list:
            for instruction in instructions:
                placeOver(self.blank, instruction[0], instruction[1])


    def update(self, image:numpy.ndarray):
        img = ImageTk.PhotoImage(image)
        self.section.configure(image = img)
        self.section.image=img
    
    def getBlank(self):
        return self.blank.copy()