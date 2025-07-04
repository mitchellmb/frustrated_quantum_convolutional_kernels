import cudaq
from typing import List

@cudaq.kernel 
def kernel(rotations: List[float], j1: float, j2: float, zeeman: float):
    
    qubits = cudaq.qvector(len(rotations))

    h(qubits)

    #B
    for qubit in qubits:
        ry(zeeman, qubit)

    #J1 & input
    controls = [0, 2, 0, 1]
    targets =  [1, 3, 2, 3]

    for i in range(4):
        x.ctrl(qubits[controls[i]], qubits[targets[i]])
        rz(rotations[i], qubits[targets[i]]) 
        rx(j1, qubits[targets[i]]) 
        x.ctrl(qubits[controls[i]], qubits[targets[i]])


    #J2 & input
    diag_1 = (rotations[0] + rotations[3])/2.0 # average diagonal values to set rotations
    diag_2 = (rotations[2] + rotations[1])/2.0

    x.ctrl(qubits[0], qubits[3])
    rz(diag_1, qubits[3])
    rx(j2, qubits[3])
    x.ctrl(qubits[0], qubits[3])

    x.ctrl(qubits[2], qubits[1])
    rz(diag_2, qubits[1])
    rx(j2, qubits[1])
    x.ctrl(qubits[2], qubits[1])

    #B
    for qubit in qubits:
        ry(zeeman, qubit)

    mz()