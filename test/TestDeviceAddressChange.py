from machine import Pin, I2C
from RadSensBoard import RadSensBoard
import DebugHelpers

ALTERNATIVE_DEVICE_ADDRESS = 0x54

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Start device with default device address and change it to alternative device address

DebugHelpers.scan_i2c(i2c)
print()

def verify_device_adrress(expected_value):
    actual_value = geiger.get_device_address()
    print(f'Device I2C address:  0x{actual_value:2x}')
    assert actual_value == expected_value
    print()

geiger = RadSensBoard(i2c)

verify_device_adrress(RadSensBoard.DEFAULT_DEVICE_ADDRESS)

print(f'--> Setting device address to 0x{ALTERNATIVE_DEVICE_ADDRESS:2x}')
print()

geiger.set_device_address(ALTERNATIVE_DEVICE_ADDRESS)

# Start device with alternative device address and change it back to default device address

DebugHelpers.scan_i2c(i2c)
print()

geiger = RadSensBoard(i2c, ALTERNATIVE_DEVICE_ADDRESS)

verify_device_adrress(ALTERNATIVE_DEVICE_ADDRESS)

print(f'--> Setting device address to 0x{RadSensBoard.DEFAULT_DEVICE_ADDRESS:2x}')
print()

geiger.set_device_address(RadSensBoard.DEFAULT_DEVICE_ADDRESS)

# Start device with default device address

DebugHelpers.scan_i2c(i2c)
print()

geiger = RadSensBoard(i2c)

verify_device_adrress(RadSensBoard.DEFAULT_DEVICE_ADDRESS)
