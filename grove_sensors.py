from grove_rgb_lcd import *

import time
import grovepi

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

grovepi.pinMode(potentiometer,"INPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

def main():

    threshold = grovepi.analogRead(potentiometer)
    supersonice_range = 999
    prev_threshold = 0
    nl = '\n'
    setRGB(0,128,64)


    while True:
        
        # update the threshold only if the user used the potentiometer
        # we give a buffer of 5 so that the screen doesn't always refresh like crazy
        if threshold - prev_threshold > 5 or threshold - prev_threshold < -5:
            prev_threshold = threshold
            if supersonice_range > threshold:
                setText_norefresh(f"OBJ PRES{nl}{threshold:3}cm")
            else:
                setText_norefresh(f"        {nl}{threshold:3}cm")
            

        threshold = grovepi.analogRead(potentiometer) # constantly check and update the threshold

        
    

if __name__ == "__main__":
    main()
    
    
