from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import math
from perceval import Processor, Circuit


def CZ_4mode(params):
    phi1 = params[0]
    theta1 = params[1]
    theta2 = params[2]
    theta3 = params[3]
    circ = pcvl.Circuit(m=4, name="mzi")
    circ.add(0, PS(phi1)).add(1, PS(phi1)).add(0, PERM([0, 2, 1, 3])).add(
        (0, 1), BS(theta1)
    ).add((2, 3), BS(theta1)).add(0, PERM([0, 2, 1, 3])).add((0, 1), BS(theta2)).add(
        (2, 3), BS(theta3)
    )
    return circ


def CZGate(params):
    circ4mode = CZ_4mode(params)
    return (
        Circuit(6, name="Heralded CZ")
        .add(1, PERM([1, 0]))
        .add(2, circ4mode, merge=True)
        .add(1, PERM([1, 0]))
    )


def CZ_proc(params):
    circ = CZGate(params)
    proc = Processor("SLOS", circ)
    proc.add_herald(4, 1).add_herald(5, 1)
    return proc






def fidelity(params):
    proc = Processor("SLOS", 4)
    proc.add(2, pcvl.BS.H())
    proc.add(0, CZ_proc(params))
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

    #pcvl.pdisplay(ca)
    #print(f"performance = {ca.performance}, fidelity = {ca.fidelity.real}")
    print(ca.fidelity.real)
    return -ca.fidelity.real

import numpy as np
from scipy.optimize import minimize

def optimize_CZ():
    params = np.ones(15)
    res = minimize(fidelity, params, method="SLSQP")
    print(res)
    print(res.x)


if __name__ == "__main__":
    optimize_CZ()

