from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import numpy as np
from perceval import Processor, PostSelect
import math
'''
class HeraldedCzItem():

    theta1 = 2*math.pi*54.74/180
    theta2 = 2*math.pi*17.63/180
    #The additional 2 factor takes into account the difference between the beam-splitter conventions of Perceval and the paper

    def __init__(self):

    @deprecated(version="0.10.0", reason="Use build_circuit or build_processor instead")
    def build(self):
        if self._opt('type') == AsType.CIRCUIT:
            return self.build_circuit()
        elif self._opt('type') == AsType.PROCESSOR:
            return self.build_processor(backend=self._opt('backend'))

    def build_circuit(self, **kwargs) -> Circuit:
        # the matrix of this first circuit is the same as the one presented in the reference paper, the difference in the second phase shift - placed on mode 3 instead of mode 1 - is due to a different convention for the beam-splitters (signs inverted in second column).
        last_modes_cz = (Circuit(4)
                         .add(0, PS(math.pi), x_grid=1)
                         .add(3, PS(math.pi), x_grid=1)
                         .add((1, 2), PERM([1, 0]), x_grid=1)
                         .add((0, 1), BS.H(theta=self.theta1), x_grid=2)
                         .add((2, 3), BS.H(theta=self.theta1), x_grid=2)
                         .add((1, 2), PERM([1, 0]))
                         .add((0, 1), BS.H(theta=-self.theta1))
                         .add((2, 3), BS.H(theta=self.theta2)))

        return (Circuit(6, name="Heralded CZ")
                .add(1, PERM([1, 0]))
                .add(2, last_modes_cz, merge=True)
                .add(1, PERM([1, 0])))

    def build_processor(self, **kwargs) -> Processor:
        p = self._init_processor(**kwargs)
        return p.add_port(0, Port(Encoding.DUAL_RAIL, 'ctrl')) \
            .add_port(2, Port(Encoding.DUAL_RAIL, 'data')) \
            .add_herald(4, 1) \
            .add_herald(5, 1)
'''


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
    parameters[0].set_value(2*54.74 / 180 * np.pi)
    parameters[1].set_value(2*54.74 / 180 * np.pi)
    parameters[2].set_value(-2*54.74 / 180 * np.pi)
    parameters[3].set_value(2*17.63 / 180 * np.pi)

    proc.set_circuit(circuit)

    # Set Post Selection
    proc.set_postselection(PostSelect("[4,5] == 1"))

    final_circuit = proc.linear_circuit()

    return pcvl.pdisplay(final_circuit.U)


'''
add CZ gate to an existing processor
'''


def add_CZGate_6modes(processor):
    thetalist = [54.74, 54.74, -54.74, 17.63]
    thetalist = [2*x / 180 * np.pi for x in thetalist]
    processor.add(1, PS(phi=np.pi))
    processor.add(3, PS(phi=np.pi))

    processor.add(0, PERM([0, 1, 2, 4, 3, 5]))
    processor.add(0, PERM([0, 1, 3, 2, 4, 5]))

    processor.add(1, BS(theta=thetalist[0]))

    processor.add(4, BS(theta=thetalist[1]))

    processor.add(0, PERM([0, 1, 4, 3, 2, 5]))

    processor.add(1, BS(theta=thetalist[2]))

    processor.add(4, BS(theta=thetalist[3]))

    # Set parameters:
    # parameters = processor.get_parameters()
    # parameters[0].set_value(54.74 / 180 * np.pi)
    # parameters[1].set_value(54.74 / 180 * np.pi)
    # parameters[2].set_value(-54.74 / 180 * np.pi)
    # parameters[3].set_value(17.63 / 180 * np.pi)

    # Set Post Selection
    processor.set_postselection(PostSelect("[4,5] == 1"))

    return


def test_CZ_6modes():
    # First,we convert the CZ to a CNOT
    proc = Processor("SLOS", 6)
    proc.add(2, BS.H())
    add_CZGate_6modes(proc)
    proc.add(2, BS.H())

    states = {
        pcvl.BasicState([1, 0, 1, 0, 0, 0]): "00",
        pcvl.BasicState([1, 0, 1, 0, 0, 1]): "00",
        pcvl.BasicState([1, 0, 1, 0, 1, 0]): "00",
        pcvl.BasicState([1, 0, 1, 0, 1, 1]): "00",
        pcvl.BasicState([1, 0, 0, 1, 0, 0]): "01",
        pcvl.BasicState([1, 0, 0, 1, 0, 1]): "01",
        pcvl.BasicState([1, 0, 0, 1, 1, 0]): "01",
        pcvl.BasicState([1, 0, 0, 1, 1, 1]): "01",
        pcvl.BasicState([0, 1, 1, 0, 0, 0]): "10",
        pcvl.BasicState([0, 1, 1, 0, 0, 1]): "10",
        pcvl.BasicState([0, 1, 1, 0, 1, 0]): "10",
        pcvl.BasicState([0, 1, 1, 0, 1, 1]): "10",
        pcvl.BasicState([0, 1, 0, 1, 0, 0]): "11",
        pcvl.BasicState([0, 1, 0, 1, 0, 1]): "11",
        pcvl.BasicState([0, 1, 0, 1, 1, 0]): "11",
        pcvl.BasicState([0, 1, 0, 1, 1, 1]): "11"
    }

    ca = pcvl.algorithm.Analyzer(proc, states)

    truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}
    ca.compute(expected=truth_table)

    pcvl.pdisplay(ca)
    print(
        f"performance = {ca.performance}, fidelity = {ca.fidelity.real}")


'''
Implement the CZ gate with 4 modes
Input: four parameters, which denotes the four angles
'''


def CZGate_4modes(params):
    return


if __name__ == "__main__":
    test_CZ_6modes()
