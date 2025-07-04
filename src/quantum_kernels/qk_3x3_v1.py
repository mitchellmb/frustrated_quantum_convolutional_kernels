import cudaq
from typing import List

@cudaq.kernel 
def kernel(rotations_0: List[float], rotations_1: List[float], rotations_2: List[float], rotations_3: List[float], j1: float, j2: float, zeeman: float): 
    # TODO - make programmatic after testing

    qubits = cudaq.qvector(9)

    h(qubits)

    #B
    for qubit in qubits:
        ry(zeeman, qubit)

    #J1 & input
    # upper left
    controls_0 = [0, 3, 0, 1]
    targets_0 = [1, 4, 3, 4]
    # upper right
    controls_1 = [1, 4, 1, 2]
    targets_1 = [2, 5, 4, 5]
    # lower left
    controls_2 = [3, 6, 3, 4]
    targets_2 = [4, 7, 6 ,7]
    # lower right
    controls_3 = [4, 7, 4, 5]
    targets_3 = [5, 8, 7 ,8]
    
    for i in range(4):
        x.ctrl(qubits[controls_0[i]], qubits[targets_0[i]])
        rz(rotations_0[i], qubits[targets_0[i]]) 
        rx(j1, qubits[targets_0[i]]) 
        x.ctrl(qubits[controls_0[i]], qubits[targets_0[i]])

        x.ctrl(qubits[controls_1[i]], qubits[targets_1[i]])
        rz(rotations_1[i], qubits[targets_1[i]]) 
        rx(j1, qubits[targets_1[i]]) 
        x.ctrl(qubits[controls_1[i]], qubits[targets_1[i]])

        x.ctrl(qubits[controls_2[i]], qubits[targets_2[i]])
        rz(rotations_2[i], qubits[targets_2[i]]) 
        rx(j1, qubits[targets_2[i]]) 
        x.ctrl(qubits[controls_2[i]], qubits[targets_2[i]])

        x.ctrl(qubits[controls_3[i]], qubits[targets_3[i]])
        rz(rotations_3[i], qubits[targets_3[i]]) 
        rx(j1, qubits[targets_3[i]]) 
        x.ctrl(qubits[controls_3[i]], qubits[targets_3[i]])
    

    # J2 & input
    # Hard coded diagonals    
    # upper left
    diag_0_1 = (rotations_0[0] + rotations_0[3])/2.0
    diag_0_2 = (rotations_0[2] + rotations_0[1])/2.0
    x.ctrl(qubits[0], qubits[4])
    rz(diag_0_1, qubits[4])
    rx(j2, qubits[4])
    x.ctrl(qubits[0], qubits[4])

    x.ctrl(qubits[3], qubits[1])
    rz(diag_0_2, qubits[1])
    rx(j2, qubits[1])
    x.ctrl(qubits[3], qubits[1])


    # upper right
    diag_1_1 = (rotations_1[0] + rotations_1[3])/2.0
    diag_1_2 = (rotations_1[2] + rotations_1[1])/2.0
    x.ctrl(qubits[1], qubits[5]) 
    rz(diag_1_1, qubits[5])
    rx(j2, qubits[5])
    x.ctrl(qubits[1], qubits[5])

    x.ctrl(qubits[4], qubits[2])
    rz(diag_1_2, qubits[2])
    rx(j2, qubits[2])
    x.ctrl(qubits[4], qubits[2])


    # lower left
    diag_2_1 = (rotations_2[0] + rotations_2[3])/2.0
    diag_2_2 = (rotations_2[2] + rotations_2[1])/2.0
    x.ctrl(qubits[3], qubits[7])
    rz(diag_2_1, qubits[7])
    rx(j2, qubits[7])
    x.ctrl(qubits[3], qubits[7])

    x.ctrl(qubits[6], qubits[4])
    rz(diag_2_2, qubits[4])
    rx(j2, qubits[4])
    x.ctrl(qubits[6], qubits[4])


    # lower right
    diag_3_1 = (rotations_3[0] + rotations_3[3])/2.0
    diag_3_2 = (rotations_3[2] + rotations_3[1])/2.0
    x.ctrl(qubits[4], qubits[8]) 
    rz(diag_3_1, qubits[8])
    rx(j2, qubits[8])
    x.ctrl(qubits[4], qubits[8])

    x.ctrl(qubits[7], qubits[5])
    rz(diag_3_2, qubits[5])
    rx(j2, qubits[5])
    x.ctrl(qubits[7], qubits[5])

    # B
    for qubit in qubits:
        ry(zeeman, qubit)

    mz()