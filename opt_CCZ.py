from perceval.components.unitary_components import PS, BS, PERM
import perceval as pcvl
import random
import math
from perceval import Processor, PostSelect, Circuit


def create_paramaters():
    phis = [pcvl.P("Phi" + str(i)) for i in range(0, 6)]
    thetas = [pcvl.P("Theta" + str(i)) for i in range(0, 9)]
    return phis, thetas


def set_phis(phis, values=None):
    if not values:
        phis = [phis[i].set_value(random.random() * 2 * math.pi) for i in range(6)]
    else:
        phis = [phis[i].set_value(values[i]) for i in range(6)]


def set_thetas(thetas, values=None):
    if not values:
        thetas = [thetas[i].set_value(random.random() * 2 * math.pi) for i in range(9)]
    else:
        thetas = [thetas[i].set_value(values[i]) for i in range(9)]


def CCZ_9mode(phis, thetas):
    mzi = pcvl.Circuit(m=6, name="CCZ6")
    for i in range(len(phis)):
        mzi.add(i, PS(phis[i]))

    mzi.add((0, 1), BS(thetas[0]))
    mzi.add((2, 3), BS(thetas[1]))
    mzi.add((4, 5), BS(thetas[2]))
    mzi.add((1, 2), BS(thetas[3]))
    mzi.add((3, 4), BS(thetas[4]))

    mzi.add(0, PERM([0, 1, 3, 2]))
    mzi.add((1, 2), BS(thetas[5]))
    mzi.add((3, 4), BS(thetas[6]))
    mzi.add(0, PERM([0, 1, 3, 2]))

    mzi.add(0, PERM([0, 2, 1, 3, 5, 4]))
    mzi.add((0, 1), BS(thetas[7]))
    mzi.add((3, 4), BS(thetas[8]))
    mzi.add(0, PERM([0, 2, 1, 3, 5, 4]))
    return mzi


def CCZ(phis, thetas):
    c1 = Circuit(9, name="CCZ")
    c1.add(5, PERM([1, 0]))
    c1.add(3, PERM([1, 0]))
    c1.add(4, PERM([1, 0]))

    c1.add(1, PERM([1, 0]))
    c1.add(2, PERM([1, 0]))
    c1.add(3, PERM([1, 0]))
    c1.add(3, CCZ_9mode(phis, thetas), merge=True)
    c1.add(5, PERM([1, 0]))
    c1.add(3, PERM([1, 0]))
    c1.add(4, PERM([1, 0]))

    c1.add(1, PERM([1, 0]))
    c1.add(2, PERM([1, 0]))
    c1.add(3, PERM([1, 0]))

    return c1


def CCZ_proc(phis, thetas):
    c1 = CCZ(phis, thetas)
    p1 = Processor("SLOS", c1)
    p1.set_postselection(PostSelect("[0,1]==1 & [2,3]==1 & [4,5]==1"))
    p1.add_herald(6, 0)
    p1.add_herald(7, 0)
    p1.add_herald(8, 0)
    return p1


def fidelity(phis=None, thetas=None):
    set_phis(phis)
    set_thetas(thetas)
    proc = Processor("SLOS")
    proc.add(4, pcvl.BS.H())
    proc.add(0, p1)
    proc.add(4, pcvl.BS.H())

    states = {
        pcvl.BasicState([1, 0, 1, 0, 1, 0]): "000",
        pcvl.BasicState([1, 0, 1, 0, 0, 1]): "001",
        pcvl.BasicState([1, 0, 0, 1, 1, 0]): "010",
        pcvl.BasicState([1, 0, 0, 1, 0, 1]): "011",
        pcvl.BasicState([0, 1, 1, 0, 1, 0]): "100",
        pcvl.BasicState([0, 1, 1, 0, 0, 1]): "101",
        pcvl.BasicState([0, 1, 0, 1, 1, 0]): "110",
        pcvl.BasicState([0, 1, 0, 1, 0, 1]): "111",
    }

    ca = pcvl.algorithm.Analyzer(proc, states)

    truth_table = {
        "000": "000",
        "001": "001",
        "010": "010",
        "011": "011",
        "100": "100",
        "101": "101",
        "110": "111",
        "111": "110",
    }
    ca.compute(expected=truth_table)

    return ca.performance, ca.fidelity.real


if __name__ == "__main__":
    phis, thetas = create_paramaters()
    p1 = CCZ_proc(phis, thetas)
    print(fidelity(phis, thetas))
