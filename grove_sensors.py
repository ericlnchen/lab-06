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
    prev_threshold = 0
    current_threshold = -1
    nl = '\n'
    setRGB(0,128,64)

    while True:
        sensor_value = grovepi.analogRead(potentiometer)
        prev_threshold = sensor_value
        if current_threshold != prev_threshold:
            current_threshold = prev_threshold
            setText(f"{nl}{current_threshold:3}cm")
    

if __name__ == "__main__":
    main()
    
    
