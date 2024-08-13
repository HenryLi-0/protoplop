'''This file is just the window that pops up and refreshes itself!'''

from settings import *
import tkinter as tk
from PIL import ImageTk, Image
import time, math
from subsystems.interface import Interface
from subsystems.label import LabelWrapper
from subsystems.render import placeOver, arrayToImage
from settings import *

class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window = tk.Tk()
        self.window.grid()
        self.window.title("Protoplop")
        self.window.geometry("1366x698")
        self.window.configure(background=BACKGROUND_COLOR)
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False
        self.mPressed = False
        self.keysPressed = []
        self.mouseScroll = 0

        '''load test image'''
        testImage = ImageTk.PhotoImage(PLACEHOLDER_IMAGE)
        self.w_sketch = {}
        for region in ALL_REGIONS:
            self.w_sketch[region] = LabelWrapper(self.window, (128, 94), (region[0]*128+20, region[1]*94+20), (region[0]*128+20, region[1]*94+20), VOID_COLOR)
        self.w_tools  = LabelWrapper(self.window, ( 288, 179), (1057,  20), (1057,  20), BACKGROUND_COLOR, FRAME_TOOLS_INSTRUCTIONS )
        self.b_tools  = self.w_tools .getBlank() 
        self.w_colors = LabelWrapper(self.window, ( 288, 155), (1057, 212), (1057, 212), BACKGROUND_COLOR, FRAME_COLORS_INSTRUCTIONS)
        self.b_colors = self.w_colors.getBlank() 
        self.w_layers = LabelWrapper(self.window, ( 288, 298), (1057, 380), (1057, 380), BACKGROUND_COLOR, FRAME_LAYERS_INSTRUCTIONS)
        self.b_layers = self.w_layers.getBlank() 
        self.w_popUp  = LabelWrapper(self.window, ( 288, 179), ( 756,  20), ( 756,  20), BACKGROUND_COLOR, FRAME_LAYERS_INSTRUCTIONS)
        self.b_popUp  = self.w_popUp.getBlank() 

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
        self.interface.tick(mx,my,self.mPressed, self.fps, self.keysPressed, self.mouseScroll)
        self.mouseScroll = 0
        
        temp = self.interface.updateSketchLayers or self.interface.updateSketch or len(self.interface.updateSketchRegions) > 0
        if self.interface.updateSketchLayers:
            # self.interface.processSketchLayers()
            # self.interface.updateSketchLayers = False
            pass
        if self.interface.updateSketch: 
            # self.i_sketch = self.interface.processSketch(self.i_sketch)
            # self.w_sketch.update(arrayToImage(self.i_sketch))
            # self.interface.updateSketch = False
            pass

        '''OPTIMIZE, CONSTANT SKETCH SCREEN UPDATES ARE NOT NECCESARY!'''
        if len(self.interface.updateSketchRegions) > 0:
            i = 0
            start = time.time()
            for i in range(min(SKETCH_MAX_REGIONS, len(self.interface.updateSketchRegions))):
                region = self.interface.updateSketchRegions.pop(0)
                temp = arrayToImage(self.interface.processFetchSketchSector(region[0], region[1])).resize((128,94))
                self.w_sketch[region].update(temp)
                if time.time() - start > SKETCH_MAX_REGIONS_TIME:
                    break
            self.interface.consoleAlerts.append(f"{self.interface.ticks} - regions left: {len(self.interface.updateSketchRegions)}")
        self.w_tools .update(arrayToImage(self.interface.processTools (self.b_tools )))
        self.w_colors.update(arrayToImage(self.interface.processColors(self.b_colors)))
        self.w_layers.update(arrayToImage(self.interface.processLayers(self.b_layers)))
        self.w_popUp .update(arrayToImage(self.interface.processPopUp (self.b_popUp )))

        if self.interface.selectedTool in self.interface.popUpDataIDs:
            if not(self.w_popUp.shown): self.w_popUp.show()
        else:
            if self.w_popUp.shown: self.w_popUp.hide()


        self.fpsCounter +=1
        if math.floor(time.time()) == round(time.time()) and not(self.fpsGood):
            self.fps = self.fpsCounter
            self.fpsCounter = 0
            self.fpsGood = True
        if math.ceil(time.time()) == round(time.time()) and self.fpsGood:
            self.fpsGood = False

        self.window.after(TICK_MS, self.windowProcesses)

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        self.window.title(f"Protoplop")
        print(self.getFPS())
        self.interface.scheduleAllRegions(False)
        self.window.after(OCCASIONAL_TICK_MS, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    def keyPressed(self, key): 
        if (not str(key.keysym) in self.keysPressed) and (not str(key.keysym) in KB_IGNORE):
            self.keysPressed.append(str(key.keysym))
    def keyReleased(self, key):
        if str(key.keysym) in self.keysPressed:
            self.keysPressed.remove(str(key.keysym))
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<KeyPress>", self.keyPressed)
        self.window.bind("<KeyRelease>", self.keyReleased)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(TICK_MS, self.windowProcesses)
        self.window.after(TICK_MS, self.windowOccasionalProcesses)
        self.window.mainloop()
        self.window.after(0, self.windowStartupProcesses)