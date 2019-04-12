#!/usr/bin/env python3
import sys
import time
import RPi.GPIO as gpio

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(2, gpio.OUT)
    gpio.setup(3, gpio.OUT)
    gpio.setup(4, gpio.OUT)
    gpio.setup(7, gpio.OUT)
    gpio.setup(14, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(10, gpio.OUT)
    gpio.setup(9, gpio.OUT)
    gpio.setup(25, gpio.OUT)
    gpio.setup(8, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(5, gpio.OUT)

    inputs = [21, 20, 26, 16, 19, 13, 12, 6]
    for i in inputs:
        #gpio.setup(i, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(i, gpio.IN)
    #gpio.setup(21, gpio.IN)
    #gpio.setup(20, gpio.IN)
    #gpio.setup(26, gpio.IN)
    #gpio.setup(16, gpio.IN)
    #gpio.setup(19, gpio.IN)
    #gpio.setup(13, gpio.IN)
    #gpio.setup(12, gpio.IN)
    #gpio.setup(6, gpio.IN)

def set_address(address):
    gpio.output(5, (address & (1 << 0)) > 0)
    gpio.output(3, (address & (1 << 1)) > 0)
    gpio.output(2, (address & (1 << 2)) > 0)
    gpio.output(4, (address & (1 << 3)) > 0)
    gpio.output(7, (address & (1 << 4)) > 0)
    gpio.output(14, (address & (1 << 5)) > 0)
    gpio.output(15, (address & (1 << 6)) > 0)
    gpio.output(18, (address & (1 << 7)) > 0)

    #gpio.output(9, (address & (1 << 8)) > 0)

    gpio.output(9, (address & (1 << 8)) > 0)
    gpio.output(10, (address & (1 << 9)) > 0)
    gpio.output(22, (address & (1 << 10)) > 0)
    gpio.output(23, (address & (1 << 11)) > 0)
    gpio.output(17, (address & (1 << 12)) > 0)
    gpio.output(25, (address & (1 << 13)) > 0)
    gpio.output(11, (address & (1 << 14)) > 0)

def read_data():
    data = 0
    data |= gpio.input(26) << 0
    data |= gpio.input(20) << 1
    data |= gpio.input(21) << 2
    data |= gpio.input(16) << 3
    data |= gpio.input(19) << 4
    data |= gpio.input(13) << 5
    data |= gpio.input(12) << 7
    data |= gpio.input(6) << 6
    return data

def select_chip(chip):
    if chip == 0:
        gpio.output(27, True)
        gpio.output(8, False)
        #gpio.output(8, True)
    elif chip == 1:
        gpio.output(27, False)
        gpio.output(8, True)
    #gpio.output(27, False)
    #gpio.output(8, True)

def set_chip_address(address):
    select_chip(address & 1)
    set_address(address >> 1)

def read_chip(address):
    set_address(0)
    time.sleep(0.0001)
    set_address(address)
    time.sleep(0.0001)
    return read_data()

def test_address(chip):
    select_chip(chip)
    print("Value = " + hex(read_chip(0x1)))
    for i in range(0, 15):
        value = read_chip(1 << i)
        print("At line " + str(i) + " = " + hex(value))

def read_rom(chip):
    select_chip(chip)
    for i in range(0, 0x8000):
        #read_chip(i)
        value = read_chip(i)
        #value = read_data()
        sys.stdout.buffer.write(bytes([value]))
        if i % 0x80 == 0:
            sys.stdout.flush()

def read_both():
    for i in range(0, 0x8000):
        select_chip(0)
        value = read_chip(i)
        sys.stdout.buffer.write(bytes([value]))
        select_chip(1)
        value = read_chip(i)
        sys.stdout.buffer.write(bytes([value]))
    sys.stdout.flush()

def read_rom_debug(chip):
    select_chip(chip)
    for i in range(0x400, 0x8000):
        value = read_chip(i)
        print(format(i, '#06x') + " = " + format(value, '#04x') + ", " + format(value, '#010b'))
        input("Press enter to read the next value")

try:
    init()
    
    chip = 0
    #test_address(chip)
    read_rom(chip)
    #read_rom_debug(chip)
    #read_both()

    #select_chip(1)
    #for address in range(0x0, 0xFFFF):
    #    set_chip_address(address)
    #for address in range(0x0, 0x8000):
    #    set_address(address)
    #    time.sleep(0.001)
    #    value = read_data()
    #    sys.stdout.write(chr(value))
        #print(hex(address) + " = " + hex(value))
finally:
    gpio.cleanup()
    sys.stdout.flush()
