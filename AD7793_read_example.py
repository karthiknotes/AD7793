import AD7793
import spidev
import time

spi = spidev.SpiDev()
ADC = AD7793.ADC7793(spi,0)

# Set Mode register of the ADC ( See page 15 of datasheet for options)

MD  =[0x00, 0x0A]   #   16 bit Mode register [MSB[8], LSB[8]]   Page 15 of Datasheet 
                        #MSB
			#0x00 - Continuous reading
                        #0x20 - Single conversion
                        #0x40 - Idle
                        #0x60 - Power down
			
			#LSB
			
			#0x0A - Internal 64Hz clock selected with default filter update rate
			
			
# Set Configuration register of the ADC ( see page 17 of datasheet for options)
                                          
CFW =[0x00, 0x80]   #   16 bit Configuration register [MSB[8], LSB[8]] 

			# Parameters to set - Bias voltage, 
			#		    - Unipolar/Bipolar modes
			#		    - Gain (1x to 128x)
			#                   - Reference source (Internal or external?)
			#                   - ADC channel selection
			
			# [MSB]
			# 0x00 - Bias voltage generator disabled, Bipolar output coding, Gain -1x
			
                        # [LSB] channel selection + reference selector
                                       
                        # 0x80 - (AIN1+) - (AIN1-)  Internal Reference without Buffer
                        # 0x90 - (AIN1+) - (AIN1-)  Internal Reference with Buffer
                        # 0x00 - (AIN1+) - (AIN1-)  External Reference without Buffer
                        # 0x10 - (AIN1+) - (AIN1-)  External Reference with Buffer
VREF = 1.17 # Internal V reference 1.17V, or external reference voltage                                              
GAIN = 1  # Change this according to the gain set in the register
			
# Set IO register of the ADC ( see page 18 of datasheet for options)

IO =[0x00]		# 8 bit IO register to configure excitation currents to IO pins	
                                                


# Reset the ADC                                                                            
print("RESET",hex(ADC.RST(0)[0]))
# Get the ADC ID and model number
print("ID",hex(ADC.ID(0)[0]))
# See if the ADC is ready
print("STATUS",hex(ADC.STATUS(0)[0]))

# Set the mode register
print("MODE",hex(ADC.SET_MODE(MD)[0]))

# Set the Configuration register
print("CONFIG-WRI",hex(ADC.WRITE_CONFIG(CFW)[0]))
# Read the configuration register to verify 
print("CONFIG-R",hex(ADC.READ_CONFIG(0)[0]),hex(ADC.READ_CONFIG(0)[1]))

# Set IO register
print("CONFIG-R",hex(ADC.WRITE_IO(IO)[0]))
# Read the IOP register to verify
print("CONFIG-R",hex(ADC.READ_IO(0)[0]))


# Continouosly read the voltage
while True:
        
    DATA = ADC.READ_DATA(0)
    
    # Print the raw 24 bit hex data		
    print(hex(DATA[0]),hex(DATA[1]),hex(DATA[2]))
    
    # Convert the raw data to volatage using the formula 
    # DATA =  2^(N-1) * (((V1 * GAIN)/VREF)+1)
    #  N = 24 bit, V1 = is the analog input voltage, For our case - Internal VREF= 1.17 V and  Gain = 1
    # (See page 24 of datasheet under 'Data Output Coding')

    V1= ((int((DATA[0]<<16)|(DATA[1]<<8)|(DATA[2]))) - (2**(24-1)))/(2**(24-1))* (VREF/GAIN)      

    print ("Voltage", ADC.round_up(V1,4), "V") # rounding up the voltage to 4 decimal points
    time.sleep(1)
