from grove_rgb_lcd import *

import time
import grovepi

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

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
    prev_threshold = 0
    nl = '\n'
    setRGB(0,128,64)


    while True:
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)
        # update the threshold only if the user used the potentiometer
        # we give a buffer of 5 so that the screen doesn't always refresh like crazy
        if threshold - prev_threshold > 2 or threshold - prev_threshold < -2:
            prev_threshold = threshold
            
        threshold = grovepi.analogRead(potentiometer) # constantly check and update the threshold

        if distance < threshold:
            setText_norefresh(f"{threshold:3}cm OBJ PRES{nl}{distance:3}cm")
        else:
            setText_norefresh(f"{threshold:3}cm         {nl}{distance:3}cm")

        
    

if __name__ == "__main__":
    main()
    
    
