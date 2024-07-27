'''This file contains classes all about the visual objects the user sees'''

import time, numpy, random, math
from subsystems.render import placeOver
from subsystems.fancy import displayText, generateColorBox, generateBorderBox
from subsystems.point import *
from settings import *

class VisualManager:
    def __init__(self, worker, pruneCount = 5, maxLength = 15):
        '''A class for caching recently processed inputs in order to save on loading time and CPU power'''
        self.cache = {}
        self.memoryManage = []
        self.worker = worker
        self.pruneCount = min(pruneCount,maxLength)
        self.maxLength = maxLength
    def process(self, key):
        '''Process and caches an input's output if the input was not recently processed'''
        if not(str(key) in self.cache):
            self.cache[str(key)] = self.worker.get(key)
            self.memoryManage.append(time.time())
    def getRender(self, key):
        '''Returns an input's output if the input was recently processed, otherwise processes the input and returns the output'''
        self.process(key)
        key = str(key)         
        self.memoryManage[list(self.cache.keys()).index(key)] = time.time()
        if len(self.memoryManage) > self.maxLength:
            prune = self.memoryManage.copy()
            prune.sort()
            prune = prune[0:self.pruneCount]
            for item in prune:
                i = self.memoryManage.index(item)
                self.cache.pop(list(self.cache.keys())[i])
                self.memoryManage.pop(i)
        return self.cache[key]
    
'''Hitboxes'''

class CircularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific ciruclar range'''
    def __init__(self, r:int = 10, ix = 0, iy = 0):
        '''Circular detection box will be centered!'''
        self.r, self.ix, self.iy = r, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy): 
        '''Returns whether or not the mouse is in range of interaction'''
        return math.sqrt((rmx-self.ix)**2 + (rmy-self.iy)**2) <= self.r
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getR(self): return self.r
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setR(self, nr): self.r = nr

class RectangularPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific bounding box'''
    def __init__(self, bbox:tuple|list = (10,10), ix = 0, iy = 0):
        '''Bounding box will NOT be centered!'''
        self.bbox, self.ix, self.iy = bbox, ix, iy
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        if interact: self.ix, self.iy = rmx, rmy
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the bounding box of interaction'''
        return (self.ix < rmx) and (rmx < (self.ix+self.bbox[0])) and (self.iy < rmy) and (rmy < (self.iy+self.bbox[1]))
    def getPosition(self): return (self.ix, self.iy)
    def getX(self): return self.ix
    def getY(self): return self.iy
    def getBBOX(self): return self.bbox
    def setPosition(self, position: tuple|list): self.ix, self.iy = position
    def setX(self, nx): self.ix = nx
    def setY(self, ny): self.iy = ny
    def setBBOX(self, nbbox): self.bbox = nbbox

class FixedRegionPositionalBox:
    '''Just remembers where the object is supposed to be on screen, given the mouse position and updates when the mouse is in a specific region. Not movable by interaction.'''
    def __init__(self, pointA:tuple|list = (0,0), pointB:tuple|list = (10,10)):
        '''Point A and Point B are two opposite corners of a region!'''
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))
    def process(self, interact, rmx, rmy):
        '''Should be called whenever the position wants to question its position'''
        pass
    def getInteract(self, rmx, rmy):
        '''Returns whether or not the mouse is in the region of interaction'''
        return (self.pointA[0] < rmx) and (rmx < self.pointB[0]) and (self.pointA[1] < rmy) and (rmy < self.pointB[1])
    def getPosition(self): return self.pointA
    def getX(self): return self.pointA[0]
    def getY(self): return self.pointA[1]
    def getRegion(self): return (self.pointA, self.pointB)
    def setPosition(self, position: tuple|list): 
        self.pointB = subtractP(self.pointB, subtractP(self.pointA, position))
        self.pointA = position
    def setRegion(self, pointA, pointB):
        self.pointA = (min(pointA[0], pointB[0]), min(pointA[1], pointB[1]))
        self.pointB = (max(pointA[0], pointB[0]), max(pointA[1], pointB[1]))

'''Visual Objects'''

from settings import ORB_IDLE_ARRAY, ORB_SELECTED_ARRAY, CURSOR_SELECT_ARRAY

class OrbVisualObject:
    '''A movable point.'''
    def __init__(self, name):
        self.type = "orb"
        self.name = name
        self.positionO = CircularPositionalBox(50)
        self.positionO.setPosition((random.randrange(0,903), random.randrange(0,507)))
    def tick(self, c, active):
        c.placeOver(ORB_SELECTED_ARRAY if active else ORB_IDLE_ARRAY, self.positionO.getPosition(), True)
        c.placeOver(displayText(self.name, "m"), self.positionO.getPosition(), True)
    def updatePos(self, rmx, rmy):
        self.positionO.setPosition((rmx, rmy))
    def keepInFrame(self, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < 0 or maxX < pos[0] or pos[1] < 0 or maxY < pos[1]:
            self.positionO.setPosition((max(0,min(pos[0],maxX)), max(0,min(pos[1],maxY))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)

class ButtonVisualObject:
    '''A button.'''
    def __init__(self, name, pos:tuple|list, img:numpy.ndarray, img2:numpy.ndarray):
        self.type = "button"
        self.name = name
        self.img = img
        self.img2 = img2
        self.positionO = RectangularPositionalBox((img.shape[1],img.shape[0]), pos[0], pos[1])
    def tick(self, c, active):
        c.placeOver(self.img2 if active else self.img, self.positionO.getPosition(), False)
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < 0 or maxX < pos[0] or pos[1] < 0 or maxY < pos[1]:
            self.positionO.setPosition((max(0,min(pos[0],maxX)), max(0,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class EditableTextBoxVisualObject:
    '''An editable text box.'''
    def __init__(self, name, pos:tuple|list, startTxt= ""):
        self.type = "textbox"
        self.name = name
        self.txt = startTxt
        self.txtImg = displayText(self.txt, "m")
        self.positionO = RectangularPositionalBox((max(self.txtImg.shape[1],10),max(self.txtImg.shape[0],23)), pos[0], pos[1])
    def tick(self, c, active):
        c.placeOver(generateColorBox(self.positionO.getBBOX(), hexColorToRGBA(FRAME_COLOR) if active else hexColorToRGBA(BACKGROUND_COLOR)), self.positionO.getPosition())
        c.placeOver(self.txtImg, self.positionO.getPosition(), False)
    def updateText(self, txt):
        if self.txt!=txt:
            self.txt = txt
            self.txtImg = displayText(self.txt, "m")
            self.positionO.setBBOX((max(self.txtImg.shape[1]+3,10),max(self.txtImg.shape[0],23)))
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < 0 or maxX < pos[0] or pos[1] < 0 or maxY < pos[1]:
            self.positionO.setPosition((max(0,min(pos[0],maxX)), max(0,min(pos[1],maxY))))
    def getInteractable(self,rmx,rmy):
        return self.positionO.getInteract(rmx, rmy)
    
class DummyVisualObject:
    '''I sit around doing nothing and can store data. A little better that one group member in randomly assigned class projects. That person didn't deserve that 100, did they now? (joke)'''
    def __init__(self, name, pos:tuple|list, data = None):
        self.type = "dummy"
        self.name = name
        self.positionO = RectangularPositionalBox((0,0), pos[0], pos[1])
        self.data = data
    def tick(self, c, active):
        pass
    def updatePos(self, rmx, rmy):
        pass
    def keepInFrame(self, maxX, maxY):
        pass
    def getInteractable(self,rmx,rmy):
        return False

