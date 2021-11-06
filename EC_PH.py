# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:27:05 2021

@author: pcochang
"""

import time
import sys
import RPi.GPIO as GPIO 
import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

sys.path.insert(0,'Aquaponics/DFRobot_ADS1115/RaspberryPi/Python/')
from DFRobot_ADS1115 import ADS1115


ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3

def GPIO_init():
    EC_PWR = 16
    PH_PWR = 18
    GPIO.setup (EC_PWR, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup (PH_PWR, GPIO.OUT, initial=GPIO.LOW)
    
def readEC(voltage, temperature = 25):
    _kvalue = 1.0
    _kvalueLow = 1.0
    _kvalueHigh = 1.02
    rawEC = 1000*voltage/820.0/200.0
    #print(">>>current rawEC is: %.3f" % rawEC)
    valueTemp = rawEC * _kvalue
    if(valueTemp > 2.5):
        _kvalue = _kvalueHigh
    elif(valueTemp < 2.0):
        _kvalue = _kvalueLow
    value = rawEC * _kvalue
    value = value / (1.0+0.0185*(temperature-25.0))
    return value


 def readPH(voltage):
    # pH 4.0
    _acidVoltage = 2032.44
    # pH 7.0
    _neutralVoltage = 1500.0
    slope = (7.0-4.0)/((_neutralVoltage-1500.0) /
                       3.0 - (_acidVoltage-1500.0)/3.0)
    intercept = 7.0 - slope*(_neutralVoltage-1500.0)/3.0
    _phValue = slope*(voltage-1500.0)/3.0+intercept
    return round(_phValue, 2)


def read_ph_ec():
	global ads1115
	temperature = 25 # or make your own temperature read process
	#Set the IIC address
	ads1115.setAddr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
	#Get the Digital Value of Analog of selected channel
	adc0 = ads1115.readVoltage(0)
	adc1 = ads1115.readVoltage(1)
	#Convert voltage to EC with temperature compensation
    GPIO.output(16,1 )
    time.sleep(0.1)
	EC = readEC(adc0['r'],temperature)
    GPIO.output(16,0 )
    GPIO.output(18,1 )
    time.sleep(0.1)
	PH = readPH(adc1['r'])
    GPIO.output(18,0 )
	print("Temperature:%.1f ^C EC:%.2f ms/cm PH:%.2f " %(temperature,EC,PH))
	return temperature, EC, PH


ads1115 = ADS1115()
GPIO_init():
input("Connect EC sensor Vdd pin to pin 16 of raspberry pi. GND pin to any ground of raspi. Press Enter to continue")
print("")
input("Connect PH sensor Vdd pin to pin 18 of raspberry pi. GND pin to any ground of raspi. Press Enter to continue")
if __name__ == "__main__":
    while True:
        read_ph_ec()
        time.sleep(1)