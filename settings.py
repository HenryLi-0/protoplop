'''
Settings

Here are the parts:
- Calculation
- Visuals
- Saving
- Keybinds
- Constants (Please do not change!)
'''

'''Calculation'''
FLOAT_ACCURACY = 3 #This is how many digits after the decimal point things will generally round to

'''Visuals'''
INTERFACE_FPS = 60 # The interface window will be called every 1/INTERFACE_FPS seconds
TICK_MS = 1 #round((1/INTERFACE_FPS)*1000)
OCCASIONAL_TICK_MS = 5000 # Highly recommended to keep above 1 second, as it runs processes that do not need updates every tick

SKETCH_QUALITY = 1 # The display quality of the sketch SHOWN computationally. 1 is the highsst, the greater you go, the more pixelated it gets
SKETCH_MAX_REGIONS = 5 # The maximum allowed regions of the sketch screen (total 48) allowed to be updated per call to update
SKETCH_MAX_REGIONS_TIME = 0.1 # The maximum allowed time to spend on region updates per tick

SHOW_CROSSHAIR = True # Shows a crosshair for the mouse's position, meant for touch-screen based drawing use
DEFAULT_IMAGE_SIZE = (1366,697)

hexColorToRGBA = lambda hexcolor: tuple(int(hexcolor[i:i+2], 16) for i in (1, 3, 5)) + (255,)

BACKGROUND_COLOR = "#333247" #Background color
FRAME_COLOR      = "#524f6b" #Borders and Frame color
SELECTED_COLOR   = "#bebcd5" #Selected Element color
VOID_COLOR       = "#84829b" #Void color

BACKGROUND_COLOR_RGBA = hexColorToRGBA(BACKGROUND_COLOR)
FRAME_COLOR_RGBA      = hexColorToRGBA(FRAME_COLOR     )
SELECTED_COLOR_RGBA   = hexColorToRGBA(SELECTED_COLOR  )
VOID_COLOR_RGBA       = hexColorToRGBA(VOID_COLOR      )

'''Saving'''
import os, time
PATH_SAVE_DEFAULT = os.path.join("saves")

FORMAT_TIME = lambda x: time.strftime("%I:%M:%S %p %m/%d/%Y", time.localtime(x))

'''Keybinds'''
KB_IGNORE    = ["Win_L"]                                                                                # Keys to ignore
KB_ZOOM      = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("space" in keys)            # Zooming
KB_FOCUS     = lambda keys: (len(keys) == 2) and ("Control_L" in keys) and ("F" in keys or "f" in keys) # Center Screen
KB_L_MV_UP   = lambda keys: (len(keys) == 2) and ("Alt_L" in keys) and ("Up" in keys)                   # Move Selected Layer Up
KB_L_MV_DOWN = lambda keys: (len(keys) == 2) and ("Alt_L" in keys) and ("Down" in keys)                 # Move Selected Layer Down
KB_L_NEW     = lambda keys: (len(keys) == 2) and ("Alt_L" in keys) and ("A" in keys or "a" in keys)     # Create a new layer
KB_L_DELETE  = lambda keys: (len(keys) == 2) and ("Alt_L" in keys) and ("S" in keys or "s" in keys)     # Delete a layer
KB_T_NONE    = lambda keys: (len(keys) == 1) and ("N" in keys or "n" in keys)                           # Switch to tool None
KB_T_MOVE    = lambda keys: (len(keys) == 1) and ("M" in keys or "m" in keys)                           # Switch to tool Move 
KB_T_BRUSH   = lambda keys: (len(keys) == 1) and ("B" in keys or "b" in keys)                           # Switch to tool Brush 
KB_T_PENCIL  = lambda keys: (len(keys) == 1) and ("P" in keys or "p" in keys)                           # Switch to tool Pencil 
KB_T_ERASER  = lambda keys: (len(keys) == 1) and ("E" in keys or "e" in keys)                           # Switch to tool Eraser 
KB_T_BUCKET  = lambda keys: (len(keys) == 1) and ("G" in keys or "g" in keys)                           # Switch to tool Bucket 
KB_T_EYEDROP = lambda keys: (len(keys) == 1) and ("I" in keys or "i" in keys)                           # Switch to tool Eyedrop 

