import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import *
from subsystems.label import LabelWrapper
from subsystems.simplefancy import generatePaintBrush
from settings import *

# bigImage1 = generateColorBox((1024,658))
# bigImage2 = generateColorBox((1024,658), (50,50,50,50))

# total = 0
# for i in range(100):
#     start = time.time()
#     placeOver(bigImage1, bigImage2, (0,0))
#     end = time.time()
#     total += end-start
#     print(f"{i+1} tests | {total/(i+1)}s each")

print(ALL_REGIONS)