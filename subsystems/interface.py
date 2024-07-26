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
        a - animation
        '''
        self.interactableVisualObjects = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))],
            -998 : [" ", DummyVisualObject("dummy", (0,0))],

            # self.c.c():["o",ButtonVisualObject("sprites",(7,0),FRAME_OPTIONS_BUTTON_OFF_ARRAY,FRAME_OPTIONS_BUTTON_ON_ARRAY)],
        }
        #for i in range(10): self.interactableVisualObjects[self.c.c()] = ["a", OrbVisualObject(f"test{i}")]

        self.interacting = -999
        self.stringKeyQueue = ""
        self.mouseScroll = 0 

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
        if self.interactableVisualObjects[self.interacting][1].name == "new sprite" and mPressed < 3: 
            print("button press")

        '''Keyboard and Scroll (graph and timeline)'''
        for key in keyQueue: 
            if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                self.stringKeyQueue+=key
            else:
                if key=="space":
                    self.stringKeyQueue+=" "
                if key=="BackSpace":
                    self.stringKeyQueue=self.stringKeyQueue[0:-1]
                if key=="Return" or key=="Control_L":
                    self.interacting = -998
                    break
            if self.interacting == -999:
                if key in KB_SPRITE_LIST_OFFSET_UP:   self.spriteListVelocity -= 25
                if key in KB_SPRITE_LIST_OFFSET_DOWN: self.spriteListVelocity += 25
                            
        self.mouseScroll = mouseScroll

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
        if self.interacting != -999:
            section = self.interactableVisualObjects[self.interacting][0]
            if section == "s": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 20, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(1024,658)
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
            if (self.selectedProperty == 1) and (self.interactableVisualObjects[previousInteracting][1].type  == "point"):
                if not(self.interacting == -998):
                    self.interacting = previousInteracting

    def processSketch(self, c:CanvasWrapper):
        '''Sketch Area: `(20,20) to (1043,677)`: size `(1024,658)`'''
        rmx = self.mx - 20
        rmy = self.my - 20

        c.placeOver(displayText(f"FPS: {self.fps}", "m", colorTXT=(0,0,0,255)), (55,15))
        c.placeOver(displayText(f"Relative (animation) Mouse Position: ({self.mx-23}, {self.my-36})", "m", colorTXT=(0,0,0,255)), (455,55))
        c.placeOver(displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (55,55))
        c.placeOver(displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (55,95))
        c.placeOver(displayText(f"Interacting With Element: {self.interacting}", "m", colorTXT=(0,0,0,255)), (455,15))
        c.placeOver(displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m", colorTXT=(0,0,0,255)), (455,95))

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
                self.interactableVisualObjects[id][1].tick(c, self.animationPlaying)

    
    def processColors(self, c:CanvasWrapper):
        '''Colors Area: `(1057,212) to (1344,366)`: size `(288,155)`'''

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "c":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)

    def processLayers(self, c:CanvasWrapper):
        '''Layers Area: `(1057,380) to (1344,677)`: size `(288,298)`'''

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "c":
                self.interactableVisualObjects[id][1].tick(c, self.interacting==id)
        

    def saveState(self):
        pass

    def close(self):
        pass