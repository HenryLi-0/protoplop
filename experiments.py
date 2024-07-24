import tkinter as tk
import numpy, time, math
from PIL import Image, ImageTk
from subsystems.render import getRegion

IMAGE_ARRAY = numpy.array(Image.open("C:/Users/henry/Downloads/tape.jpg").convert("RGBA"))
IMAGE_SIZE = (IMAGE_ARRAY.shape[1], IMAGE_ARRAY.shape[0])

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CHUNK_SIZE = 128


class Window:
    def __init__(self):
        '''initalize tk window'''
        self.window= tk.Tk()
        self.window.grid()
        self.window.title("Protoplop")
        self.window.geometry("1366x698")
        self.window.configure(background="#005555")
        self.fps = 0
        self.fpsCounter = 0
        self.fpsGood = False
        self.mPressed = False

        self.canvas = tk.Canvas(self.window, width=1350, height=650, bg='white')
        self.canvas.pack()

    def windowProcesses(self):
        '''window processes'''
        mx = self.window.winfo_pointerx()-self.window.winfo_rootx()
        my = self.window.winfo_pointery()-self.window.winfo_rooty()
        if self.mPressed > 0:
            self.mPressed += 1
        else:
            self.mPressed = 0


        copy = getRegion(IMAGE_ARRAY, (1350-mx,650-my), (1350+1350-mx, 650+650-my))
        photo = ImageTk.PhotoImage(Image.fromarray(copy))


        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

        self.cache = photo

        print(f"beep {time.time()}")

        self.window.after(30, self.windowProcesses)

        self.fpsCounter +=1
        if math.floor(time.time()) == round(time.time()) and not(self.fpsGood):
            self.fps = self.fpsCounter
            self.fpsCounter = 0
            self.fpsGood = True
        if math.ceil(time.time()) == round(time.time()) and self.fpsGood:
            self.fpsGood = False
        print(f"FPS: {self.fps}")

    def windowOccasionalProcesses(self):
        '''window processes that happen less frequently (once every 5 seconds)'''
        print("windowOccaionalProcess")
        print(self.getFPS())
        self.window.after(5000, self.windowOccasionalProcesses)

    def windowStartupProcesses(self):
        '''window processes that occur once when startup'''
        print("windowStartupProcess")
        pass
    
    def getFPS(self): return self.fps
    def mPress(self, side = 0): self.mPressed = 1
    def mRelease(self, side = 0): self.mPressed = -999
    def keyPressed(self, key): self.keyQueue.append(str(key.keysym))
    def mouseWheel(self, event): self.mouseScroll -= event.delta
    
    def start(self):
        '''start window main loop'''
        print("windowStart")
        
        self.window.bind("<ButtonPress-1>", self.mPress)
        self.window.bind("<ButtonRelease-1>", self.mRelease)
        self.window.bind("<Key>", self.keyPressed)
        self.window.bind_all("<MouseWheel>", self.mouseWheel)

        self.window.after(30, self.windowProcesses)
        self.window.after(30, self.windowOccasionalProcesses)
        self.window.mainloop()
        self.window.after(0, self.windowStartupProcesses)


window = Window()
window.start()
