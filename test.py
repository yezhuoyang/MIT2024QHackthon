
import perceval as pcvl



'''
processor = pcvl.Processor("SLOS", 4)
processor.add(2, pcvl.BS.H())
processor.add(0, pcvl.catalog["heralded cz"].build_processor())
processor.add(2, pcvl.BS.H())

states = {
    pcvl.BasicState([1, 0, 1, 0]): "00",
    pcvl.BasicState([1, 0, 0, 1]): "01",
    pcvl.BasicState([0, 1, 1, 0]): "10",
    pcvl.BasicState([0, 1, 0, 1]): "11"
}

ca = pcvl.algorithm.Analyzer(processor, states)

truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}
ca.compute(expected=truth_table)
'''
def test_fidelity(processor, states, truth_table):
    ca = pcvl.algorithm.Analyzer(processor, states)
    ca.compute(expected=truth_table)    
    return ca.performance, ca.fidelity.real



def get_number_of_photon():
    return



def get_number_of_modes():
    return

