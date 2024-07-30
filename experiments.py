import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import *
from subsystems.label import LabelWrapper
from subsystems.simplefancy import generatePaintBrush
from settings import *

img = generatePaintBrush(100,(50,20,255,127),100)

Image.fromarray(img).show()