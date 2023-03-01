from grove_rgb_lcd import *

prev_threshold = 0
current_threshold = -1
nl = '\n'
setRGB(0,128,64)

while True:
    if current_threshold != prev_threshold:
        current_threshold = prev_threshold
        setText(f"{nl}{current_threshold:3}cm")
    
