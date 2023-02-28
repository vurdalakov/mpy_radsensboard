from time import sleep
from machine import Pin, I2C
from RadSensBoard import RadSensBoard
import DebugHelpers

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

DebugHelpers.scan_i2c(i2c)
print()

geiger = RadSensBoard(i2c)

DebugHelpers.dump_device_information(geiger)
print()

DebugHelpers.dump_radiation_data(geiger)
print()

for i in range(0, 20):
    geiger.get_firmware_version()
    DebugHelpers.dump_radiation_data(geiger)
    print('Radiation data (alt)')
    print(f'    Dynamic window: {geiger.get_radiation_level_dynamic():.3f} uSv/h')
    print(f'    Fixed window:   {geiger.get_radiation_level_fixed():.3f} uSv/h')
    print(f'    Pulse count:    {geiger.get_pulse_count()}')
    print()
    sleep(1)

print('Reset pulse count')
print()

geiger.reset_pulse_count()
DebugHelpers.dump_radiation_data(geiger)
