from machine import Pin, I2C
from RadSensBoard import RadSensBoard
import DebugHelpers

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

DebugHelpers.scan_i2c(i2c)
print()

print(f"RadSensBoard library version '{RadSensBoard.VERSION}'")
print()

geiger = RadSensBoard(i2c)

DebugHelpers.dump_registers(geiger)
print()

DebugHelpers.dump_device_information(geiger)
