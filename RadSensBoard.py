# A MicroPython library for Raspberry Pi Pico that works with RadSens Geiger counter board
# MIT license
# Copyright (c) 2022 Vurdalakov
# https://github.com/vurdalakov/mpy_radsensboard

from micropython import const

class RadSensBoard():
    
    VERSION = const("1.0")
    
    DEFAULT_DEVICE_ID = const(0x7D)

    DEFAULT_DEVICE_ADDRESS = const(0x66)
    
    DEFAULT_CALIBRATION_VALUE = const(105)

    # private constants

    __REG_DEVICE_ID = const(0x00)
    __REG_FIRMWARE_VERSION = const(0x01)
    __REG_RADATION_LEVEL_DYNAMIC = const(0x03)
    __REG_RADATION_LEVEL_FIXED = const(0x06)
    __REG_PULSE_COUNT = const(0x09)
    __REG_DEVICE_ADDRESS = const(0x10)
    __REG_HV_GENERATOR_STATE = const(0x11)
    __REG_CALIBRATION_VALUE = const(0x12)
    __REG_LED_INDICATION_STATE = const(0x14)
    
    # constructor

    def __init__(self, i2c, i2c_address = DEFAULT_DEVICE_ADDRESS):
        self.__i2c = i2c
        self.__i2c_address = i2c_address
        
        self.__registers = bytearray(21)
        self.__write_buffer = bytearray(1)

        self.__pulse_count = 0
        
        self.__read_registers()

        self.reset_pulse_count()
        
    def is_valid(self):
        return self.get_device_id() == RadSensBoard.DEFAULT_DEVICE_ID

    # radiation data

    def get_radiation_data(self):
        self.__read_registers()
        
        level_dynamic = self.__get_register24_big_endian(__REG_RADATION_LEVEL_DYNAMIC) / 1000
        level_fixed = self.__get_register24_big_endian(__REG_RADATION_LEVEL_FIXED) / 1000
        
        # self.__pulse_count is calculated in __read_registers()

        return (level_dynamic, level_fixed, self.__pulse_count)
        
    def get_radiation_level_dynamic(self):
        radiation_data = self.get_radiation_data()
        return radiation_data[0]
        
    def get_radiation_level_fixed(self):
        radiation_data = self.get_radiation_data()
        return radiation_data[1]
        
    def get_pulse_count(self):
        radiation_data = self.get_radiation_data()
        return radiation_data[2]

    def reset_pulse_count(self):
        self.__pulse_count = 0
        
    # device configuration
        
    def get_device_id(self):
        return self.__read_register8(__REG_DEVICE_ID)
        
    def get_firmware_version(self):
        return self.__read_register8(__REG_FIRMWARE_VERSION)
        
    def get_device_address(self):
        return self.__read_register8(__REG_DEVICE_ADDRESS)
        
    def set_device_address(self, board_address):
        self.__write_register8(__REG_DEVICE_ADDRESS, board_address)
    
    def get_high_voltage_generator_state(self):
        return self.__read_register8(__REG_HV_GENERATOR_STATE)
        
    def set_high_voltage_generator_state(self, state):
        self.__write_register8(__REG_HV_GENERATOR_STATE, state)
    
    def get_calibration_value(self):
        return self.__read_register16(__REG_CALIBRATION_VALUE)

    def set_calibration_value(self, value):
        self.__write_register16(__REG_CALIBRATION_VALUE, value)
    
    def get_led_indication_state(self):
        return self.__read_register8(__REG_LED_INDICATION_STATE)
        
    def set_led_indication_state(self, state):
        self.__write_register8(__REG_LED_INDICATION_STATE, state)
        
    # debug
    
    def read_registers(self, count):
        buffer = bytearray(count)
        self.__i2c.readfrom_into(self.__i2c_address, buffer)
        return buffer
        
    # private methods
    
    def __read_registers(self):
        self.__i2c.readfrom_into(self.__i2c_address, self.__registers)

        # board pulse counter is reset every time I2C read operation is performed,
        # so we need to accumulate pulse count in a class variable
        pulse_count = self.__get_register16_big_endian(__REG_PULSE_COUNT)
        self.__pulse_count += pulse_count

    def __read_register8(self, address):
        self.__read_registers()
        return self.__registers[address]

    def __read_register16(self, address):
        self.__read_registers()
        return self.__registers[address] | (self.__registers[address + 1] << 8)
    
    def __get_register16_big_endian(self, address):
        return (self.__registers[address] << 8) | self.__registers[address + 1]
    
    def __get_register24_big_endian(self, address):
        return (self.__registers[address] << 16) | (self.__registers[address + 1] << 8) | self.__registers[address + 2]
    
    def __write_register8(self, address, value):
        self.__write_buffer[0] = value & 0xFF
        self.__i2c.writeto_mem(self.__i2c_address, address, self.__write_buffer)

    def __write_register16(self, address, value):
        self.__write_register8(address, value)
        self.__write_register8(address + 1, value >> 8)
