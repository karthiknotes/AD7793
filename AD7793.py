from time import sleep
import math
import spidev

STATUS_REG = [0x40]
CONFIG_WRITE_REG = [0x10]
CONFIG_READ_REG = [0x50]
ID_REG = [0x60]
MODE_WRITE_REG = [0x08]
ADC_READ_REG =[0x58]
IO_READ_REG = [0x68]
IO_WRITE_REG = [0x28]
RESET = [0xFF, 0XFF, 0XFF, 0XFF]


class ADC7793():
    
    def __init__(self,spi,spi_channel):
        self.spi = spi
        spi.open(spi_channel,0)
        spi.max_speed_hz = 1000000
        spi.mode = 0b11
        spi.bits_per_word = 8

    def RST(self,RS):
        self.spi.writebytes(RESET)
        RS = self.spi.readbytes(1)
        return RS
      
    def ID(self,ID2):
        self.spi.writebytes(ID_REG) 
        ID2 = self.spi.readbytes(1)
        return ID2

    def STATUS(self,ST):
        self.spi.writebytes(STATUS_REG)
        ST = self.spi.readbytes(2)
        return ST

    def SET_MODE(self,MD):
        self.spi.writebytes(MODE_WRITE_REG)
        self.spi.writebytes([MD[0]]) 
                             
        self.spi.writebytes([MD[1]]) 
        MD = self.spi.readbytes(2)
        return MD
        
    def READ_CONFIG(self,CFR):
        self.spi.writebytes(CONFIG_READ_REG)
        CFR = self.spi.readbytes(2)
        return CFR

    def WRITE_CONFIG(self,CFW):
        self.spi.writebytes(CONFIG_WRITE_REG)
        self.spi.writebytes([CFW[0]])
        self.spi.writebytes([CFW[1]]) 
        CFW = self.spi.readbytes(2)
        return CFW
        
    def READ_IO(self,CFR):
        self.spi.writebytes(IO_READ_REG)
        CFR = self.spi.readbytes(1)
        return CFR

    def WRITE_IO(self,IO):
        self.spi.writebytes(IO_WRITE_REG)
        self.spi.writebytes([IO[0]])
        CFW = self.spi.readbytes(1)
        return CFW
        
    def READ_DATA(self,V):   
        self.spi.writebytes(ADC_READ_REG)
        value = self.spi.readbytes(3)
        return value

    def round_up(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

