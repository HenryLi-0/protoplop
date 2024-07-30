import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import *
from subsystems.label import LabelWrapper
from subsystems.simplefancy import generateColorBox
from settings import *

img = generateColorBox((100,100),(0,0,0,0))
placeOver(img, ORB_IDLE_ARRAY, (50,50))
placeOver(img, ORB_IDLE_ARRAY, (75,75))
placeOver(img, PLACEHOLDER_IMAGE_2_ARRAY, (25,25))

Image.fromarray(img).show()