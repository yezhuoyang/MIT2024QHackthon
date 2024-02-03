from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import numpy as np
from perceval import Processor,PostSelect
'''
Four modes,  2 180 Wave plate , 2 Perm , 2 (54.74,0)PBS, 2 (-54.74,0)PBS, 2 post selection
'''


'''
Implement the CZ gate with 6 modes
Input: four parameters, which denotes the four angles
'''
def CZGate_6modes(params):

    proc = Processor("SLOS", 6)

    # Defining the circuit
    circuit = pcvl.Circuit(6)

    circuit.add(1, PS(phi=np.pi))
    circuit.add(3, PS(phi=np.pi))


    circuit.add(0, PERM([0, 1, 2, 4, 3, 5]))
    circuit.add(0, PERM([0, 1, 3, 2, 4, 5]))

    circuit.add(1, BS(theta=pcvl.P('theta1')))

    circuit.add(4, BS(theta=pcvl.P('theta2')))

    circuit.add(0, PERM([0, 1, 4, 3, 2, 5]))

    circuit.add(1, BS(theta=pcvl.P('theta3')))

    circuit.add(4, BS(theta=pcvl.P('theta4')))

    # Set parameters:
    parameters = circuit.get_parameters()
    parameters[0].set_value(54.74 / 180 * np.pi)
    parameters[1].set_value(54.74 / 180 * np.pi)
    parameters[2].set_value(-54.74 / 180 * np.pi)
    parameters[3].set_value(17.63 / 180 * np.pi)

    proc.set_circuit(circuit)

    # Set Post Selection
    proc.set_postselection(PostSelect("[4,5] == 1"))

    final_circuit = proc.linear_circuit()

    return pcvl.pdisplay(final_circuit.U)


'''
Implement the CZ gate with 4 modes
Input: four parameters, which denotes the four angles
'''
def CZGate_4modes(params):
    return





if __name__ == "__main__":
    ps = PS(phi=np.pi)

    print(ps.name)
    print(ps.describe())
    pcvl.pdisplay(ps.definition())
    pcvl.pdisplay(ps)  # A pdisplay call on a circuit/processor needs to be the last line of a cell

