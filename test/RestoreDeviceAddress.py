from machine import Pin, I2C
from RadSensBoard import RadSensBoard

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

devices = i2c.scan()
if 0 == len(devices):
    print("I2C: No devices found")
else:
    print(f"I2C: {len(devices)} devices found")
    for device in devices:
        print()
        print(f"---> Hex: {hex(device)}, dec: {device}")

        geiger = RadSensBoard(i2c, device)
        if geiger.is_valid():
            print(f'Device I2C address:  0x{geiger.get_device_address():2X}')
            
            try:
                print(f'Setting device address to 0x{RadSensBoard.DEFAULT_DEVICE_ADDRESS:2x}')
                geiger.set_device_address(RadSensBoard.DEFAULT_DEVICE_ADDRESS)

                geiger = RadSensBoard(i2c)

                print(f'Device I2C address:  0x{geiger.get_device_address():2X}')
                assert geiger.get_device_address() == RadSensBoard.DEFAULT_DEVICE_ADDRESS
            except OSError as ex:
                print(ex)
        else:
            print("Not a RadSense device")
