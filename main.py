# This is an example of the file you must have in your main git branch
import perceval as pcvl
from opt_CCZ import CCZ_proc
from opt_CCZ import create_paramaters


params = [
    2.16229035,
    2.32355081,
    3.14159843,
    4.20592149,
    1.05179214,
    4.70936268,
    1.05272042,
    0.2410778,
    4.87299728,
    1.48332889,
    0.19210323,
    1.94935521,
    1.45815626,
    0.81566202,
    1.25720826,
    0.93387039,
    1.89597638,
    3.14152039,
    5.18063196,
    1.13067133,
]




def get_CCZ() -> pcvl.Processor:
    phis,theta=create_paramaters(params)
    return CCZ_proc(phis,theta)


if __name__ == "__main__":
    ccz = get_CCZ()
