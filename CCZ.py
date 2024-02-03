from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import numpy as np
from perceval import Processor, PostSelect






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



