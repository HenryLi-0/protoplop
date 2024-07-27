'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast, cv2
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import OrbVisualObject, ButtonVisualObject, EditableTextBoxVisualObject, DummyVisualObject, PointVisualObject
from subsystems.counter import Counter
from subsystems.point import *
from subsystems.canvas import CanvasWrapper

class Interface:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.c = Counter()
        '''Generate Icons'''
        # i_plusIconIdle = generateIcon(PLUS_SIGN_ARRAY, False, (29,29))
        # i_plusIconActive = generateIcon(PLUS_SIGN_ARRAY, True, (29,29))

        '''Interactable Visual Objects'''
        '''
        Code:
        s - sketch
        t - tools
        c - colors
        l - layers
        '''
        self.interactableVisualObjects = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # to be used by keybinds

            # self.c.c():["o",ButtonVisualObject("sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
        }
        #for i in range(10): self.interactableVisualObjects[self.c.c()] = ["a", OrbVisualObject(f"test{i}")]

        self.interacting = -999
        self.stringKeyQueue = ""
        self.mouseScroll = 0 


        self.imageSize = (512,512)
        self.drawingImage = PLACEHOLDER_IMAGE_ARRAY #numpy.empty((self.imageSize[1], self.imageSize[0], 4), dtype=numpy.uint8)
        self.drawingImage[:,:] = [255,255,255,255]
        self.sketchZoomMul = 1000/max(self.imageSize[0], self.imageSize[1])
        self.cameraPos = (0,0)
        self.sketchZoom = 100

        pass

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks
        
        self.mouseInSketchSection =   20 <= self.mx and self.mx <= 1043 and   20 <= self.my and self.my <=  677
        self.mouseInToolsSection  = 1057 <= self.mx and self.mx <= 1344 and   20 <= self.my and self.my <=  198
        self.mouseInColorsSection = 1057 <= self.mx and self.mx <= 1344 and  212 <= self.my and self.my <=  366
        self.mouseInLayersSection = 1057 <= self.mx and self.mx <= 1344 and  380 <= self.my and self.my <=  677
        
        if self.interactableVisualObjects[self.interacting][1].name == "new sprite" and mPressed < 3: 
            print("button press")

        '''Keyboard'''
        for key in keyQueue: 
            if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                self.stringKeyQueue+=key
            else:
                if key=="space":
                    self.stringKeyQueue+=" "
                if key=="BackSpace":
                    self.stringKeyQueue=self.stringKeyQueue[0:-1]
                if key=="Return":
                    self.interacting = -998
                    break
        if self.interacting == -999 or self.interacting == -997:
            if KB_ZOOM(keyQueue) and self.mPressed:
                if self.interacting == -999:
                    self.interacting = -997
                    self.interactableVisualObjects[-997][1].data = [mx, my, self.sketchZoom]
                else:
                    temp = self.interactableVisualObjects[-997][1].data
                    self.sketchZoom = temp[2] + ((mx - temp[0]) + (my - temp[1]))/10
                    if self.sketchZoom < 1: 
                        self.sketchZoom = 1
                        self.interactableVisualObjects[-997][1].data = [mx, my, self.sketchZoom]
                    if self.sketchZoom > 10000: 
                        self.sketchZoom = 10000
                        self.interactableVisualObjects[-997][1].data = [mx, my, self.sketchZoom]


        '''Mouse Scroll'''
        self.mouseScroll = mouseScroll
        if abs(self.mouseScroll) > 0:
            if self.mouseInSketchSection:
                self.sketchZoom -= self.mouseScroll/10
                if self.sketchZoom < 1: self.sketchZoom = 1
                if self.sketchZoom > 10000: self.sketchZoom = 10000

        self.sketchZoomMulScaled = self.sketchZoomMul*self.sketchZoom

        pass

        '''Interacting With...'''
        previousInteracting = self.interacting
        if not(self.mPressed):
            self.interacting = -999
        if self.interacting == -999 and self.mPressed and self.mRising:
            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "s":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 20, self.my - 20):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "t":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 20):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "c":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 212):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "l":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 380):
                        self.interacting = id
                        break
        if self.interacting != -999:
            section = self.interactableVisualObjects[self.interacting][0]
            if section == "s": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 20, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(1024,658)
            if section == "t": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(288,179)
            if section == "c": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 212)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(288,155)
            if section == "l": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 380)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(288,298)
        if ((self.mPressed)) and (previousInteracting == -999) and (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.interactableVisualObjects[self.interacting][1].txt
        if (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"):
            self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
        if (previousInteracting != -999) and (previousInteracting != -998):
            if (self.interactableVisualObjects[previousInteracting][1].type  == "textbox"):
                if not(self.interacting == -998):
                    self.interacting = previousInteracting
                    self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
                else:
                    self.interactableVisualObjects[previousInteracting][1].updateText(self.stringKeyQueue)

    def processSketch(self, c:CanvasWrapper):
        '''Sketch Area: `(20,20) to (1043,677)`: size `(1024,658)`'''
        rmx = self.mx - 20
        rmy = self.my - 20
        
        c.placeOver(displayText(f"sketchZoom is {self.sketchZoom}", "s"), (0,0))
        for ix in range(0,8+1):
            for iy in range(0,7+1):
                c.placeOver(setSize(getRegion(self.drawingImage, (round(ix*self.sketchZoomMul), round(iy*self.sketchZoomMul)), (round((ix+1)*self.sketchZoomMul), round((iy+1)*self.sketchZoomMul))), self.sketchZoomMulScaled), (ix*128,iy*94))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "s":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)

        tempPath = []
        for id in self.interactableVisualObjects: 
            if self.interactableVisualObjects[id][1].type == "orb": 
                tempPath.append(self.interactableVisualObjects[id][1].positionO.getPosition())

    
    def processTools(self, c:CanvasWrapper):
        '''Tools Area: `(1057,20) to (1344,198)`: size `(288,179)`'''

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "t":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)

    
    def processColors(self, c:CanvasWrapper):
        '''Colors Area: `(1057,212) to (1344,366)`: size `(288,155)`'''

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "c":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)

    def processLayers(self, c:CanvasWrapper):
        '''Layers Area: `(1057,380) to (1344,677)`: size `(288,298)`'''

        c.placeOver(displayText(f"FPS: {self.fps}", "m"), (15,15))
        c.placeOver(displayText(f"R(S) Mouse Position: ({self.mx-23}, {self.my-36})", "m"), (15,55))
        c.placeOver(displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (15,95))
        c.placeOver(displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (15,135))
        c.placeOver(displayText(f"Interacting With Element: {self.interacting}", "m"), (15,175))
        c.placeOver(displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (15,215))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "l":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)
        

    def saveState(self):
        pass

    def close(self):
        pass