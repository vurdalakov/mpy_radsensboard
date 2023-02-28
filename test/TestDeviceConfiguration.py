from machine import Pin, I2C
from RadSensBoard import RadSensBoard
import DebugHelpers

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

DebugHelpers.scan_i2c(i2c)
print()

geiger = RadSensBoard(i2c)

DebugHelpers.dump_device_information(geiger)
print()

assert geiger.get_device_id() == RadSensBoard.DEFAULT_DEVICE_ID
assert geiger.get_firmware_version() == 2
assert geiger.get_device_address() == RadSensBoard.DEFAULT_DEVICE_ADDRESS

def set_and_verify_calibration_value(expected_value):
    geiger.set_calibration_value(expected_value)
    actual_value = geiger.get_calibration_value()
    print(f'Calibration value:    {actual_value}')
    assert actual_value == expected_value

set_and_verify_calibration_value(106)
set_and_verify_calibration_value(106 + 512)
set_and_verify_calibration_value(RadSensBoard.DEFAULT_CALIBRATION_VALUE)

print()

def set_and_verify_high_voltage_generator_state(expected_value):
    geiger.set_high_voltage_generator_state(expected_value)
    actual_value = geiger.get_high_voltage_generator_state()
    print(f'HW generator state:   {actual_value}')
    assert actual_value == expected_value

set_and_verify_high_voltage_generator_state(1)
set_and_verify_high_voltage_generator_state(0)
set_and_verify_high_voltage_generator_state(1)

print()

def set_and_verify_led_indication_state(expected_value):
    geiger.set_led_indication_state(expected_value)
    actual_value = geiger.get_led_indication_state()
    print(f'LED indication state: {actual_value}')
    assert actual_value == expected_value

set_and_verify_led_indication_state(1)
set_and_verify_led_indication_state(0)
set_and_verify_led_indication_state(1)

print()
