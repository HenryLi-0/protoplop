'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast, cv2
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import OrbVisualObject, ButtonVisualObject, EditableTextBoxVisualObject, DummyVisualObject, IconVisualObject, HorizontalSliderVisualObject, ColorVisualObject, VerticalSliderVisualObject
from subsystems.counter import Counter
from subsystems.point import *
from subsystems.label import LabelWrapper

class Interface:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self.prevmx = 0
        self.prevmy = 0
        self.mPressed = False
        self.mRising = False
        self.fps = 0
        self.ticks = 0
        self.c = Counter()
        '''Interactable Visual Objects'''
        '''
        Code:
        s - sketch
        t - tools
        c - colors
        l - layers
        p - pop up
        '''
        self.interactableVisualObjects = {
            -999 : [" ", DummyVisualObject("dummy", (0,0))], # used for not interacting with anything
            -998 : [" ", DummyVisualObject("dummy", (0,0))], # used for text boxes
            -997 : [" ", DummyVisualObject("dummy", (0,0))], # used by keybinds
            -996 : [" ", DummyVisualObject("dummy", (0,0))], # used by scrolling
            -995 : [" ", DummyVisualObject("dummy", (0,0))], # used when drawing

            -99 : ["t", IconVisualObject(        "None", ICON_SPACING(0,0),    ICON_NONE_ARRAY, (33,33))],
            -98 : ["t", IconVisualObject(        "Move", ICON_SPACING(0,1),    ICON_MOVE_ARRAY, (33,33))],
            -97 : ["t", IconVisualObject( "Paint Brush", ICON_SPACING(0,2),   ICON_BRUSH_ARRAY, (33,33))],
            -96 : ["t", IconVisualObject(      "Pencil", ICON_SPACING(0,3),  ICON_PENCIL_ARRAY, (33,33))],
            -95 : ["t", IconVisualObject(      "Eraser", ICON_SPACING(1,0),  ICON_ERASER_ARRAY, (33,33))],
            -94 : ["t", IconVisualObject(      "Bucket", ICON_SPACING(1,1),  ICON_BUCKET_ARRAY, (33,33))],
            -93 : ["t", IconVisualObject("Color Picker", ICON_SPACING(1,2), ICON_EYEDROP_ARRAY, (33,33))],

            -80 : ["t", IconVisualObject(     "Console", ICON_SPACING(1,3), ICON_CONSOLE_ARRAY, (33,33))],

            -79 : ["c", ColorVisualObject("past color 9", (9*28+6, 128), 12, (255,255,255,255))],
            -78 : ["c", ColorVisualObject("past color 8", (8*28+6, 128), 12, (255,255,255,255))],
            -77 : ["c", ColorVisualObject("past color 7", (7*28+6, 128), 12, (255,255,255,255))],
            -76 : ["c", ColorVisualObject("past color 6", (6*28+6, 128), 12, (255,255,255,255))],
            -75 : ["c", ColorVisualObject("past color 5", (5*28+6, 128), 12, (255,255,255,255))],
            -74 : ["c", ColorVisualObject("past color 4", (4*28+6, 128), 12, (255,255,255,255))],
            -73 : ["c", ColorVisualObject("past color 3", (3*28+6, 128), 12, (255,255,255,255))],
            -72 : ["c", ColorVisualObject("past color 2", (2*28+6, 128), 12, (255,255,255,255))],
            -71 : ["c", ColorVisualObject("past color 1", (1*28+6, 128), 12, (255,255,255,255))],
            -70 : ["c", ColorVisualObject("past color 0", (0*28+6, 128), 12, (255,255,255,255))],

            -50 : ["c", VerticalSliderVisualObject("Hue", (232,20), 100, [0,360])],
            -49 : ["c", VerticalSliderVisualObject("Transparency", (260,20), 100, [100,0])],
        }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.stringKeyQueue = ""
        self.mouseScroll = 0 
        self.consoleAlerts = []
        '''Tools and Sliders'''
        self.selectedTool = -99
        self.previousSelectedTool = self.selectedTool
        self.sliders = []
        self.slidersData = []
        '''Image and Camera'''
        self.imageSize = (1366,697)
        self.sketchZoomMul = 1000/max(self.imageSize[0], self.imageSize[1])
        self.cameraPos = (683,349) # Refers to the center of focus relative to the origin of the unscaled/unzoomed/original image
        self.sketchZoom = 100
        self.updateSketch = True
        self.updateSketchLayers = True
        self.updateSketchRegions = ALL_REGIONS.copy()
        '''Layers'''
        self.drawingImage = LOADING_IMAGE_ARRAY 
        self.blankLayer = generateColorBox((self.imageSize[0], self.imageSize[1]), (0,0,0,0))
        self.blankProcessingLayer = setSize(self.blankLayer, 100/SKETCH_QUALITY)
        self.blankProcessingLayerSector = generateColorBox((128,94), (0,0,0,0))
        self.layers = [
            self.blankLayer.copy(),
            LOADING_IMAGE_ARRAY, 
            self.blankLayer.copy()
        ]
        self.selectedLayer = 1
        self.l_belowLayer   = self.blankLayer.copy()
        self.l_currentLayer = self.blankLayer.copy()
        self.l_aboveLayer   = self.blankLayer.copy()
        self.l_total        = self.blankLayer.copy()
        '''Drawing and Brushes'''
        self.drawingToolIDs = [-97, -96, -95, -80]
        self.drawing = False
        self.brush = None
        self.brushColor = [255,127,0,255]
        self.brushSize = 1
        self.brushStrength = 100
        self.colorPickerHue = self.interactableVisualObjects[-50][1].getData()
        self.colorPickerTransparency = self.interactableVisualObjects[-49][1].getData()
        self.colorPickerImage = generateColorPicker(self.colorPickerHue/360,(162,100))

        pass

    def tick(self,mx,my,mPressed,fps,keyQueue,mouseScroll):
        '''Entire Screen: `(0,0) to (1365,697)`: size `(1366,698)`'''
        self.prevmx = self.mx
        self.prevmy = self.my
        self.mx = mx if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.mx 
        self.my = my if (0<=mx and mx<=1365) and (0<=my and my<=697) else self.my
        self.mPressed = mPressed > 0
        self.mRising = mPressed==2
        self.fps = fps
        self.deltaTicks = 1 if self.fps==0 else round(INTERFACE_FPS/self.fps)
        self.ticks += self.deltaTicks
        
        self.mouseInPopUpSection  =  756 <= self.mx and self.mx <= 1043 and   20 <= self.my and self.my <=  198
        self.mouseInSketchSection =   20 <= self.mx and self.mx <= 1043 and   20 <= self.my and self.my <=  677 and (not(self.mouseInPopUpSection))
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
                '''ZOOM: CTRL + SPACE + MOUSE_MOVEMENT'''
                if self.interacting == -999 and self.mouseInSketchSection:
                    self.interacting = -997
                    self.interactableVisualObjects[-997][1].data = (mx-20, my-20, self.sketchZoom)
                else:
                    temp = self.interactableVisualObjects[-997][1].data
                    self.sketchZoom = temp[2] + ((mx-20 - temp[0]) + (my-20 - temp[1]))/10
                    self.sketchZoom = max(1, min(self.sketchZoom, 10000))
            if KB_FOCUS(keyQueue) and self.mRising:
                '''FOCUS: CTRL + F + Click'''
                self.updateSketch = True
                self.updateSketchLayers = True
                self.scheduleAllRegions()
                self.cameraPos = (self.calcScreenToNonZoomedX(mx-20), self.calcScreenToNonZoomedY(my-20))

        self.processDrawing()

        '''Mouse Scroll'''
        self.mouseScroll = mouseScroll
        if abs(self.mouseScroll) > 0:
            if self.interacting == -999 and self.mouseInSketchSection:
                self.interacting = -996
            if self.interacting == -996 and self.mouseInSketchSection:
                self.updateSketch = True
                self.updateSketchLayers = True
                self.scheduleAllRegions()
                temp = self.interactableVisualObjects[-996][1].data
                self.sketchZoom -= self.mouseScroll/10
                self.sketchZoom = max(1, min(self.sketchZoom, 10000))

        else:
            if self.interacting == -996: self.interacting = -999
        # if abs(self.mouseScroll) > 0:
        #     self.sketchZoom -= self.mouseScroll/10
        #     if self.sketchZoom < 1: self.sketchZoom = 1
        #     if self.sketchZoom > 10000: self.sketchZoom = 10000
        #     self.sketchZoomMulScaled = self.sketchZoomMul*self.sketchZoom
        #     self.updateSketch = True
            

        self.sketchZoomMulScaled = self.sketchZoomMul*self.sketchZoom

        self.consoleAlerts.append(f"{self.ticks} - self.cameraPos: {self.cameraPos}")

        self.selectedLayer = max(1,min(self.selectedLayer,len(self.layers)-2))
        pass

        '''Interacting With...'''
        self.previousInteracting = self.interacting
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
                        if self.interactableVisualObjects[id][1].type == "icon":
                            self.selectedTool = id
                        break
                if self.interactableVisualObjects[id][0] == "c":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 212):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "l":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 380):
                        self.interacting = id
                        break
                if self.interactableVisualObjects[id][0] == "p":
                    if self.interactableVisualObjects[id][1].getInteractable(self.mx - 756, self.my - 20):
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
            if section == "p": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 756, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(288,179)
        if ((self.mPressed)) and (self.previousInteracting == -999) and (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"): 
            self.stringKeyQueue = self.interactableVisualObjects[self.interacting][1].txt
        if (self.interacting != -999) and (self.interactableVisualObjects[self.interacting][1].type  == "textbox"):
            self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
        if (self.previousInteracting != -999) and (self.previousInteracting != -998):
            if (self.interactableVisualObjects[self.previousInteracting][1].type  == "textbox"):
                if not(self.interacting == -998):
                    self.interacting = self.previousInteracting
                    self.interactableVisualObjects[self.interacting][1].updateText(self.stringKeyQueue)
                else:
                    self.interactableVisualObjects[self.previousInteracting][1].updateText(self.stringKeyQueue)


    def processSketch(self, im):
        '''Sketch Area: `(20,20) to (1043,677)`: size `(1024,658)`'''
        img = setSize(im.copy(), 100/SKETCH_QUALITY)
        rmx = self.mx - 20
        rmy = self.my - 20

        
        self.consoleAlerts.append(f"{time.time()} - processSketch() running")
        
        if len(self.updateSketchRegions) > 0:
            i = 0
            for i in range(min(SKETCH_MAX_REGIONS, len(self.updateSketchRegions))):
                ix, iy = self.updateSketchRegions.pop(0)
                placeOver(img, self.processFetchSketchSector(ix, iy), (math.floor(ix*128/SKETCH_QUALITY),math.floor(iy*94/SKETCH_QUALITY)))
                

        # placeOver(img, self.l_belowLayer,   (0,0))
        # placeOver(img, self.l_currentLayer, (0,0))
        # placeOver(img, self.l_aboveLayer,   (0,0))
        
        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "s":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

        tempPath = []
        for id in self.interactableVisualObjects: 
            if self.interactableVisualObjects[id][1].type == "orb": 
                tempPath.append(self.interactableVisualObjects[id][1].positionO.getPosition())

        img = setSizeSizeBlur(img, (1024, 658))
        return img
    
    def processSketchLayers(self):
        self.selectedLayer = max(1,min(self.selectedLayer,len(self.layers)-2))
        self.l_currentLayer = self.blankProcessingLayer.copy()
        self.l_belowLayer = self.blankProcessingLayer.copy()
        self.l_aboveLayer = self.blankProcessingLayer.copy()
        self.l_total = self.blankProcessingLayer.copy()

        for index in range(0, len(self.layers)):
            if self.sketchZoom < 100: # The entire image is smaller than the screen
                scaledDrawingImage = setSize(self.layers[index], (self.sketchZoom))
                scaledDrawingImage = getRegion(scaledDrawingImage, (self.cameraPos[0]*(self.sketchZoom/100) - 512, self.cameraPos[1]*(self.sketchZoom/100) - 329), (self.cameraPos[0]*(self.sketchZoom/100) + 512, self.cameraPos[1]*(self.sketchZoom/100) + 329), 2, color=VOID_COLOR_RGBA)
                if SKETCH_QUALITY != 1: scaledDrawingImage = setSize(scaledDrawingImage, 100/SKETCH_QUALITY)
            else: # The image is in one dimension or another larger than the screen
                scaledDrawingImage = getRegion(self.layers[index], (self.cameraPos[0] - 512*(100/self.sketchZoom),self.cameraPos[1] - 329*(100/self.sketchZoom)), (self.cameraPos[0] + 512*(100/self.sketchZoom),self.cameraPos[1] + 329*(100/self.sketchZoom)), color=VOID_COLOR_RGBA)
                scaledDrawingImage = setSizeSize(scaledDrawingImage, (round(1024*1/SKETCH_QUALITY), round(658*1/SKETCH_QUALITY)))
            if index < self.selectedLayer:
                placeOver(self.l_belowLayer, scaledDrawingImage, (0,0))
            elif index == self.selectedLayer:
                placeOver(self.l_currentLayer, scaledDrawingImage, (0,0))
            elif index > self.selectedLayer:
                placeOver(self.l_aboveLayer, scaledDrawingImage, (0,0))
            else:
                placeOver(self.l_aboveLayer, scaledDrawingImage, (0,0))
            placeOver(self.l_total, scaledDrawingImage, (0,0))
    
    def processFetchSketchSector(self, x, y):
        '''128x94'''
        self.selectedLayer = max(1,min(self.selectedLayer,len(self.layers)-2))
        total = self.blankProcessingLayerSector.copy()

        for index in range(0, len(self.layers)):
            if self.sketchZoom < 100: # The entire image is smaller than the screen
                scaledDrawingImage = setSize(self.layers[index], (self.sketchZoom))
                scaledDrawingImage = getRegion(scaledDrawingImage, (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*x, self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*y), (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*(x+1), self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*(y+1)), 2, color=VOID_COLOR_RGBA)
                if SKETCH_QUALITY != 1: scaledDrawingImage = setSize(scaledDrawingImage, 100/SKETCH_QUALITY)
            else: # The image is in one dimension or another larger than the screen
                scaledDrawingImage = getRegion(self.layers[index], (self.cameraPos[0] + (128*x-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*y-329)*(100/self.sketchZoom)), (self.cameraPos[0] + (128*(x+1)-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*(y+1)-329)*(100/self.sketchZoom)), color=VOID_COLOR_RGBA)
                scaledDrawingImage = setSizeSize(scaledDrawingImage, (math.ceil(128*1/SKETCH_QUALITY), math.ceil(94*1/SKETCH_QUALITY)))
            placeOver(total, scaledDrawingImage, (0,0))
        
        return total 

    def processDrawing(self):
        '''Run from tick(), is a seperate function/methoed for orginization'''
        rmx = self.mx-20
        rmy = self.my-20
        prevrmx = self.prevmx-20
        prevrmy = self.prevmy-20
        tx = self.calcScreenToNonZoomedX(rmx)
        ty = self.calcScreenToNonZoomedY(rmy)
        ptx = self.calcScreenToNonZoomedX(prevrmx)
        pty = self.calcScreenToNonZoomedY(prevrmy)
        if (self.interacting == -999 or self.interacting == -995) and (self.selectedTool in self.drawingToolIDs) and (self.mouseInSketchSection) and (self.mRising):
            self.interacting = -995
            self.drawing = True
            self.brush = generatePaintBrush(self.brushSize, self.brushColor, self.brushStrength)
        if self.interacting == -995 and not(self.mPressed):
            self.interacting = -999
            self.drawing = False
        if self.interacting == -995:
            t = self.brushSize * (self.sketchZoom/100)
            self.scheduleRegionGivenBrush(rmx, rmy, t)
            steps = math.ceil(math.sqrt((tx-ptx)**2 + (ty-pty)**2)/self.brushSize)+1
            i = 0
            while i <= steps:
                placeOver(self.layers[self.selectedLayer], self.brush, (ptx + round(i*(tx - ptx)/steps), pty + round(i*(ty - pty)/steps)), True)
                self.scheduleRegionGivenBrush(rmx, rmy, t)
                i+=1
            self.updateSketchLayers = True
            self.updateSketch = True

        if self.selectedTool == -93 and self.mouseInSketchSection and self.mRising and self.interacting == -999:
            # Color Picking
            self.brushColor = self.l_total[round(rmy*1/SKETCH_QUALITY), round(rmx*1/SKETCH_QUALITY)]
            self.brush = generatePaintBrush(self.brushSize, self.brushColor, self.brushStrength)


    def processPopUp(self, im):
        '''Pop Up Area: `(756,20) to (1043,198)`: size `(288,179)`'''
        if self.selectedTool in self.drawingToolIDs:
            img = im.copy()
            if self.previousSelectedTool != self.selectedTool:
                self.previousSelectedTool = self.selectedTool
                temp = []
                for id in self.interactableVisualObjects:
                    if self.interactableVisualObjects[id][0] == "p":
                        temp.append(id)
                for id in temp:
                    self.interactableVisualObjects.pop(id)
                if self.selectedTool == -97: # Paint Brush
                    self.sliders = [self.c.c(), self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", HorizontalSliderVisualObject("Size", (20,55), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[1]] = ["p", HorizontalSliderVisualObject("Strength", (20,105), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[0]][1].setData(self.brushSize)
                    self.interactableVisualObjects[self.sliders[1]][1].setData(self.brushStrength)
                if self.selectedTool == -96: # Pencil
                    pass
                if self.selectedTool == -95: # Eraser
                    pass
            else:
                if self.selectedTool == -97: # Paint Brush
                    placeOver(img, displayText(f"Paint Brush:", "m"), (10,10))
                    placeOver(img, displayText(f"Size: {self.interactableVisualObjects[self.sliders[0]][1].getData()}", "sm"), (10, 35))
                    placeOver(img, displayText(f"Strength: {self.interactableVisualObjects[self.sliders[1]][1].getData()}", "sm"), (10, 85))
                    if self.interacting == -999:
                        temp = [self.interactableVisualObjects[self.sliders[0]][1].getData(), self.interactableVisualObjects[self.sliders[1]][1].getData()]
                        if self.slidersData != temp:
                            self.brush = generatePaintBrush(temp[0], self.brushColor, temp[1])
                            self.brushSize = temp[0]
                            self.brushStrength = temp[1]
                            self.slidersData = temp
                            self.consoleAlerts.append(f"{self.ticks} - generated a brush!")
                    
                if self.selectedTool == -96: # Pencil
                    pass

                if self.selectedTool == -95: # Eraser
                    pass

                if self.selectedTool == -80: # Console
                    placeOver(img, displayText(f"sketchZoom is {self.sketchZoom}", "s"), (5,164))
                    if len(self.consoleAlerts) > 15: self.consoleAlerts = self.consoleAlerts[-15:]
                    for i in range(len(self.consoleAlerts)):
                        placeOver(img, displayText(f"{self.consoleAlerts[i]}", "s"), (5,i*10))

            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "p":
                    self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
            return img
        else:
            return EMPTY_IMAGE_ARRAY

    
    def processTools(self, im):
        '''Tools Area: `(1057,20) to (1344,198)`: size `(288,179)`'''
        img = im.copy()
        

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "t":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id or self.selectedTool==id)

        return img

    
    def processColors(self, im):
        '''Colors Area: `(1057,212) to (1344,366)`: size `(288,155)`'''
        img = im.copy()

        if self.colorPickerHue != self.interactableVisualObjects[-50][1].getData() or self.colorPickerTransparency != self.interactableVisualObjects[-49][1].getData():
            self.colorPickerHue = self.interactableVisualObjects[-50][1].getData()
            self.colorPickerTransparency = self.interactableVisualObjects[-49][1].getData()
            self.colorPickerImage = generateColorPicker(self.colorPickerHue/360,(162,100))
            print(self.colorPickerHue)

        placeOver(img, self.colorPickerImage, (62,20))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "c":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
        
        return img

    def processLayers(self, im):
        '''Layers Area: `(1057,380) to (1344,677)`: size `(288,298)`'''
        img = im.copy()

        placeOver(img, displayText(f"FPS: {self.fps}", "m"), (15,15))
        placeOver(img, displayText(f"R(S) Mouse Position: ({self.mx-23}, {self.my-36})", "m"), (15,55))
        placeOver(img, displayText(f"Mouse Pressed: {self.mPressed}", "m", colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (15,95))
        placeOver(img, displayText(f"Rising Edge: {self.mRising}", "m", colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (15,135))
        placeOver(img, displayText(f"Interacting With Element: {self.interacting}", "m"), (15,175))
        placeOver(img, displayText(f"stringKeyQueue: {self.stringKeyQueue}", "m"), (15,215))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "l":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

        return img
    
    
    def calcScreenToZoomedX(self, x): return x - 512 + (self.cameraPos[0] * self.sketchZoom/100)
    def calcScreenToZoomedY(self, y): return y - 329 + (self.cameraPos[1] * self.sketchZoom/100)
    def calcZoomedToScreenX(self, x): return x - (self.cameraPos[0] * self.sketchZoom/100) + 512
    def calcZoomedToScreenY(self, y): return y - (self.cameraPos[1] * self.sketchZoom/100) + 329
    def calcScreenToNonZoomedX(self, x): return (x - 512)/(self.sketchZoom/100) + self.cameraPos[0]
    def calcScreenToNonZoomedY(self, y): return (y - 329)/(self.sketchZoom/100) + self.cameraPos[1]


    def scheduleRegionGivenBrush(self, rmx, rmy, t):
        cornerA = (max(0, min(math.floor((rmx-t)/128), 8-1)), max(0, min(math.floor((rmy-t)/96), 7-1)))
        cornerB = (max(0, min(math.floor((rmx+t)/128), 8-1)), max(0, min(math.floor((rmy+t)/96), 7-1)))
        self.consoleAlerts.append(f"cornerA {cornerA}")
        self.consoleAlerts.append(f"cornerB {cornerB}")
        for ix in range(cornerB[0]-cornerA[0]+2):
            for iy in range(cornerB[1]-cornerA[1]+2):
                self.scheduleRegion((cornerA[0]+ix, cornerA[1]+iy))
        
    def scheduleRegionGivenPixel(self, pixel):
        region = (max(0, min(pixel[0] // 128, 8-1)), max(0, min(pixel[1] // 96, 7-1)))
        if region not in self.updateSketchRegions:
            self.updateSketchRegions.append(region)

    def scheduleRegion(self, region):
        safeRegion = (max(0, min(region[0], 8-1)), max(0, min(region[1], 7-1)))
        if safeRegion not in self.updateSketchRegions:
            self.updateSketchRegions.append(safeRegion)

    def scheduleAllRegions(self):
        for region in ALL_REGIONS:
            if region not in self.updateSketchRegions:
                self.updateSketchRegions.append(region)

    def saveState(self):
        pass

    def close(self):
        pass