'''Constants - DO NOT CHANGE!!!'''
'''Do not change these constants. Some are probably important. Some are used for testing purposes. 
   Editing certain constants will break things! You have been warned!'''
from PIL import Image, ImageFont
import numpy
from subsystems.simplefancy import *

# Version
VERSION = "v1.0.0"

ICON_SPACING = lambda x,y: (6+43*x, 6+43*y)

ALL_REGIONS = [(x,y) for x in range(8) for y in range(7)]

from subsystems.simplefancy import generateRainbowColorPicker

RAINBOW_COLOR_PICKER = generateRainbowColorPicker()

# Imagery
LOADING_IMAGE = Image.open(os.path.join("resources", "loading.png")).convert("RGBA") # 1366x697, Solid, Loading Screen
LOADING_IMAGE_ARRAY = numpy.array(LOADING_IMAGE)
EMPTY_LARGE_IMAGE = Image.open(os.path.join("resources", "blank_large.png")).convert("RGBA")
EMPTY_LARGE_IMAGE_ARRAY = numpy.array(EMPTY_LARGE_IMAGE)
PLACEHOLDER_IMAGE = Image.open(os.path.join("resources", "placeholder", "placeholder.png")).convert("RGBA")    # 512x512, Solid, [black, white, grey]
PLACEHOLDER_IMAGE_ARRAY = numpy.array(PLACEHOLDER_IMAGE)
PLACEHOLDER_IMAGE_2 = Image.open(os.path.join("resources", "placeholder", "placeholder2.png")).convert("RGBA")  # 100x100, Transparent Background [black, white, grey]
PLACEHOLDER_IMAGE_2_ARRAY = numpy.array(PLACEHOLDER_IMAGE_2)
PLACEHOLDER_IMAGE_3 = Image.open(os.path.join("resources", "placeholder", "placeholder3.png")).convert("RGBA")  # 128x128, Solid Background [black, white, grey]
PLACEHOLDER_IMAGE_3_ARRAY = numpy.array(PLACEHOLDER_IMAGE_3)
PLACEHOLDER_IMAGE_4 = Image.open(os.path.join("resources", "placeholder", "placeholder4.png")).convert("RGBA")  # 16x16, Transparent Background [black, white]
PLACEHOLDER_IMAGE_4_ARRAY = numpy.array(PLACEHOLDER_IMAGE_4)
PLACEHOLDER_IMAGE_5 = Image.open(os.path.join("resources", "placeholder", "placeholder5.png")).convert("RGBA")  # 32x32, Solid Background [rainbow]
PLACEHOLDER_IMAGE_5_ARRAY = numpy.array(PLACEHOLDER_IMAGE_5)
MISSING_IMAGE_PATH = os.path.join("resources", "missing.png")
MISSING_IMAGE = Image.open(os.path.join("resources", "missing.png")).convert("RGBA")
MISSING_IMAGE_ARRAY = numpy.array(MISSING_IMAGE)
EMPTY_IMAGE_ARRAY = numpy.zeros((1, 1, 4), dtype=numpy.uint8)

# Fonts
FONT_LARGE = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 24)
FONT_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 15)
FONT_SMALL_MEDIUM = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 12)
FONT_SMALL = ImageFont.truetype(os.path.join("resources", "Comfortaa-Medium.ttf"), 10)
EDITOR_SPACING = lambda x: x*20+15

# Blank Interface Sections
'''
- Sketch Area:   `(  20,  20) to (1043, 677)` : size `(1024, 658)`
- Tools Area:    `(1057,  20) to (1344, 198)` : size `( 288, 179)`
- Colors Area:   `(1057, 212) to (1344, 366)` : size `( 288, 155)`
- Layers Area:   `(1057, 380) to (1344, 677)` : size `( 288, 298)`
- Entire Screen: `(   0,   0) to (1365, 697)` : size `(1366, 698)`
'''

