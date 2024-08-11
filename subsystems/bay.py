'''This file contatins some functions for saving and importing things!'''

import numpy, io
from settings import *

def arrayToRawNumpy(img:numpy.ndarray):
    '''Given an array, returns to .npy binary data'''
    out = io.BytesIO()
    numpy.save(out, img)
    return out.getvalue()

def rawNumpyToArray(raw):
    '''The raw array is turned into an array'''
    binary = io.BytesIO(raw)
    image = numpy.load(binary)
    return image

def arrayToRawImage(img:numpy.ndarray):
    '''Given an array it returns the .png binary data'''
    out = io.BytesIO()
    Image.fromarray(img).save(out, "PNG")
    return out.getvalue()

def rawImageToArray(raw):
    '''Given a raw image, it will return it as a numpy array'''
    binary = io.BytesIO(raw)
    image = numpy.array(Image.open(binary))
    return image