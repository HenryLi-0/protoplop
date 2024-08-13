# Code Guide

Hello! Looks like you're interested in this code for whatever reason (75% chance it's future me who forgot what this is all about...)! Anyways, here's the way this code is stored:

**protoplop/** 

where the most important things are
- `main.py` : just initializes the window after checking
- `SETTINGS.py` : contains important constants, and some editable settings
- `README.md` : the readme.md?
- `CODEGUIDE.md` : idk what to call it, but here's some documentation on what files do
- `MANUAL.md` : a little instruction manual for default keybinds and things

not really relevant stuff
- `experiments.py` : not really relevant to stuff yet


**protoplop/subsystems/** 

where useful code exists across different files
- `bay.py` : used for converting things between image and numpy arrays, used for saving
- `checks.py` : checks that important resources exist to prevent random crashes
- `counter.py` : just a counter, but it is shockingly important!
- `fancy.py` : used for fancy rendering stuff, requires imports from `SETTINGS.py`!
- `interface.py` : parts of the tk window, contains most of the code
- `label.py` : contains a simple wrapper for labels, used for the tk window!
- `point.py` : contains simple functions/methoeds related to points
- `render.py` : things related to rendering and image stuff
- `simplefancy.py` : used for fancy rendering stuff, but does not require imprts from `SETTINGS.py`!
- `visuals.py` : very silly way for buttons and visuals on the screen
- `window.py` : just the tk window!

**other directories in protoplop/**
- `protoplop/resources/` : resources and things used (ex. test images, fonts)
- `protoplop/subsystems/` : subsystems, see above!
- `protoplop/updatelogs/` : where my silly silly fingers type strange update logs about what i did today (programming and not programming stuff included)

### Probably something important:

I use a lot of words and terms that probably don't mean what I think they mean. Some names may also not be very intuitive/even make sense. If there are any suggestions for better things to name stuff, I'll definitely be interested! 