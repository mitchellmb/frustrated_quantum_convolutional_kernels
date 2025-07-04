import cudaq
from typing import List

@cudaq.kernel 
def kernel(rotations: List[float], j1: float, j2: float, zeeman: float): 
    
    qubits = cudaq.qvector(len(rotations))

    h(qubits) # initialize in xy-plane

    #B & input
    for idx, qubit in enumerate(qubits):
        rz(rotations[idx], qubit)
        ry(zeeman, qubit)

    #J1 - pseudo-exchange ~ bond-dependent bias towards/away z-axis
    controls = [0, 2, 0, 1]
    targets =  [1, 3, 2, 3]

    for i in range(4):
        x.ctrl(qubits[controls[i]], qubits[targets[i]])
        rx(j1, qubits[targets[i]]) 
        x.ctrl(qubits[controls[i]], qubits[targets[i]])

    #J2 - pseudo-exchange ~ bond-dependent bias towards/away z-axis
    x.ctrl(qubits[0], qubits[3])
    rx(j2, qubits[3])
    x.ctrl(qubits[0], qubits[3])

    x.ctrl(qubits[2], qubits[1])
    rx(j2, qubits[1])
    x.ctrl(qubits[2], qubits[1])

    #B - pseudo-zeeman ~ global bias to move in pseudo-magnetic phase space
    for qubit in qubits:
        ry(zeeman, qubit)

    mz() # z-axis measurement