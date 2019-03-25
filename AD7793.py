# DSL 

import spidev
import time
import math
from enum import Enum


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 0b11
spi.bits_per_word = 8


# AD7793 Register values
STATUS_REG = [0x40]
CONFIG_WRITE_REG = [0x10]
CONFIG_READ_REG = [0x50]
ID_REG = [0x60]
MODE_WRITE_REG = [0x08]
ADC_READ_REG =[0x58]
RESET = [0xFF, 0XFF, 0XFF, 0XFF]


def ADC_RST(RS):
	spi.writebytes(RESET)
	RS = spi.readbytes(1)
	return RS
  
def ADC_ID(ID2):
	spi.writebytes(ID_REG) 
	ID2 = spi.readbytes(1)
	return ID2

def ADC_STAT(ST):
	spi.writebytes(STATUS_REG)
	ST = spi.readbytes(2)
	return ST

def SET_MODE(MD):
	spi.writebytes(MODE_WRITE_REG)
	spi.writebytes([0x00]) #0x00 - Continuous reading 
						 #0x20 - Single conversion
						 #0x40 - Idle
						 #0x60 - Power down
						 
	spi.writebytes([0x0A]) #0x0A 16.7Hz 120mS -65dB for 50/60Hz filter
	MD = spi.readbytes(2)
	return MD
	
def READ_CONFIG(CFR):
	spi.writebytes(CONFIG_READ_REG)
	CFR = spi.readbytes(2)
	return CFR

def WRITE_CONFIG(CFW):
	spi.writebytes(CONFIG_WRITE_REG)
	spi.writebytes([0x00]) #0x00 - (AIN1+) - (AIN1-)
						   #0x01 - (AIN2+) - (AIN2-)
						   #0x02 - (AIN3+) - (AIN3-)
						   #0x40 - Idle
						   #0x60 - Power down
						     #ADC_CH(CS, CH)
	spi.writebytes([0x90])
	CFW = spi.readbytes(2)
	return CFW
	
def ADC_READ(C):	
    spi.writebytes(ADC_READ_REG)
    value = spi.readbytes(3)
    return value

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


print("RESET",hex(ADC_RST(0)[0]))
print("ID",hex(ADC_ID(0)[0]))
print("STATUS",hex(ADC_STAT(0)[0]))
print("MODE",hex(SET_MODE(0)[0]))
print("CONFIG-R",hex(READ_CONFIG(0)[0]),hex(READ_CONFIG(0)[1]))
print("CONFIG-WRI",hex(WRITE_CONFIG(0)[0]))
print("CONFIG-R",hex(READ_CONFIG(0)[0]),hex(READ_CONFIG(0)[1]))

while True:
	
	#print("CONFIG-WRI",hex(WRITE_CONFIG(0)[0]),hex(WRITE_CONFIG(0)[1]))
	DATA = ADC_READ(0)
	#print (hex(ADC_ID(0)[0]), hex(ADC_STAT(0)[0]), hex(DATA[0]), hex(DATA[1]), hex(DATA[2]))
	V1= ((int((DATA[0]<<16)|(DATA[1]<<8)|(DATA[2]))) - 8388608)/8388608*1.19
	print ("Voltage-", round_up(V1,4), "V")
	time.sleep(1)
spi.close()

