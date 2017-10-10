""" Simple bitreader class and some utility functions.
Inspired by http://multimedia.cx/eggs/python-bit-classes
"""

import sys

class BitReadError(ValueError):
    pass

class BitReader(object):
    """Read bits from bytestring buffer into unsigned integers."""

    def __init__(self, buffer):
        self.buffer = buffer
        # Set the pos of bit
        self.bit_pos = 7
        # get the first bytestring to interger value
        self.byte = ord(self.buffer[0])
        self.index = 1

    def get_bits(self, num_bits):
        """Read num_bits from the buffer."""

        num = 0
        # create a mask to filter per bit for per position
        # firstly get the highest bit in  byte
        mask = 1 << self.bit_pos
        if self.byte is None:
            return None

        while num_bits:
            num_bits -=1
            num <<= 1

            if self.byte & mask:
                num |= 1
            mask >>= 1
            self.bit_pos -= 1

            if self.bit_pos < 0:
                if self.byte is None:
                    raise  BitReadError("Beyond buffer doundary")
                self.bit_pos = 7
                mask =1 << self.bit_pos
                if self.index < len(self.buffer):
                    self.byte = ord(self.buffer[self.index])
                else:
                    self.byte = None

                self.index += 1
        return  num

if __name__ == '__main__':
    buffer = sys.argv[1]
    num_bits = sys.argv[2]

    bit_object = BitReader(buffer)

    num = bit_object.get_bits(int(num_bits))