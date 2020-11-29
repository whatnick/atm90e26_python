import spidev
from atm90e26_registers import *

import time
import struct
import binascii
__write__ = False
__read__ = True
class ATM90E26_SPI:

    '''       
    spi - hardware or software SPI implementation
    cs - Chip Select pin
    '''

    def __init__(self, spi):
        self.spi = spi
        self.init_config()
    '''
    rw - True - read, False - write
    address - register to operate
    val - value to write (if any)
    '''

    def comm_atm90(self, RW, address, val):
        # switch MSB and LSB of value
        read_buf = bytearray(1)
        write_buf = bytearray(3)
        # Set read write flag
        address |= RW << 7

        if(RW): # 1 as MSB marks a read
            struct.pack_into('>B',read_buf,0,address)
            ''' Must wait 4 us for data to become valid '''
            time.sleep(10e-6)
            # Write address
            read_res = self.spi.xfer3(read_buf,2)
            return read_res
        else: #0 as MSB and 32 clock cycles marks a write
            struct.pack_into('>B',write_buf,0,address)
            struct.pack_into('>H',write_buf,2,val)
            self.spi.xfer(write_buf)# write all the bytes
    
    def init_config(self):
        pass
    
    def get_rms_voltages(self):
        VA = 0
        VB = 0
        VC = 0

        return (VA,VB,VC)

    def get_meter_status(self):
        s1 = 0
        s2 = 0

        return (s1,s2)


if __name__=="__main__":
    spi = spidev.SpiDev()
    spi.open(0, 1)

    spi.mode = 0b11
    spi.max_speed_hz = 200000

    eic1 = ATM90E26_SPI(spi)
    for i in range(10):
        print("Meter Status:",eic1.get_meter_status())
        print("Voltages:",eic1.get_rms_voltages())