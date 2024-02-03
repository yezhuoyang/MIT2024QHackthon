
import perceval as pcvl
from perceval.components.unitary_components import PS, BS, PERM
import numpy as np

## Use the symbolic skin for display
from perceval.rendering.circuit import DisplayConfig, SymbSkin

#The implementation for single qubit gates



circuit_x = PERM([1,0])  #it's not the only way
circuit_y = PERM([1,0]) // (0,PS(-np.pi/2)) // (1,PS(np.pi/2))
circuit_z = pcvl.Circuit(2) // (1,PS(np.pi))
circuit_h = BS.H()

circuit_rx = pcvl.Circuit(2) // (0, PS(np.pi)) // BS.Rx(theta=pcvl.P("theta")) // (0, PS(np.pi)) #Be careful for the minus ! We use a convention
circuit_ry = BS.Ry(theta=pcvl.P("theta"))
circuit_rz = BS.H() // circuit_rx // BS.H()  # Indeed, Rz = H Rx H. Of course, we would like to be able to have many parameters with the same name. It will come soon :)