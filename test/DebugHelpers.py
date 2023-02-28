from RadSensBoard import RadSensBoard

def scan_i2c(i2c):
    device_addresses = i2c.scan()
    if 0 == len(device_addresses):
        print("No I2C devices found")
    else:
        print(f"I2C devices found: {len(device_addresses)}")
        for device_address in device_addresses:
            geiger = RadSensBoard(i2c, device_address)
            is_radsens = " - RadSens!" if geiger.is_valid() else ""
            print(f"    Hex: 0x{device_address:02X}, dec: {device_address:3d} {is_radsens}")

def dump_registers(geiger):
    print('Device registers')
    registers = geiger.read_registers(24)
    print(f"    0x00: 0x{registers[0x00]:02X}", f"0x{registers[0x01]:02X} \t\t# __REG_DEVICE_ID, __REG_FIRMWARE_VERSION")
    print(f"    0x02: 0x{registers[0x02]:02X}")
    print(f"    0x03: 0x{registers[0x03]:02X}", f"0x{registers[0x04]:02X}", f"0x{registers[0x05]:02X} \t# __REG_RADATION_LEVEL_DYNAMIC")
    print(f"    0x06: 0x{registers[0x06]:02X}", f"0x{registers[0x07]:02X}", f"0x{registers[0x08]:02X} \t# __REG_RADATION_LEVEL_STATIC")
    print(f"    0x09: 0x{registers[0x09]:02X}", f"0x{registers[0x0A]:02X} \t\t# __REG__PULSE_COUNT")
    print(f"    0x0B: 0x{registers[0x0B]:02X}", f"0x{registers[0x0C]:02X}", f"0x{registers[0x0D]:02X}", f"0x{registers[0x0E]:02X}", f"0x{registers[0x0F]:02X}")
    print(f"    0x10: 0x{registers[0x10]:02X}", f"0x{registers[0x11]:02X} \t\t# __REG_DEVICE_ADDRESS, __REG_HV_GENERATOR_STATE")
    print(f"    0x12: 0x{registers[0x12]:02X}", f"0x{registers[0x13]:02X} \t\t# __REG_CALIBRATION_VALUE")
    print(f"    0x14: 0x{registers[0x14]:02X} \t\t\t# __REG_LED_INDICATION_STATE")
    print(f"    0x15: 0x{registers[0x15]:02X}", f"0x{registers[0x16]:02X}", f"0x{registers[0x17]:02X}")

def dump_device_information(geiger):
    print('Device information')
    print(f'    Device ID:            0x{geiger.get_device_id():02X}')
    print(f'    Firmware version:     {geiger.get_firmware_version()}')
    print(f'    Device I2C address:   0x{geiger.get_device_address():02X}')
    print(f'    Calibration value:    {geiger.get_calibration_value()}')
    print(f'    HV generator state:   {geiger.get_high_voltage_generator_state()}')
    print(f'    LED indication state: {geiger.get_led_indication_state()}')

def dump_radiation_data(geiger):
    radiation_data = geiger.get_radiation_data()
    print('Radiation data')
    print(f'    Dynamic window: {radiation_data[0]:.3f} uSv/h')
    print(f'    Fixed window:   {radiation_data[1]:.3f} uSv/h')
    print(f'    Pulse count:    {radiation_data[2]}')