FRAME_SKETCH_INSTRUCTIONS = genereateThemedBorderRectangleInstructions((1024, 658),hexColorToRGBA(FRAME_COLOR))
FRAME_TOOLS_INSTRUCTIONS  = genereateThemedBorderRectangleInstructions(( 288, 179),hexColorToRGBA(FRAME_COLOR))
FRAME_COLORS_INSTRUCTIONS = genereateThemedBorderRectangleInstructions(( 288, 155),hexColorToRGBA(FRAME_COLOR))
FRAME_LAYERS_INSTRUCTIONS = genereateThemedBorderRectangleInstructions(( 288, 298),hexColorToRGBA(FRAME_COLOR))
GEAR = Image.open(os.path.join("resources", "gear.png")).convert("RGBA")
GEAR_ARRAY = numpy.array(GEAR)
PLAY_BUTTON = Image.open(os.path.join("resources", "play.png")).convert("RGBA")
PLAY_BUTTON_ARRAY = numpy.array(PLAY_BUTTON)
PAUSE_BUTTON = Image.open(os.path.join("resources", "pause.png")).convert("RGBA")
PAUSE_BUTTON_ARRAY = numpy.array(PAUSE_BUTTON)

CURSOR_ARROW = Image.open(os.path.join("resources", "cursor_arrow.png")).convert("RGBA")
CURSOR_ARROW_ARRAY = numpy.array(CURSOR_ARROW)
CURSOR_SELECT = Image.open(os.path.join("resources", "cursor_select.png")).convert("RGBA")
CURSOR_SELECT_ARRAY = numpy.array(CURSOR_SELECT)

ORB_IDLE = Image.open(os.path.join("resources", "orb_idle.png")).convert("RGBA")
ORB_IDLE_ARRAY = numpy.array(ORB_IDLE)
ORB_SELECTED = Image.open(os.path.join("resources", "orb_selected.png")).convert("RGBA")
ORB_SELECTED_ARRAY = numpy.array(ORB_SELECTED)
POINT_IDLE = Image.open(os.path.join("resources", "point_idle.png")).convert("RGBA")
POINT_IDLE_ARRAY = numpy.array(POINT_IDLE)
POINT_SELECTED = Image.open(os.path.join("resources", "point_selected.png")).convert("RGBA")
POINT_SELECTED_ARRAY = numpy.array(POINT_SELECTED)
UP_ARROW_ARRAY = numpy.array(Image.open(os.path.join("resources", "up_arrow.png")).convert("RGBA"))
DOT_IDLE_ARRAY = numpy.array(Image.open(os.path.join("resources", "dot_idle.png")).convert("RGBA"))
DOT_SELECTED_ARRAY = numpy.array(Image.open(os.path.join("resources", "dot_selected.png")).convert("RGBA"))
PLUS_SIGN_ARRAY = numpy.array(Image.open(os.path.join("resources", "plus.png")).convert("RGBA"))
TRASHCAN_ARRAY = numpy.array(Image.open(os.path.join("resources", "trashcan.png")).convert("RGBA"))
IMPORT_ARRAY = numpy.array(Image.open(os.path.join("resources", "import.png")).convert("RGBA"))
SAVE_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "save.png")).convert("RGBA"))
LOAD_ICON_ARRAY = numpy.array(Image.open(os.path.join("resources", "load.png")).convert("RGBA"))

ICON_NONE_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "none.png")).convert("RGBA"))
ICON_MOVE_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "move.png")).convert("RGBA"))
ICON_BRUSH_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "paintbrush.png")).convert("RGBA"))
ICON_PENCIL_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "pencil.png")).convert("RGBA"))
ICON_ERASER_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "eraser.png")).convert("RGBA"))
ICON_BUCKET_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "bucket.png")).convert("RGBA"))
ICON_EYEDROP_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "eyedrop.png")).convert("RGBA"))
ICON_RESIZE_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "resize.png")).convert("RGBA"))

ICON_CONSOLE_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "console.png")).convert("RGBA"))
ICON_SAVE_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "save.png")).convert("RGBA"))
ICON_OPEN_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "import.png")).convert("RGBA"))

ICON_SHOWN_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "shown.png")).convert("RGBA"))
ICON_HIDDEN_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "hidden.png")).convert("RGBA"))
ICON_LOCK_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "lock.png")).convert("RGBA"))
ICON_UNLOCK_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "unlock.png")).convert("RGBA"))
ICON_PLUS_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "plus.png")).convert("RGBA"))
ICON_TRASHCAN_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "trashcan.png")).convert("RGBA"))
ICON_LAYERMASK_ARRAY = numpy.array(Image.open(os.path.join("resources", "icon", "layermask.png")).convert("RGBA"))