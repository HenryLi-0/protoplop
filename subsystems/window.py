'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from subsystems.canvas import CanvasWrapper
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.grid()
        self.window.title("Tape")
        self.window.geometry("1366x698")
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False
        self.mPressed = False
        self.keyQueue = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.w_sketch = CanvasWrapper(self.window, (1024, 658), (  20,  20), (  20,  20), "white",          FRAME_SKETCH_INSTRUCTIONS)
        self.w_tools  = CanvasWrapper(self.window, ( 288, 179), (1057,  20), (1057,  20), BACKGROUND_COLOR, FRAME_TOOLS_INSTRUCTIONS )
        self.w_colors = CanvasWrapper(self.window, ( 288, 155), (1057, 212), (1057, 212), BACKGROUND_COLOR, FRAME_COLORS_INSTRUCTIONS)
        self.w_layers = CanvasWrapper(self.window, ( 288, 298), (1057, 380), (1057, 380), BACKGROUND_COLOR, FRAME_LAYERS_INSTRUCTIONS)

        '''start interface'''
        self.interface = Interface()

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0:
            self.mPressed += 1
        else:
            self.mPressed = 0

        '''update screens'''
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keyQueue, self.mouseScroll)
        self.keyQueue = []
        self.mouseScroll = 0
        

        self.interface.processSketch(self.w_sketch)
        self.w_sketch.clear()
        self.interface.processTools (self.w_tools )
        self.w_tools .clear()
        self.interface.processColors(self.w_colors)
        self.w_colors.clear()
        self.interface.processLayers(self.w_layers)
        self.w_layers.clear()

        self.fpsCounter +=1
        if math.floor(time.time()) == round(time.time()) and not(self.fpsGood):
            self.fps = self.fpsCounter
            self.fpsCounter = 0
            self.fpsGood = True
        if math.ceil(time.time()) == round(time.time()) and self.fpsGood:
            self.fpsGood = False

        self.window.after(TICK_MS, self.windowProcesses)

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 3 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Protoplop")
        print(self.getFPS())
        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def keyPressed(self, key): self.keyQueue.append(str(key.keysym))
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<Key>", self.keyPressed)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(TICK_MS, self.windowProcesses)
        self.window.after(TICK_MS, self.windowOccasionalProcesses)
        self.window.mainloop()
        self.window.after(0, self.windowStartupProcesses)