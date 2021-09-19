import numpy as np
from impeller import PyPumpRadialImpeller

class PyPumpRadialStatorVanes(PyPumpRadialImpeller):
    def __init__(self, H, Q, n, i, ro):
        super().__init__(H, Q, n, i, ro)

    def Z3(self):
        '''Recommended value of stator vanes blades'''

        Z3 = 9
        return Z3

    def D3toD2(self, D2):
        '''Recomended value of D3 to D2 ratio by Gulich'''

        D3toD2 = 1.035
        return D3toD2


if __name__ == '__main__':
    stator = PyPumpRadialStatorVanes(1150, 260/3600, 2910, 12, 997)
    print(stator.ns())
