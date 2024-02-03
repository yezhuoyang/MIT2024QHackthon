from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import math
from perceval import Processor, PostSelect, Circuit, Port
from perceval.utils import Encoding


"""
Four modes,  2 180 Wave plate , 2 Perm , 2 (54.74,0)PBS, 2 (-54.74,0)PBS, 2 post selection
"""

"""
Implement the CZ gate with 6 modes
Input: four parameters, which denotes the four angles
"""


def CZ_4mode():
    phi1 = pcvl.P("phi1")
    theta = pcvl.P("theta")
    theta2 = pcvl.P("theta2")
    theta3 = pcvl.P("theta3")
    phi1.set_value(math.pi)
    theta.set_value(2 * math.pi * 54.74 / 180)
    theta2.set_value(2 * math.pi * -54.74 / 180)
    theta3.set_value(2 * math.pi * 17.63 / 180)
    circ = pcvl.Circuit(m=4, name="mzi")
    circ.add(0, PS(phi1)).add(1, PS(phi1)).add(0, PERM([0, 2, 1, 3])).add(
        (0, 1), BS(theta)
    ).add((2, 3), BS(theta)).add(0, PERM([0, 2, 1, 3])).add((0, 1), BS(theta2)).add(
        (2, 3), BS(theta3)
    )
    return circ


def CZGate():
    circ4mode = CZ_4mode()
    return (
        Circuit(6, name="Heralded CZ")
        .add(1, PERM([1, 0]))
        .add(2, circ4mode, merge=True)
        .add(1, PERM([1, 0]))
    )


def CZ_proc():
    circ = CZGate()
    proc = Processor("SLOS", circ)
    proc.add_port(0, Port(Encoding.DUAL_RAIL, "ctrl")).add_port(
        2, Port(Encoding.DUAL_RAIL, "data")
    ).add_herald(4, 1).add_herald(5, 1)

    return proc


def test_CZ():
    proc = Processor("SLOS", 4)
    proc.add(2, pcvl.BS.H())
    proc.add(0, CZ_proc())
    proc.add(2, pcvl.BS.H())

    states = {
        pcvl.BasicState([1, 0, 1, 0]): "00",
        pcvl.BasicState([1, 0, 0, 1]): "01",
        pcvl.BasicState([0, 1, 1, 0]): "10",
        pcvl.BasicState([0, 1, 0, 1]): "11",
    }

    ca = pcvl.algorithm.Analyzer(proc, states)

    truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}
    ca.compute(expected=truth_table)

    pcvl.pdisplay(ca)
    print(f"performance = {ca.performance}, fidelity = {ca.fidelity.real}")


if __name__ == "__main__":
    test_CZ()
