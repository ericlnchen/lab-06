import time
import grovepi
import sys
import math
import struct
import numpy
import di_i2c

def set_bus(bus):
	global i2c
	i2c = di_i2c.DI_I2C(bus = bus, address = address)

address = 0x04
max_recv_size = 10
set_bus("RPI_1SW")

# This allows us to be more specific about which commands contain unused bytes
unused = 0
retries = 10
additional_waiting = 0

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

# analogRead() command format header
aRead_cmd = [3]
# Ultrasonic read
uRead_cmd = [7]
# No data is available from the GrovePi
data_not_available_cmd = [23]

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

def write_i2c_block(block, custom_timing = None):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	counter = 0
	reg = block[0]
	data = block[1:]
	while counter < 3:
		try:
			i2c.write_reg_list(reg, data)
			time.sleep(0.002 + additional_waiting)
			return
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			continue
                
# Read I2C block from the GrovePi
def read_i2c_block(no_bytes = max_recv_size):
	'''
	Now catches and raises Keyboard Interrupt that the user is responsible to catch.
	'''
	data = data_not_available_cmd
	counter = 0
	while data[0] in [data_not_available_cmd[0], 255] and counter < 3:
		try:
			data = i2c.read_list(reg = None, len = no_bytes)
			time.sleep(0.002 + additional_waiting)
			if counter > 0:
				counter = 0
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		except:
			counter += 1
			time.sleep(0.003)
			
	return data
                
def read_identified_i2c_block(read_command_id, no_bytes):
	data = [-1]
	while len(data) <= 1:
		data = read_i2c_block(no_bytes + 1)

	return data[1:]

# Read analog value from Pin
def analogRead(pin):
	write_i2c_block(aRead_cmd + [pin, unused, unused])
	number = read_identified_i2c_block(aRead_cmd, no_bytes = 2)
	return number[0] * 256 + number[1]

def ultrasonicRead(pin):
	write_i2c_block(uRead_cmd + [pin, unused, unused])
	number = read_identified_i2c_block(uRead_cmd, no_bytes = 2)
	return (number[0] * 256 + number[1])

def main():

    threshold = grovepi.analogRead(potentiometer)
    prev_threshold = 0
    nl = '\n'
    setRGB(0,128,64)


    while True:

        # get the distance between object and ultrasonic range sensor
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        # update the threshold only if the user used the potentiometer
        # we give a buffer of 5 so that the screen doesn't always refresh like crazy
        if threshold - prev_threshold > 2 or threshold - prev_threshold < -2:
            prev_threshold = threshold
        
        # get the value of the potentiometer
        threshold = grovepi.analogRead(potentiometer) # constantly check and update the threshold

        # doesn't always refresh the whole screen
        # formats and writes to the display according to the write up
        if distance < threshold:
            if threshold < 1000:
                setText_norefresh(f"{threshold:3}cm OBJ PRES {nl}{distance:3}cm")
            else:
                setText_norefresh(f"{threshold:3}cm OBJ PRES{nl}{distance:3}cm")
        else:
            setText_norefresh(f"{threshold:3}cm           {nl}{distance:3}cm")

        
    

if __name__ == "__main__":
    main()
    
    
