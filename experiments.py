import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CHUNK_SIZE = 128

class ChunkedCanvas(tk.Canvas):
    def __init__(self, parent, width, height, chunk_size):
        super().__init__(parent, width=width, height=height, bg='white')
        self.chunk_size = chunk_size
        self.chunks = {}
        self.image_cache = {}
        self.bind("<B1-Motion>", self.paint)
        
    def ticktick(self):
        for chunk in self.chunks:
            print(f"chunk: {chunk} ticked")
            self.update_chunk_image(chunk)
        
    def get_chunk_key(self, x, y):
        return (x // self.chunk_size, y // self.chunk_size)
    
    def paint(self, event):
        chunk_key = self.get_chunk_key(event.x, event.y)
        if chunk_key not in self.chunks:
            self.chunks[chunk_key] = np.ones((self.chunk_size, self.chunk_size, 3), dtype=np.uint8)*5
        
        chunk = self.chunks[chunk_key]
        local_x = event.x % self.chunk_size
        local_y = event.y % self.chunk_size
        chunk[local_y, local_x] = [255, 255, 255]  # Draw black
        
        self.update_chunk_image(chunk_key, chunk)
        
    def update_chunk_image(self, chunk_key, chunk = ""):
        if type(chunk) != np.ndarray:
            image = Image.fromarray(chunk, 'RGB')
            self.chunks[chunk_key] = image
            photo = ImageTk.PhotoImage(image)
        else:
            photo = ImageTk.PhotoImage(Image.fromarray(self.chunks[chunk_key]))
        
        x0, y0 = chunk_key[0] * self.chunk_size, chunk_key[1] * self.chunk_size
        self.create_image(x0, y0, image=photo, anchor=tk.NW)
        self.image_cache[chunk_key] = photo  # Prevent image from being garbage collected

class windowthing:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chunked Drawing Canvas")

        self.canvas = ChunkedCanvas(self.root, CANVAS_WIDTH, CANVAS_HEIGHT, CHUNK_SIZE)
        self.canvas.pack()

        self.root.mainloop()
        
    def start(self):
        self.root.after(33, self.canvas.tick)
        self.root.after(33, self.start)

thing = windowthing()
thing.start()