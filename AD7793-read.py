import AD7793
import spidev
import time

spi = spidev.SpiDev()
ADC = AD7793.ADC7793(spi,0)

# Set Mode and Configuration of the ADC

MD  =[0x00, 0x0A]   #   16 bit Mode register [MSB[8], LSB[8]]   Page 15 of Datasheet 
                        #0x00 - Continuous reading  , 0x0A
                        #0x20 - Single conversion
                        #0x40 - Idle
                        #0x60 - Power down
                                          
CFW =[0x00, 0x80]   #   16 bit Configuration register [MSB[8], LSB[8]] Page 17 of Datasheet
                        # Example- channel selection [LSB]
                        
                        
                        
                        # 0x80 - (AIN1+) - (AIN1-)  Internal Reference without Buffer
                        # 0x90 - (AIN1+) - (AIN1-)  Internal Reference with Buffer
                        # 0x00 - (AIN1+) - (AIN1-)  External Reference without Buffer
                        # 0x10 - (AIN1+) - (AIN1-)  External Reference with Buffer
                        
                        
IO =[0x00]		    # 8 bit IO register to configure excitation currents to IO pins	
                                                
VREF = 1.17 # Internal V reference 1.17V, or external reference voltage                                              
GAIN = 1  

                                                                            
print("RESET",hex(ADC.RST(0)[0]))
print("ID",hex(ADC.ID(0)[0]))
print("STATUS",hex(ADC.STATUS(0)[0]))
print("MODE",hex(ADC.SET_MODE(MD)[0]))
print("CONFIG-R",hex(ADC.READ_CONFIG(0)[0]),hex(ADC.READ_CONFIG(0)[1]))
print("CONFIG-WRI",hex(ADC.WRITE_CONFIG(CFW)[0]))
print("CONFIG-R",hex(ADC.READ_CONFIG(0)[0]),hex(ADC.READ_CONFIG(0)[1]))
print("CONFIG-R",hex(ADC.WRITE_IO(IO)[0]))
print("CONFIG-R",hex(ADC.READ_IO(0)[0]))


while True:
        
    DATA = ADC.READ_DATA(0)
    
    print(hex(DATA[0]),hex(DATA[1]),hex(DATA[2]))
    
    V1= ((int((DATA[0]<<16)|(DATA[1]<<8)|(DATA[2]))) - (2**(24-1)))/(2**(24-1))* (VREF/GAIN)       # DATA =  2^(N-1) * (((AIN * GAIN)/VREF)+1)
																												  #  N = 24 bit,  Internal VREF= 1.17 V
    print ("Voltage", ADC.round_up(V1,4), "V")
    time.sleep(1)
