## Force Sensitive Resistor Array

from machine import Pin
from machine import ADC
import time

# pin selection based on : https://docs.micropython.org/en/latest/esp32/quickref.html#pins-and-gpio

#   0   
#   1   TX
#   2   LED
#   3   RX
#   4   
#   5   BOOT
#   6   FLASH
#   7   FLASH
#   8   FLASH
#   9   
#   10  
#   11  FLASH
#   12  BOOT
#   13  Column 0
#   14  
#   15  BOOT
#   17  FLASH
#   18  Column 1
#   19  I2C (0)
#   21  Column 2
#   22  Column 3
#   23  Column 4
#   25  Row 1
#   26  Row 2
#   27  Row 3
#   32  Row 4
#   33  ADC-Column 0
#   34  ADC-Column 1
#   35  ADC-Column 2
#   36  ADC-Column 3
#   39  ADC-Column 4




col0=Pin(13,Pin.OUT, value=0)
col1=Pin(18,Pin.OUT, value=0)
col2=Pin(21,Pin.OUT, value=0)
col3=Pin(22,Pin.OUT, value=0)
col4=Pin(23,Pin.OUT, value=0)

column_gpio=[col0,col1,col2,col3,col4]


row1=Pin(25,Pin.IN)
row2=Pin(26,Pin.IN)
row3=Pin(27,Pin.IN)
row4=Pin(32,Pin.IN)

row_gpio=[row1,row2,row3,row4]


adc_col0=ADC(Pin(33))
adc_col0.atten(ADC.ATTN_11DB)

adc_col1=ADC(Pin(34))
adc_col1.atten(ADC.ATTN_11DB)


adc_col2=ADC(Pin(35))
adc_col2.atten(ADC.ATTN_11DB)

adc_col3=ADC(Pin(36))
adc_col3.atten(ADC.ATTN_11DB)

adc_col4=ADC(Pin(39))
adc_col4.atten(ADC.ATTN_11DB)

column_adc=[adc_col0,adc_col1,adc_col2,adc_col3,adc_col4]

# array for storing values
matrix_values=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
#calibration_values=[[2000,800,1900],[2000,1000,1400],[1000,1200,1300]]



def read_matrix_element(row,col):
    # note, zero based numbering is used for rows and columns
    if row not in (1,2,3,4):
        return None
    
    if col not in (0,1,2,3,4):
        return None
    
    
    #set the row to be read as an output low, set all others as inputs (high impedance)
    for matrix_row in (1,2,3,4):
        if matrix_row == row:
            row_gpio[matrix_row-1].init(mode=Pin.OUT,pull=None,value=0)
        else:
            row_gpio[matrix_row-1].init(mode=Pin.IN, pull=None)
    
    #set the column to be read as an output high, set all others to output low
    for matrix_col in (0,1,2,3,4):
        if matrix_col == col:
            column_gpio[matrix_col].on()
        else:
            column_gpio[matrix_col].off()
            
    # read the ADC for the desired column
    return column_adc[col].read()

            
# read each matrix element and print output
while(True):
    data=""
    # get the values
    for row in (1,2,3,4):
        for col in (0,1,2,3,4):
            result=read_matrix_element(row,col)
            #result=result/calibration_values[row][col]
            matrix_values[row-1][col]=result
            if result >620:
                print ("You have bad posture")
                print ("To fix your posture by sitting strait")
                print ("Maybe do some stretches")
            elif result >1000:
                print ("You have really bad posture")
                print ("To fix your posture by sitting strait")
                print ("Maybe do some stretches")
            elif result >3000:
                print ("WOW! To fix your posture! sit strait")
                print ("Maybe do some stretches")
            elif col==4 and row==4:
                data=data+str(result)
            else:
                data=data+str(result)+","
           # if col==4 and row==4:
           #     data=data+str(result)
           # else:
           #     data=data+str(result)+","
    # print the values
    
    
    print(data)
    
    #delay 1 second
    time.sleep(1)
                
            
            
            
            





