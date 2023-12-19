import re
import cirq
import tqdm
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from noise._simplex import noise4

from quantum_circuit import *

def pack_128_bit_integer(int_value):
    # Assuming int_value is a 128-bit integer represented as two 64-bit integers
    upper_bits = int_value >> 64
    lower_bits = int_value & 0xFFFFFFFFFFFFFFFF

    # Pack the two 64-bit integers into a bytes object
    packed_bytes = struct.pack('QQ', upper_bits, lower_bits)
    return packed_bytes

def unpack_128_bit_integer(packed_bytes):
    # Unpack the bytes into two 64-bit integers
    upper_bits, lower_bits = struct.unpack('QQ', packed_bytes)

    # Combine the two 64-bit integers into a single 128-bit integer
    int_value = (upper_bits << 64) | lower_bits
    return int_value

def qn_random_float_generator_64(min: float = 0, max: float = 2*np.pi):
    int_list = simulating_circuit()
    random_desired_list = []
    for int_value in int_list:
        unpacked = 0x3FF0000000000000 | int_value >> 12
        packed = struct.pack('Q',unpacked)
        value = struct.unpack('d',packed)[0] - 1.0
        final = min + (max-min) * value
        random_desired_list.append(final)
    return np.array(random_desired_list)

def qn_random_float_generator_128(min: float = 0, max: float = 2*np.pi):
    int_list = simulating_circuit(1)
    random_desired_list = []
    for int_value in int_list:
        _packed = pack_128_bit_integer(int_value)
        value = unpack_128_bit_integer(_packed) / (2**128)
        final = min + (max-min) * value
        random_desired_list.append(final)
    return np.array(random_desired_list)

