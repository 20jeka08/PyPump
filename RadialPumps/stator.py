import numpy as np
from impeller import PyPumpRadialImpeller

class PyPumpRadialStatorVanes(PyPumpRadialImpeller):
    def __init__(self, H, Q, n, i, ro):
        super().__init__(H, Q, n, i, ro)

    def Z3(self):
        '''Recommended value of stator vanes blades'''

        Z3 = 9
        return Z3

    def D3toD2(self):
        '''Recomended value of D3 to D2 ratio by Gulich'''
        nq = self.nq()
        print(nq)
        if self.Hi < 100:
            D3toD2 = 1.015
        else:
            if nq < 40:
                D3toD2 = 1.015+0.08*((self.ro*self.Hi)/(1000*1000)-0.1)**0.8
            else:
                D3toD2 = 1.04+0.001*(nq-40)

        return D3toD2

    def D3(self, D2, D3toD2):
        '''Calculation of radial position of Leading edge of stator vanes [mm]'''
        D3 = D2*D3toD2
        return D3


if __name__ == '__main__':
    stator = PyPumpRadialStatorVanes(1150, 260/3600, 2910, 10, 997)
    D3toD2 = stator.D3toD2()
    print(D3toD2)
    D3 = stator.D3(D2=318, D3toD2=D3toD2)
    print(D3)
