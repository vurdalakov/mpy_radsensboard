from machine import Pin, I2C
import DebugHelpers

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

DebugHelpers.scan_i2c(i2c)
