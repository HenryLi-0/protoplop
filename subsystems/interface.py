'''This file is all about managing what the user sees'''

from settings import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time, random, ast
from subsystems.render import *
from subsystems.fancy import *
from subsystems.simplefancy import *
from subsystems.visuals import *
from subsystems.counter import Counter
from subsystems.point import *
from subsystems.bay import *

class Interface:
    def __init__(self, imageSize = DEFAULT_IMAGE_SIZE, reset = True):
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
        if reset:
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
                -92 : ["t", IconVisualObject("Resize (All)", ICON_SPACING(1,3),  ICON_RESIZE_ARRAY, (33,33))],

                -82 : ["t", IconVisualObject(        "Open", ICON_SPACING(5,1),    ICON_OPEN_ARRAY, (33,33))],
                -81 : ["t", IconVisualObject(        "Save", ICON_SPACING(5,2),    ICON_SAVE_ARRAY, (33,33))],
                -80 : ["t", IconVisualObject(     "Console", ICON_SPACING(5,3), ICON_CONSOLE_ARRAY, (33,33))],

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

                -50 : ["c", VerticalSliderVisualObject(         "Hue", (232,20), 100, [0,360])],
                -49 : ["c", VerticalSliderVisualObject("Transparency", (260,20), 100, [100,0])],
                -48 : ["c", MovableColorVisualObject("Color Picker", (62-10,120-10), 10, [0,0,0,255])],
                -47 : ["c", ColorVisualObject("Brush Color", (14, 20), 18, (  0,  0,  0,255))],
                -46 : ["c", ColorVisualObject( "Back Color", (14, 56), 18, (255,255,255,255))],

                -30 : ["l", EditableTextBoxVisualObject("Selected Layer Name", (70, 11), "Layer")],
                -29 : ["l", ToggleVisualObject(  "Show/Hide Layer", (10, 10), ICON_HIDDEN_ARRAY, ICON_SHOWN_ARRAY, (15,15))],
                -28 : ["l", ToggleVisualObject("Lock/Unlock Layer", (40, 10), ICON_UNLOCK_ARRAY,  ICON_LOCK_ARRAY, (15,15))],
                -22 : ["l", IconVisualObject(  "Layer Mask", (215,273), ICON_LAYERMASK_ARRAY, (15,15))],
                -21 : ["l", IconVisualObject(   "New Layer", (239,273),      ICON_PLUS_ARRAY, (15,15))],
                -20 : ["l", IconVisualObject("Delete Layer", (263,273),  ICON_TRASHCAN_ARRAY, (15,15))],
            }
        '''Control'''
        self.interacting = -999
        self.previousInteracting = -999
        self.stringKeyQueue = ""
        self.previousKeyQueue = []
        self.mouseScroll = 0 
        self.consoleAlerts = []
        self.keybindLastUpdate = time.time()
        '''Tools and Sliders'''
        self.selectedTool = -99
        self.previousSelectedTool = self.selectedTool
        self.sliders = []
        self.slidersData = []
        '''Image and Camera'''
        self.imageSize = imageSize
        self.sketchZoomMul = 1000/max(self.imageSize[0], self.imageSize[1])
        self.cameraPos = (round(imageSize[0]/2),round(imageSize[1]/2)) # Refers to the center of focus relative to the origin of the unscaled/unzoomed/original image
        self.sketchZoom = 100
        self.updateSketch = True
        self.updateSketchLayers = True
        self.updateSketchRegions = ALL_REGIONS.copy()
        self.updateSketchRegionLayers = ALL_REGIONS.copy()
        '''Layers'''
        self.blankLayer = generateColorBox((self.imageSize[0], self.imageSize[1]), (0,0,0,0))
        self.blankMask = generateMask((self.imageSize[0], self.imageSize[1]), 255)
        self.blankProcessingLayer = setSize(self.blankLayer, 100/SKETCH_QUALITY)
        self.blankProcessingLayerSector = generateColorBox((128,94), (0,0,0,0))
        if reset:
            self.layers = [
                self.blankLayer.copy(),
                EMPTY_LARGE_IMAGE_ARRAY.copy(), 
                self.blankLayer.copy()
            ]
            self.layerNames = [
                "Blank",
                "Layer",
                "Blank"
            ]
            self.layerProperties = [
                [True, True, ""],
                [False, True, ""],
                [True, True, ""]
            ]
        self.selectedLayer = 1
        self.previousSelectedLayer = -999
        self.layersOffset = 0
        self.numberOfLayers = len(self.layers)
        self.l_belowLayer   = self.blankLayer.copy()
        self.l_currentLayer = self.blankLayer.copy()
        self.l_aboveLayer   = self.blankLayer.copy()
        self.l_total        = self.blankLayer.copy()
        self.editingMask = False
        '''Regions'''
        self.regionDataCache = {}
        self.regionLayersCache = {}
        for region in ALL_REGIONS:
            self.regionDataCache[region] = EMPTY_IMAGE_ARRAY.copy()
            self.regionLayersCache[region] = [EMPTY_IMAGE_ARRAY.copy(), EMPTY_IMAGE_ARRAY.copy()]
        '''Drawing and Brushes'''
        self.popUpDataIDs = [-97, -96, -95, -80, -94, -81, -92]
        self.drawingToolsIDs = [-97,-96, -95]
        self.lastDrawingTool = -999
        self.drawing = False
        self.brush = None
        self.brushColor = self.interactableVisualObjects[-47][1].getColor()
        self.backColor = self.interactableVisualObjects[-46][1].getColor()
        self.modifyingColor = -47 # -47 is brush, -46 is back
        self.pastBrushColors = [(255,255,255,255) for i in range(10)]
        self.brushSize = 1
        self.brushStrength = 100
        self.colorPickerHue = self.interactableVisualObjects[-50][1].getData()
        self.colorPickerTransparency = self.interactableVisualObjects[-49][1].getData()
        self.colorPickerImage = generateColorPicker(self.colorPickerHue/360)

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

        self.tickButtons(mPressed)
        
        if self.interacting == -21 and mPressed < 3: 
            '''Create Layer'''
            self.scheduleAllRegions()
            self.layers.insert(self.selectedLayer+1, self.blankLayer.copy())
            self.layerNames.insert(self.selectedLayer+1, "Layer")
            self.layerProperties.insert(self.selectedLayer+1, [False, True, "???"])
        if self.interacting == -20 and mPressed < 3:
            '''Delete Layer'''
            if len(self.layers) > 3:
                self.scheduleAllRegions()
                self.layers.pop(self.selectedLayer)
                self.layerNames.pop(self.selectedLayer)
                self.layerProperties.pop(self.selectedLayer)
                self.selectedLayer = max(1, min(self.selectedLayer, len(self.layers)-2))
        if self.interacting == -22 and mPressed < 3:
            '''Layer Mask'''
            self.editingMask = not(self.editingMask)


        '''Keyboard'''
        for key in keyQueue: 
            if not key in self.previousKeyQueue:
                if key in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
                    self.stringKeyQueue+=key
                else:
                    if key=="space":
                        self.stringKeyQueue+=" "
                    if key=="BackSpace":
                        if len(self.stringKeyQueue) > 0:
                            self.stringKeyQueue=self.stringKeyQueue[0:-1]
                    if key=="Return" or key=="Control_L":
                        self.interacting = -998
                        break
        self.previousKeyQueue = keyQueue.copy()
        if (self.interacting == -999 or self.interacting == -997) and (time.time() - self.keybindLastUpdate > 0.2):
            if KB_ZOOM(keyQueue) and self.mPressed:
                '''ZOOM: CTRL + SPACE + MOUSE_MOVEMENT'''
                self.keybindLastUpdate = time.time()
                if self.interacting == -999 and self.mouseInSketchSection:
                    self.interacting = -997
                    self.interactableVisualObjects[-997][1].data = (mx-20, my-20, self.sketchZoom)
                else:
                    temp = self.interactableVisualObjects[-997][1].data
                    self.sketchZoom = temp[2] + ((mx-20 - temp[0]) + (my-20 - temp[1]))/10
                    self.sketchZoom = max(1, min(self.sketchZoom, 10000))
            if KB_FOCUS(keyQueue) and self.mRising:
                '''FOCUS: CTRL + F + Click'''
                self.keybindLastUpdate = time.time()
                self.updateSketch = True
                self.updateSketchLayers = True
                self.scheduleAllRegions()
                self.cameraPos = (self.calcScreenToNonZoomedX(mx-20), self.calcScreenToNonZoomedY(my-20))
            if KB_L_MV_UP(keyQueue):
                '''MOVE LAYER UP: ALT + UP'''
                self.keybindLastUpdate = time.time()
                if len(self.layers) > 3 and self.selectedLayer < len(self.layers)-2:
                    self.scheduleAllRegions()
                    temp = self.layers.pop(self.selectedLayer)
                    temp2 = self.layerNames.pop(self.selectedLayer)
                    temp3 = self.layerProperties.pop(self.selectedLayer)
                    self.selectedLayer += 1
                    self.layers.insert(self.selectedLayer, temp)
                    self.layerNames.insert(self.selectedLayer, temp2)
                    self.layerProperties.insert(self.selectedLayer, temp3)
            if KB_L_MV_DOWN(keyQueue):
                '''MOVE LAYER DOWN: ALT + DOWN'''
                self.keybindLastUpdate = time.time()
                if len(self.layers) > 3 and self.selectedLayer > 1:
                    self.scheduleAllRegions()
                    temp = self.layers.pop(self.selectedLayer)
                    temp2 = self.layerNames.pop(self.selectedLayer)
                    temp3 = self.layerProperties.pop(self.selectedLayer)
                    self.selectedLayer -= 1
                    self.layers.insert(self.selectedLayer, temp)
                    self.layerNames.insert(self.selectedLayer, temp2)
                    self.layerProperties.insert(self.selectedLayer, temp3)
            if KB_L_NEW(keyQueue):
                '''CREATE LAYER: ALT + A'''
                self.keybindLastUpdate = time.time()
                self.scheduleAllRegions()
                i = self.selectedLayer
                if self.mouseInLayersSection:
                    i = max(0, min(len(self.layers)-round(((self.my-380)+self.layersOffset)/50)-1, len(self.layers)-2))
                self.layers.insert(i+1, self.blankLayer.copy())
                self.layerNames.insert(i+1, "Layer")
                self.layerProperties.insert(i+1, [False, True, "???"])
            if KB_L_DELETE(keyQueue):
                '''DELETE LAYER: ALT + S'''
                self.keybindLastUpdate = time.time()
                if len(self.layers) > 3:
                    self.scheduleAllRegions()
                    self.layers.pop(self.selectedLayer)
                    self.layerNames.pop(self.selectedLayer)
                    self.layerProperties.pop(self.selectedLayer)
                    self.selectedLayer = max(1, min(self.selectedLayer, len(self.layers)-2))
            if KB_T_NONE(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -99
            if KB_T_MOVE(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -98
            if KB_T_BRUSH(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -97
            if KB_T_PENCIL(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -96
            if KB_T_ERASER(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -95
            if KB_T_BUCKET(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -94
            if KB_T_EYEDROP(keyQueue):
                self.keybindLastUpdate = time.time()
                self.selectedTool = -93


        self.tickDrawing()

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

        if abs(self.mouseScroll) > 0:
            if self.mouseInLayersSection:
                self.layersOffset += self.mouseScroll/10
                self.layersOffset = max(0, min(round(self.layersOffset), 50*(len(self.layers)-7)))
            

        self.sketchZoomMulScaled = self.sketchZoomMul*self.sketchZoom

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
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,1024,658)
            if section == "t": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,288,179)
            if section == "c" and self.interactableVisualObjects[self.interacting][1].type != "movable color": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 212)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,288,155)
            if section == "l": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 380)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,288,298)
            if section == "p": 
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 756, self.my - 20)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(0,0,288,179)
            if self.interactableVisualObjects[self.interacting][1].type == "movable color":
                self.interactableVisualObjects[self.interacting][1].updatePos(self.mx - 1057, self.my - 212)
                self.interactableVisualObjects[self.interacting][1].keepInFrame(62,20,225,120)

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

        if 1057 <= self.mx and self.mx <= 1344 and 380 <= self.my and self.my <= 677 and self.mPressed and mPressed < 3 and self.interacting == -999:
            i = len(self.layers)-math.floor(((self.my-380)+self.layersOffset)/50)-1
            if 1 <= i and i <= len(self.layers)-2:
                self.selectedLayer = i

        if self.selectedTool in self.drawingToolsIDs: self.lastDrawingTool = self.selectedTool


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
    
    def processFetchSketchSector(self, x, y, forceNoRegen = False):
        '''128x94'''
        self.selectedLayer = max(1,min(self.selectedLayer,len(self.layers)-2))
        total = self.blankProcessingLayerSector.copy()

        if (x,y) in self.updateSketchRegionLayers and not(forceNoRegen):
            back = self.blankProcessingLayerSector.copy()
            front = self.blankProcessingLayerSector.copy()
            for index in range(0, len(self.layers)):
                if self.layerProperties[index][1] and index != self.selectedLayer:
                    if self.sketchZoom < 100: # The entire image is smaller than the screen
                        scaledDrawingImage = setSize(self.layers[index], self.sketchZoom)
                        scaledDrawingImage = getRegion(scaledDrawingImage, (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*x, self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*y), (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*(x+1), self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*(y+1)), 2, color=VOID_COLOR_RGBA)
                        if type(self.layerProperties[index][2]) != str:
                            scaledDrawingMask  = setSize(self.layerProperties[index][2], self.sketchZoom)
                            scaledDrawingMask  = getRegion(scaledDrawingMask, (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*x, self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*y), (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*(x+1), self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*(y+1)), 2, color=0, thirdaxis=False)
                            applyMask(scaledDrawingImage, scaledDrawingMask)
                        if SKETCH_QUALITY != 1: scaledDrawingImage = setSize(scaledDrawingImage, 100/SKETCH_QUALITY)
                    else: # The image is in one dimension or another larger than the screen
                        scaledDrawingImage = getRegion(self.layers[index], (self.cameraPos[0] + (128*x-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*y-329)*(100/self.sketchZoom)), (self.cameraPos[0] + (128*(x+1)-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*(y+1)-329)*(100/self.sketchZoom)), color=VOID_COLOR_RGBA)
                        scaledDrawingImage = setSizeSize(scaledDrawingImage, (math.ceil(128*1/SKETCH_QUALITY), math.ceil(94*1/SKETCH_QUALITY)))
                        if type(self.layerProperties[index][2]) != str:
                            scaledDrawingMask  = getRegion(self.layerProperties[index][2], (self.cameraPos[0] + (128*x-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*y-329)*(100/self.sketchZoom)), (self.cameraPos[0] + (128*(x+1)-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*(y+1)-329)*(100/self.sketchZoom)), color=0, thirdaxis=False)
                            scaledDrawingMask  = setSizeSize(scaledDrawingMask, (math.ceil(128*1/SKETCH_QUALITY), math.ceil(94*1/SKETCH_QUALITY)))
                            applyMask(scaledDrawingImage, scaledDrawingMask)
                    if self.selectedLayer < index:
                        placeOver(front, scaledDrawingImage, (0,0))
                    else:
                        placeOver(back, scaledDrawingImage, (0,0))
            self.regionLayersCache[(x,y)] = [back, front]
            self.updateSketchRegionLayers.remove((x,y))
            return self.processFetchSketchSector(x, y, True)
        else:
            placeOver(total, self.regionLayersCache[(x,y)][0], (0,0))
            if self.layerProperties[self.selectedLayer][1]:
                if self.sketchZoom < 100: # The entire image is smaller than the screen
                    scaledDrawingImage = setSize(self.layers[self.selectedLayer], self.sketchZoom)
                    scaledDrawingImage = getRegion(scaledDrawingImage, (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*x, self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*y), (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*(x+1), self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*(y+1)), 2, color=VOID_COLOR_RGBA)
                    if type(self.layerProperties[self.selectedLayer][2]) != str:
                        scaledDrawingMask  = setSize(self.layerProperties[self.selectedLayer][2], self.sketchZoom)
                        scaledDrawingMask  = getRegion(scaledDrawingMask, (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*x, self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*y), (self.cameraPos[0]*(self.sketchZoom/100) - 512 + 128*(x+1), self.cameraPos[1]*(self.sketchZoom/100) - 329 + 94*(y+1)), 2, color=0, thirdaxis=False)
                        applyMask(scaledDrawingImage, scaledDrawingMask)
                    if SKETCH_QUALITY != 1: scaledDrawingImage = setSize(scaledDrawingImage, 100/SKETCH_QUALITY)
                else: # The image is in one dimension or another larger than the screen
                    scaledDrawingImage = getRegion(self.layers[self.selectedLayer], (self.cameraPos[0] + (128*x-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*y-329)*(100/self.sketchZoom)), (self.cameraPos[0] + (128*(x+1)-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*(y+1)-329)*(100/self.sketchZoom)), color=VOID_COLOR_RGBA)
                    scaledDrawingImage = setSizeSize(scaledDrawingImage, (math.ceil(128*1/SKETCH_QUALITY), math.ceil(94*1/SKETCH_QUALITY)))
                    if type(self.layerProperties[self.selectedLayer][2]) != str:
                        scaledDrawingMask  = getRegion(self.layerProperties[self.selectedLayer][2], (self.cameraPos[0] + (128*x-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*y-329)*(100/self.sketchZoom)), (self.cameraPos[0] + (128*(x+1)-512)*(100/self.sketchZoom),self.cameraPos[1] + (94*(y+1)-329)*(100/self.sketchZoom)), color=0, thirdaxis=False)
                        scaledDrawingMask  = setSizeSize(scaledDrawingMask, (math.ceil(128*1/SKETCH_QUALITY), math.ceil(94*1/SKETCH_QUALITY)))
                        applyMask(scaledDrawingImage, scaledDrawingMask)
                placeOver(total, scaledDrawingImage, (0,0))
            placeOver(total, self.regionLayersCache[(x,y)][1], (0,0))

        self.regionDataCache[(x,y)] = total

        return total 
    
    def tickButtons(self, mPressed):
        '''Run from tick(), is a seperate function/methoed for orginization'''
        if self.interactableVisualObjects[self.interacting][1].name == "Save To File" and mPressed < 3: 
            self.saveDrawing()
            self.interacting = -999
            self.selectedTool = -99
            self.scheduleAllRegions()
        if self.interacting == -82 and mPressed < 3: 
            self.loadDrawing()
            self.interacting = -999
            self.selectedTool = -99
            self.scheduleAllRegions()
        if self.interactableVisualObjects[self.interacting][1].name == "Resize Image" and mPressed < 3:
            for i in range(len(self.layers)):
                self.layers[i] = setSizeSize(self.layers[i], (int(self.interactableVisualObjects[self.sliders[2]][1].txt),int(self.interactableVisualObjects[self.sliders[3]][1].txt)))
            for i in range(len(self.layerProperties)):
                if type(self.layerProperties[i][2]) != str:
                    self.layerProperties[i][2] = setSizeSize(self.layerProperties[i][2], (int(self.interactableVisualObjects[self.sliders[2]][1].txt),int(self.interactableVisualObjects[self.sliders[3]][1].txt)))
            self.interacting = -999
            self.selectedTool = -99
            self.__init__((max(1,int(self.interactableVisualObjects[self.sliders[2]][1].txt)),max(1,int(self.interactableVisualObjects[self.sliders[3]][1].txt))),reset=False)
            self.scheduleAllRegions()
            


    def tickDrawing(self):
        '''Run from tick(), is a seperate function/methoed for orginization'''
        rmx = self.mx-20
        rmy = self.my-20
        prevrmx = self.prevmx-20
        prevrmy = self.prevmy-20
        tx = self.calcScreenToNonZoomedX(rmx)
        ty = self.calcScreenToNonZoomedY(rmy)
        ptx = self.calcScreenToNonZoomedX(prevrmx)
        pty = self.calcScreenToNonZoomedY(prevrmy)
        if not(self.layerProperties[self.selectedLayer][0]) and self.layerProperties[self.selectedLayer][1]:
            if (self.interacting == -999 or self.interacting == -995) and (self.mouseInSketchSection) and (self.mRising):
                if self.selectedTool in self.drawingToolsIDs:
                    self.interacting = -995
                    self.drawing = True
                    self.regenerateBrush(self.lastDrawingTool)
            if self.interacting == -995 and not(self.mPressed):
                self.interacting = -999
                self.drawing = False
            if self.interacting == -995 and not(self.editingMask):
                t = self.brushSize * (self.sketchZoom/100)
                self.scheduleRegionGivenBrush(rmx, rmy, t)
                steps = math.ceil(math.sqrt((tx-ptx)**2 + (ty-pty)**2)/self.brushSize)+1
                i = 0
                while i <= steps:
                    if self.selectedTool in self.drawingToolsIDs:
                        placeOver(self.layers[self.selectedLayer], self.brush, (ptx + round(i*(tx - ptx)/steps), pty + round(i*(ty - pty)/steps)), True)
                    self.scheduleRegionGivenBrush(rmx, rmy, t)
                    i+=1
                self.updateSketchLayers = True
                self.updateSketch = True
            elif self.interacting == -995 and self.editingMask:
                if type(self.layerProperties[self.selectedLayer][2]) == str:
                    self.layerProperties[self.selectedLayer][2] = self.blankMask.copy()
                _, _, v = colorsys.rgb_to_hsv(self.brushColor[0]/255, self.brushColor[1]/255, self.brushColor[2]/255)
                self.brushColor = (round(v*255), round(v*255), round(v*255), 255)

                self.regenerateBrush(self.lastDrawingTool)
                t = self.brushSize * (self.sketchZoom/100)
                self.scheduleRegionGivenBrush(rmx, rmy, t)
                steps = math.ceil(math.sqrt((tx-ptx)**2 + (ty-pty)**2)/self.brushSize)+1
                i = 0
                while i <= steps:
                    if self.selectedTool in self.drawingToolsIDs:
                        placeOverMask(self.layerProperties[self.selectedLayer][2], self.brush, (ptx + round(i*(tx - ptx)/steps), pty + round(i*(ty - pty)/steps)), True)
                    self.scheduleRegionGivenBrush(rmx, rmy, t)
                    i+=1
                self.updateSketchLayers = True
                self.updateSketch = True
            else:
                pass      
        else:
            if self.interacting == -995: self.interacting = -999
            self.drawing = False

        if self.selectedTool == -93 and self.mouseInSketchSection and self.mRising and self.interacting == -999:
            # Color Picking
            temp = self.regionDataCache[(max(0, min(rmx // 128, 8-1)), max(0, min(rmy // 96, 7-1)))][rmy % 94, rmx % 128]
            temp = (temp[0], temp[1], temp[2], temp[3])
            h, s, v = colorsys.rgb_to_hsv(temp[0]/255, temp[1]/255, temp[2]/255)
            self.interactableVisualObjects[-50][1].setData(h*360) # Hue
            self.interactableVisualObjects[-49][1].setData(temp[3]) # Transparency
            self.interactableVisualObjects[-48][1].updatePos(round(s*163)+62,round((1-v)*100)+20) # Saturation and Value
            self.interactableVisualObjects[-48][1].setColor(temp)
            self.interactableVisualObjects[self.modifyingColor][1].setColor(temp)
            if self.modifyingColor == -47: self.brushColor = temp
            elif self.modifyingColor == -46: self.backColor = temp
            else: pass

            self.brush = generatePaintBrush(self.brushSize, self.brushColor, self.brushStrength)
        
        if self.selectedTool == -94 and self.mouseInSketchSection and self.mRising and self.interacting == -999:
            # Paint Bucket / Flood Filling
            fill(self.layers[self.selectedLayer], (round(self.calcScreenToNonZoomedX(rmx)), round(self.calcScreenToNonZoomedY(rmy))), self.brushColor, self.brushStrength)
            self.scheduleAllRegions()
        
        if self.selectedTool == -98 and self.mouseInSketchSection and self.mPressed and self.interacting == -999:
            # Moving
            if self.mRising:
                if self.editingMask:
                    self.interactableVisualObjects[-997][1].data = [self.mx, self.my, self.editingMask, self.layerProperties[self.selectedLayer][2].copy()]
                else:
                    self.interactableVisualObjects[-997][1].data = [self.mx, self.my, self.editingMask, self.layers[self.selectedLayer].copy()]
            else:
                temp = self.interactableVisualObjects[-997][1].data
                dx, dy = self.mx-temp[0], self.my-temp[1]
                if temp[2]:
                    tempLayer = getRegion(temp[3], addP((0,0), (0-dx,0-dy)), addP(self.imageSize, (0-dx,0-dy)), 2, color = 255, thirdaxis = False)
                    self.layerProperties[self.selectedLayer][2] = tempLayer
                else:
                    tempLayer = getRegion(temp[3], addP((0,0), (0-dx,0-dy)), addP(self.imageSize, (0-dx,0-dy)), 2)
                    self.layers[self.selectedLayer] = tempLayer
                self.scheduleAllRegions()

    def processPopUp(self, im):
        '''Pop Up Area: `(756,20) to (1043,198)`: size `(288,179)`'''
        if self.selectedTool in self.popUpDataIDs:
            img = im.copy()
            if self.previousSelectedTool != self.selectedTool:
                self.previousSelectedTool = self.selectedTool
                temp = []
                for id in self.interactableVisualObjects:
                    if self.interactableVisualObjects[id][0] == "p":
                        temp.append(id)
                for id in temp:
                    self.interactableVisualObjects.pop(id)
                if self.selectedTool == -97: 
                    '''Paint Brush'''
                    self.sliders = [self.c.c(), self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", HorizontalSliderVisualObject("Size", (20,55), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[1]] = ["p", HorizontalSliderVisualObject("Strength", (20,105), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[0]][1].setData(self.brushSize)
                    self.interactableVisualObjects[self.sliders[1]][1].setData(self.brushStrength)
                if self.selectedTool == -96: 
                    '''Pencil'''
                    self.sliders = [self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", HorizontalSliderVisualObject("Size", (20,55), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[0]][1].setData(self.brushSize)
                    self.brushStrength = 100
                if self.selectedTool == -95: 
                    '''Eraser'''
                    self.sliders = [self.c.c(), self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", HorizontalSliderVisualObject("Size", (20,55), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[1]] = ["p", HorizontalSliderVisualObject("Strength", (20,105), 248, (1,100))]
                    self.interactableVisualObjects[self.sliders[0]][1].setData(self.brushSize)
                    self.interactableVisualObjects[self.sliders[1]][1].setData(self.brushStrength)
                if self.selectedTool == -94: 
                    '''Paint Bucket'''
                    self.sliders = [self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", HorizontalSliderVisualObject("Tolerance", (20,55), 248, (0,100))]
                    self.interactableVisualObjects[self.sliders[0]][1].setData(self.brushStrength)
                if self.selectedTool == -92:
                    '''Resize'''
                    self.sliders = [self.c.c(),self.c.c(),self.c.c(),self.c.c(),self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", EditableTextBoxVisualObject("scaleX", (20,55), 100, True)]
                    self.interactableVisualObjects[self.sliders[1]] = ["p", EditableTextBoxVisualObject("scaleY", (100,55), 100, True)]
                    self.interactableVisualObjects[self.sliders[2]] = ["p", EditableTextBoxVisualObject("pixelX", (20,105), self.imageSize[0], True)]
                    self.interactableVisualObjects[self.sliders[3]] = ["p", EditableTextBoxVisualObject("pixelY", (100,105), self.imageSize[1], True)]
                    self.interactableVisualObjects[self.sliders[4]] = ["p", TextButtonPushVisualObject("Resize Image", "Resize", (10,140), 10)]
                if self.selectedTool == -81: 
                    '''Saving'''
                    self.sliders = [self.c.c(), self.c.c()]
                    self.interactableVisualObjects[self.sliders[0]] = ["p", CheckboxVisualObject("Flatten", (10,35), (10,10))]
                    self.interactableVisualObjects[self.sliders[1]] = ["p", TextButtonPushVisualObject("Save To File", "Save", (10,120), 10)]
            else:
                if self.selectedTool == -97: 
                    '''Paint Brush'''
                    placeOver(img, displayText(f"Paint Brush:", "m"), (10,10))
                    placeOver(img, displayText(f"Size: {self.interactableVisualObjects[self.sliders[0]][1].getData()}", "sm"), (10, 35))
                    placeOver(img, displayText(f"Strength: {self.interactableVisualObjects[self.sliders[1]][1].getData()}", "sm"), (10, 85))
                    if self.interacting == -999:
                        temp = [self.interactableVisualObjects[self.sliders[0]][1].getData(), self.interactableVisualObjects[self.sliders[1]][1].getData()]
                        if self.slidersData != temp:
                            self.brushSize = temp[0]
                            self.brushStrength = temp[1]
                            self.slidersData = temp
                            self.regenerateBrush(-97)
                if self.selectedTool == -96: 
                    '''Pencil'''
                    placeOver(img, displayText(f"Pencil:", "m"), (10,10))
                    placeOver(img, displayText(f"Size: {self.interactableVisualObjects[self.sliders[0]][1].getData()}", "sm"), (10, 35))
                    if self.interacting == -999:
                        temp = [self.interactableVisualObjects[self.sliders[0]][1].getData()]
                        if self.slidersData != temp:
                            self.brush = generatePencilBrush(temp[0], self.brushColor)
                            self.brushSize = temp[0]
                            self.slidersData = temp
                            self.regenerateBrush(-96)
                if self.selectedTool == -95:
                    '''Eraser'''
                    placeOver(img, displayText(f"Eraser:", "m"), (10,10))
                    placeOver(img, displayText(f"Size: {self.interactableVisualObjects[self.sliders[0]][1].getData()}", "sm"), (10, 35))
                    placeOver(img, displayText(f"Strength: {self.interactableVisualObjects[self.sliders[1]][1].getData()}", "sm"), (10, 85))
                    if self.interacting == -999:
                        temp = [self.interactableVisualObjects[self.sliders[0]][1].getData(), self.interactableVisualObjects[self.sliders[1]][1].getData()]
                        if self.slidersData != temp:
                            self.brush = generatePencilBrush(temp[0], self.brushColor)
                            self.brushSize = temp[0]
                            self.brushStrength = temp[1]
                            self.slidersData = temp
                            self.regenerateBrush(-95)
                if self.selectedTool == -94:
                    '''Paint Bucket'''
                    placeOver(img, displayText(f"Paint Bucket:", "m"), (10,10))
                    placeOver(img, displayText(f"Tolerance: {self.interactableVisualObjects[self.sliders[0]][1].getData()}", "sm"), (10, 35))
                    if self.interacting == -999:
                        temp = self.interactableVisualObjects[self.sliders[0]][1].getData()
                        if self.brushStrength != temp:
                            self.brushStrength = temp
                if self.selectedTool == -92:
                    '''Resize'''
                    placeOver(img, displayText(f"Saving Options:", "m"), (10,10))
                    placeOver(img, displayText(f"Scale: {0}", "sm"), (10, 35))
                    placeOver(img, displayText(f"Pixels: {0}", "sm"), (10, 85))
                    if self.interacting == self.previousInteracting and self.previousInteracting in self.sliders[:4]:
                        altered = self.sliders.index(self.previousInteracting)
                        if altered == 0: # changed scale X
                            self.interactableVisualObjects[self.sliders[2]][1].updateText(round((float(self.interactableVisualObjects[self.sliders[0]][1].txt)/100)*self.imageSize[0]))
                        if altered == 1: # changed scale Y
                            self.interactableVisualObjects[self.sliders[3]][1].updateText(round((float(self.interactableVisualObjects[self.sliders[1]][1].txt)/100)*self.imageSize[1]))
                        if altered == 2: # changed image X
                            self.interactableVisualObjects[self.sliders[0]][1].updateText(round((float(self.interactableVisualObjects[self.sliders[2]][1].txt)/self.imageSize[0])*100))
                        if altered == 3: # changed image Y
                            self.interactableVisualObjects[self.sliders[1]][1].updateText(round((float(self.interactableVisualObjects[self.sliders[3]][1].txt)/self.imageSize[1])*100))

                if self.selectedTool == -81:
                    '''Saving'''
                    placeOver(img, displayText(f"Saving Options:", "m"), (10,10))
                    placeOver(img, displayText(f"Flatten: {self.interactableVisualObjects[self.sliders[0]][1].state}", "sm"), (30, 37))

                if self.selectedTool == -80: 
                    '''Console'''
                    if len(self.consoleAlerts) > 15: self.consoleAlerts = self.consoleAlerts[-15:]
                    for i in range(len(self.consoleAlerts)):
                        placeOver(img, displayText(f"{self.consoleAlerts[i]}", "s"), (5,i*10))
                    placeOver(img, displayText(f"sketchZoom is {self.sketchZoom}", "s", colorBG = (0,0,0,100)), (5,164))
                    placeOver(img, displayText(f"FPS: {self.fps}", "s", colorBG = (0,0,0,100)), (190,5))
                    placeOver(img, displayText(f"R(S) M Pos:", "s", colorBG = (0,0,0,100)), (190,25))
                    placeOver(img, displayText(f" | ({self.mx-23}, {self.my-36})", "s", colorBG = (0,0,0,100)), (190,45))
                    placeOver(img, displayText(f"Mouse Pressed", "s", colorBG = (0,0,0,100), colorTXT = (0,255,0,255) if self.mPressed else (255,0,0,255)), (190,65))
                    placeOver(img, displayText(f"Rising Edge", "s", colorBG = (0,0,0,100), colorTXT = (0,255,0,255) if self.mRising else (255,0,0,255)), (190,85))
                    placeOver(img, displayText(f"Interacting: {self.interacting}", "s", colorBG = (0,0,0,100)), (190,105))
                    placeOver(img, displayText(f"stringKeyQueue:", "s", colorBG = (0,0,0,100)), (190,125))
                    placeOver(img, displayText(f" | {self.stringKeyQueue}", "s", colorBG = (0,0,0,100)), (190,145))

            for id in self.interactableVisualObjects:
                if self.interactableVisualObjects[id][0] == "p":
                    self.interactableVisualObjects[id][1].tick(img, self.interacting==id)

            if SHOW_CROSSHAIR: placeOver(img, CURSOR_SELECT_ARRAY if self.mPressed else CURSOR_ARROW_ARRAY, (self.mx-756, self.my-20), True)

            return img
        else:
            return EMPTY_IMAGE_ARRAY
    
    def processTools(self, im):
        '''Tools Area: `(1057,20) to (1344,198)`: size `(288,179)`'''
        img = im.copy()
        
        placeOver(img, displayText(f"FPS: {self.fps}", "m", colorBG = (0,0,0,100)), (221,5))
        placeOver(img, displayText(f"obj: {len(self.interactableVisualObjects)}", "m", colorBG = (0,0,0,100)), (221,25))
        # placeOver(img, POINT_IDLE_ARRAY if self.ticks%2 == 0 else POINT_SELECTED_ARRAY, (120,5))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "t":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id or self.selectedTool==id or self.interactableVisualObjects[id][1].getInteractable(self.mx - 1057, self.my - 20))

        if SHOW_CROSSHAIR: placeOver(img, CURSOR_SELECT_ARRAY if self.mPressed else CURSOR_ARROW_ARRAY, (self.mx-1057, self.my-20), True)

        return img

    def processColors(self, im):
        '''Colors Area: `(1057,212) to (1344,366)`: size `(288,155)`'''
        img = im.copy()

        if self.interacting in [-47, -46]: 
            theFutureModifyingColor = self.interacting
        else:
            theFutureModifyingColor = self.modifyingColor

        regenerateColorPicker = False
        if self.colorPickerHue != self.interactableVisualObjects[-50][1].getData() or self.colorPickerTransparency != self.interactableVisualObjects[-49][1].getData():
            self.colorPickerHue = self.interactableVisualObjects[-50][1].getData()
            self.colorPickerTransparency = self.interactableVisualObjects[-49][1].getData()
            self.colorPickerImage = generateColorPicker(self.colorPickerHue/360)
            regenerateColorPicker = True

        if self.previousInteracting == -48 and self.interacting != -48:
            regenerateColorPicker = True
        if self.interacting == -48 or regenerateColorPicker:
            h = self.colorPickerHue/360
            s, v = addP(self.interactableVisualObjects[-48][1].positionO.getPosition(), (-62,-20))
            s = s/163
            v = 1-(v/100)
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            temp = [round(r*255), round(g*255), round(b*255), self.colorPickerTransparency/100*255]
            self.interactableVisualObjects[-48][1].setColor(temp[:3] + [255,])
            self.interactableVisualObjects[self.modifyingColor][1].setColor(temp)
            if self.modifyingColor == -47: self.brushColor = temp
            elif self.modifyingColor == -46: self.backColor = temp
            else: pass
            self.consoleAlerts.append(f"an editing color was updated! {self.modifyingColor}, the future sees {theFutureModifyingColor}")
        if self.previousInteracting == -995 or theFutureModifyingColor != self.modifyingColor:
            if (not self.brushColor in self.pastBrushColors) or (not self.backColor in self.pastBrushColors):
                if not self.brushColor in self.pastBrushColors: self.pastBrushColors.append(self.brushColor)
                if not  self.backColor in self.pastBrushColors: self.pastBrushColors.append( self.backColor)
                if len(self.pastBrushColors) > 10:
                    self.pastBrushColors = self.pastBrushColors[len(self.pastBrushColors)-10:]
                for i in range(10):
                    self.interactableVisualObjects[-79+i][1].setColor(self.pastBrushColors[i])
        if -79 <= self.interacting <= -70 or self.interacting in [-47, -46]:
            temp = self.interactableVisualObjects[self.interacting][1].getColor()
            h, s, v = colorsys.rgb_to_hsv(temp[0]/255, temp[1]/255, temp[2]/255)
            self.interactableVisualObjects[-50][1].setData(h*360) # Hue
            self.interactableVisualObjects[-49][1].setData(temp[3]) # Transparency
            self.interactableVisualObjects[-48][1].updatePos(round(s*163)+62,round((1-v)*100)+20) # Saturation and Value
            self.interactableVisualObjects[-48][1].setColor(temp)
            self.interactableVisualObjects[theFutureModifyingColor][1].setColor(temp)
            if theFutureModifyingColor == -47: self.brushColor = temp
            elif theFutureModifyingColor == -46: self.backColor = temp
            else: pass

        if self.interacting in [-47, -46]: self.modifyingColor = self.interacting

        placeOver(img,  RAINBOW_COLOR_PICKER, (237,20))
        placeOver(img, self.colorPickerImage, (62,20))

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "c":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id or self.modifyingColor==id)

        if SHOW_CROSSHAIR: placeOver(img, CURSOR_SELECT_ARRAY if self.mPressed else CURSOR_ARROW_ARRAY, (self.mx-1057, self.my-212), True)

        return img

    def processLayers(self, im):
        '''Layers Area: `(1057,380) to (1344,677)`: size `(288,298)`'''
        img = im.copy()

        if self.selectedLayer != self.previousSelectedLayer or len(self.layers) != self.numberOfLayers:
            self.interactableVisualObjects[-30][1].updateText(self.layerNames[self.selectedLayer])
            self.previousSelectedLayer = self.selectedLayer
            self.numberOfLayers = len(self.layers)
            self.interactableVisualObjects[-28][1].state = self.layerProperties[self.selectedLayer][0]
            self.interactableVisualObjects[-29][1].state = self.layerProperties[self.selectedLayer][1]
            self.scheduleAllRegions()
        else:
            self.layerNames[self.selectedLayer] = self.interactableVisualObjects[-30][1].txt
            self.layerProperties[self.selectedLayer][0] = self.interactableVisualObjects[-28][1].state
            if self.layerProperties[self.selectedLayer][1] != self.interactableVisualObjects[-29][1].state: 
                self.layerProperties[self.selectedLayer][1] = self.interactableVisualObjects[-29][1].state
                self.scheduleAllRegions()
        
        for i in range(1, len(self.layers)-1):
            xOffset = 0
            index = len(self.layers)-i-1
            if index == self.selectedLayer:
                placeOver(img, generateColorBox((282,40), FRAME_COLOR_RGBA), (3,50*i-4-self.layersOffset))
            placeOver(img, displayText(f"{index}", "m", colorTXT = (255,155,155,255) if self.layerProperties[index][0] else (255,255,255,255)), (8 + xOffset, 7+50*i-self.layersOffset))
            temp = setTransparency(setLimitedSizeSize(self.layers[index], (60, 34)), 100 if self.layerProperties[index][1] else 50)
            if self.selectedLayer == index and not(self.editingMask):
                placeOver(temp, generateInwardsBorderBox((temp.shape[1], temp.shape[0]), 2, SELECTED_COLOR_RGBA), (0,0))
            placeOver(img, temp, (20 + xOffset, 0+50*i-self.layersOffset))
            if not(type(self.layerProperties[index][2]) == str):
                temp = setTransparency(setLimitedSizeSize(maskToImage(self.layerProperties[index][2]), (60, 34)), 100 if self.layerProperties[index][1] else 50)
                if self.selectedLayer == index and self.editingMask:
                    placeOver(temp, generateInwardsBorderBox((temp.shape[1], temp.shape[0]), 2, SELECTED_COLOR_RGBA), (0,0))
                placeOver(img, temp, (84 + xOffset, 0+50*i-self.layersOffset))
                xOffset = 65
            placeOver(img, displayText(f"{self.layerNames[index]}", "m", colorTXT = (255,255,255,255) if self.layerProperties[index][1] else (155,155,155,255)), (85 + xOffset, 7+50*i-self.layersOffset))
            if not(self.layerProperties[index][1]):
                placeOver(img, ICON_HIDDEN_ARRAY, (249, 18+50*i-self.layersOffset))
            if self.layerProperties[index][0]:
                placeOver(img,   ICON_LOCK_ARRAY, (267, 18+50*i-self.layersOffset))
            
            if 7+50*(i+1)-self.layersOffset > 288:
                break

        for id in self.interactableVisualObjects:
            if self.interactableVisualObjects[id][0] == "l":
                self.interactableVisualObjects[id][1].tick(img, self.interacting==id)
        
        if SHOW_CROSSHAIR: placeOver(img, CURSOR_SELECT_ARRAY if self.mPressed else CURSOR_ARROW_ARRAY, (self.mx-1057, self.my-380), True)

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
        for ix in range(cornerB[0]-cornerA[0]+2):
            for iy in range(cornerB[1]-cornerA[1]+2):
                self.scheduleRegion((cornerA[0]+ix, cornerA[1]+iy))
        
    def scheduleRegionGivenPixel(self, pixel):
        region = (max(0, min(pixel[0] // 128, 8-1)), max(0, min(pixel[1] // 96, 7-1)))
        if region in self.updateSketchRegions:
            self.updateSketchRegions.remove(region)
        self.updateSketchRegions.append(region)

    def scheduleRegion(self, region):
        safeRegion = (max(0, min(region[0], 8-1)), max(0, min(region[1], 7-1)))
        if safeRegion in self.updateSketchRegions:
            self.updateSketchRegions.remove(safeRegion)
        self.updateSketchRegions.append(safeRegion)

    def scheduleAllRegions(self, regenLayer = True):
        if regenLayer: self.scheduleAllRegionLayers()
        for region in ALL_REGIONS:
            if region not in self.updateSketchRegions:
                self.updateSketchRegions.append(region)

    def scheduleAllRegionLayers(self):
        for region in ALL_REGIONS:
            if region not in self.updateSketchRegionLayers:
                self.updateSketchRegionLayers.append(region)

    def regenerateBrush(self, tool):
        if tool == -97: 
            '''Paint Brush'''
            self.brush = generatePaintBrush(self.brushSize, self.brushColor, self.brushStrength)
            self.consoleAlerts.append(f"{self.ticks} - generated a paint brush!")
        elif tool == -96: 
            '''Pencil'''
            self.brush = generatePencilBrush(self.brushSize, self.brushColor)
            self.consoleAlerts.append(f"{self.ticks} - generated a pencil brush!")
        elif tool == -95: 
            '''Eraser'''
            self.brush = generateEraserBrush(self.brushSize, self.brushStrength)
            self.consoleAlerts.append(f"{self.ticks} - generated an eraser brush!")
        return self.brush
    
    def saveDrawing(self):
        if self.interactableVisualObjects[self.sliders[0]][1].state:
            path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp"), ("TIFF files", "*.tiff;*.tif"), ("GIF files", "*.gif"), ("All files", "*.*")])
            if path != "":
                total = self.blankLayer.copy()
                for i in range(len(self.layers)):
                    if self.layerProperties[i][1]:
                        c = self.layers[i].copy()
                        if type(self.layerProperties[i][2]) != str:
                            applyMask(c, self.layerProperties[i][2])
                        placeOver(total, c, (0,0))
                img = Image.fromarray(total)
                img.save(path)
        else:
            path = filedialog.asksaveasfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".protoplop", filetypes=[("Protoplop file", "*.protoplop"), ("All files", "*.*")])
            if path != "":
                self.projectPath = path
                self.projectLastSaved = round(time.time())
                export = []
                export.append(VERSION)
                # Image (General)
                export.append(self.imageSize)
                # Layers
                export.append([arrayToRawImage(layer) for layer in self.layers])
                export.append(self.layerNames)
                temp = self.layerProperties.copy()
                for i in range(len(temp)): 
                    if type(temp[i][2]) != str:
                        temp[i][2] = arrayToRawImage(temp[i][2])
                export.append(temp)

                with open(path, "w") as f:
                    f.write(str(export))
                    f.close()

    def loadDrawing(self):
        path = filedialog.askopenfilename(initialdir=PATH_SAVE_DEFAULT, defaultextension=".protoplop", filetypes=[("Protoplop file", "*.protoplop"), ("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp"), ("TIFF files", "*.tiff;*.tif"), ("GIF files", "*.gif"), ("All files", "*.*")])
        if path != "":
            if path.endswith(".protoplop"):
                with open(path, "r") as f:
                    file = f.read()
                    drawing = ast.literal_eval(file)
                    f.close()
                # Image (General)
                self.imageSize = drawing[1]
                # Layers
                self.layers = [rawImageToArray(rawImage) for rawImage in drawing[2]]
                self.layerNames = drawing[3]
                temp = drawing[4]
                for i in range(len(temp)):
                    if type(temp[i][2]) != str:
                        temp[i][2] = rawImageToArray(temp[i][2]) 
                self.layerProperties = temp
            else:
                img = numpy.array(Image.open(path).convert("RGBA"))
                self.__init__((img.shape[1],img.shape[0]))
                self.layers[1] = img

    def saveState(self):
        pass

    def close(self):
        pass
