import re
import cirq
import tqdm
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from noise._simplex import noise4

points_num = 40_000
radius = 200
width,height = 500, 500
length = 50
scale = 0.006
time = 0
frames = 250

# creating circuit
qubits = cirq.LineQubit.range(points_num)
circuit = cirq.Circuit()

# applying Hadamard to each qubit to create superposition
circuit.append(cirq.H(qubits[i]) for i in range(points_num))

# measuring each qubit to get collapse
circuit.append(cirq.measure(q, key=str(q)) for q in qubits)

def simulating_circuit(precision = 0):
    int_list = []
    simulator = cirq.Simulator()

    if precision == 0:
        repetitions = 64
    else:
        repetitions = 128

    result = simulator.run(circuit, repetitions=repetitions)
    output_string = (str(result))

    # defining a regular expression pattern to extract binary values after '='
    pattern = re.compile(r'=\s*([01]+)')
    matches = pattern.findall(output_string)
    result_list = list(matches)
    int_list = [int(c,2) for c in result_list]
    return int_list