class PointVisualObject:
    '''A smaller movable point OFFSET BY X29,Y242 FOR GRAPH. MEANT FOR THE GRAPH AND THE GRAPH ONLY.'''
    def __init__(self, name, pos:tuple|list=(random.randrange(0,20), random.randrange(0,20))):
        self.type = "point"
        self.name = name
        self.positionO = CircularPositionalBox(15)
        self.positionO.setPosition(pos)
        self.pointData = ""
    def tick(self, c, active):
        place = addP(self.positionO.getPosition(), (29,242))
        if 27<=place[0] and 221<=place[1] and place[0]<=383 and place[1]<=477:
            c.placeOver(POINT_SELECTED_ARRAY if active else POINT_IDLE_ARRAY, place, True)
        if type(self.pointData)in [int, float]:
            if active: c.placeOver(displayText(str(roundf(self.pointData, FLOAT_ACCURACY)), "m"), addP(self.positionO.getPosition(), (29,222)), True)
        else:
            if active: c.placeOver(displayText(str(self.pointData), "m"), addP(self.positionO.getPosition(), (29,222)), True)
        if active: return self.pointData
    def updatePos(self, rmx, rmy):
        self.positionO.setPosition((rmx, rmy))
    def setPointData(self, data):
        self.pointData = data
    def keepInFrame(self, maxX, maxY):
        pos = self.positionO.getPosition()
        if pos[0] < 0 or maxX < pos[0] or pos[1] < 0 or maxY < pos[1]:
            self.positionO.setPosition((round(max(0,min(pos[0],maxX))), round(max(0,min(pos[1],maxY)))))
    def getInteractable(self, rmx, rmy):
        return self.positionO.getInteract(rmx, rmy)