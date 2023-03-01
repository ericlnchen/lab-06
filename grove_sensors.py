from grove_rgb_lcd import *

import time
import grovepi

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

# Connect the LED to digital port D5
# SIG,NC,VCC,GND
led = 5

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
    prev_threshold = 0
    nl = '\n'
    setRGB(0,128,64)

    while True:
        
        # update the threshold only if the user used the potentiometer
        if threshold - prev_threshold > 5 or threshold - prev_threshold < -5:
            prev_threshold = threshold
            setText(f"{nl}{threshold:3}cm")

        threshold = grovepi.analogRead(potentiometer) # constantly check and update the threshold
    

if __name__ == "__main__":
    main()
    
    
