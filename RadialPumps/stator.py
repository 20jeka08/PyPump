import numpy as np
from RadialPumps.impeller import PyPumpRadialImpeller

class PyPumpRadialStatorVanes(PyPumpRadialImpeller):
    def __init__(self, H, Q, n, i, ro):
        super().__init__(H, Q, n, i, ro)

    def Z_diffuser_vanes(self, Z_impeller):
        '''Recommended value of stator vanes blades Z2 [-]'''

        if Z_impeller == 5:
            Z2 = [7, 8, 12]
            return Z2
        elif Z_impeller == 6:
            Z2 = [10]
            return Z2
        elif Z_impeller == 7:
            Z2 = [9, 10, 11, 12]
            return Z2

    def D3_D2(self):
        '''Recomended value of D3 to D2 ratio by Gulich'''
        nq = self.nq()
        if self.Hi < 100:
            D3toD2 = 1.015
        else:
            if nq < 40:
                D3toD2 = 1.015+0.08*((self.ro*self.Hi)/(1000*1000)-0.1)**0.8
            else:
                D3toD2 = 1.04+0.001*(nq-40)

        return D3toD2

    def D3(self, D2, D3toD2):
        '''Calculation of radial position of Leading edge of stator vanes - D3 [mm]'''
        D3 = D2*D3toD2
        return D3

    def b3_b2(self):
        '''Recomended the smallest and biggest values of b3 to b2 ratio [-]'''
        b3tob2 = [1.05, 1.3]
        return b3tob2

    def b3(self, b3tob2, b2):
        '''Calculation width of inlet to diffuser vanes - b3 [mm]'''
        b3 = b3tob2*b2
        return b3

    def D4_D2(self, priority=1.1):
        '''Recomended ratio of outlet diameter of diffuser vanes to impeller diameter  - D4 to D2 [-],
        Input parameters: priority - is coefficient from 1.05 to 1.15. The biggest value of priority for best
        efficiency. Default value is 1.1'''
        nq = self.nq()
        D4toD2 = priority+0.01*nq
        return D4toD2

    def D4(self, D4toD2, D2):
        '''Return value of outlet diameter of diffusor vanes - D4 [mm]'''
        D4 = D2*D4toD2
        return D4

    def c3m(self, D3, b3):
        Q = self.Q
        D3 = D3/1000.0
        b3 = b3/1000.0
        c3m = Q/(np.pi*D3*b3)
        return c3m

    def c3u(self, D2, D3, c2u):
        c3u = (D2*c2u)/D3
        return c3u

    def alpha3(self, c3m, c3u, incidence = 1.0):
        tanAlpha3 = c3m/c3u
        alpha3 = np.arctan(tanAlpha3) * 180 / np.pi
        alpha3 = alpha3 + incidence
        return alpha3

    def alpha4(self, alpha3, D4toD2):

        nq = self.nq()
        priority = D4toD2-0.01*nq
        R1 = 7.3
        L_min = 55.6
        L_max = 94.1
        R1toLmin = 0.13129
        R1toLmax = 0.07757
        R1_L = -0.537*priority+0.695
        delta_alpha = 16.5*np.sqrt(R1_L)
        alpha4 = alpha3 + delta_alpha

        return alpha4

    def c6m(self, c1m):
        c6m = 0.875*c1m
        return c6m

    def b6(self, c6m, D6):
        Q = self.Q
        D6 = D6/1000.0
        b6 = Q/(np.pi*D6*c6m)
        b6 = b6*1000.0
        return b6

    def alpha5(self, alpha4, b3, b6):
        alpha5 = b3/b6*alpha4
        return alpha5

    def alpha6(self):
        alpha6 = 94.0
        return alpha6








if __name__ == '__main__':
    stator = PyPumpRadialStatorVanes(1150, 260/3600, 2910, 10, 997)
    D3toD2 = stator.D3_D2()
    D2 = 308.0
    b2 = 22
    u2 = stator.u2(D2)
    HydrEff = stator.HydraulicEfficiencyRadialPumpSingleStage()
    c2u = stator.c2u(hydraulicEff=HydrEff, u2=u2)

    c1m = stator.c1m(D1=190.0, shaftD=138.0, volumeEfficiency=97)
    print(D3toD2)
    D3 = stator.D3(D2=D2, D3toD2=D3toD2)
    print(D3)
    D4toD2 = stator.D4_D2(priority=1.05)
    print('D4toD2: ', D4toD2)
    D4 = stator.D4(D4toD2=D4toD2, D2=D2)
    print('D4: ', D4)
    b3tob2 = stator.b3_b2()[0]
    print(b3tob2)
    b3 = stator.b3(b3tob2=b3tob2, b2=b2)
    print(b3)

    c3m = stator.c3m(D3=D3, b3=b3)
    print(c3m)
    c3u = stator.c3u(D2=D2, D3=D3, c2u=c2u)
    print(c2u)
    print(c3u)
    alpha3 = stator.alpha3(c3m=c3m, c3u=c3u, incidence=0.0)
    print(alpha3)
    alpha4 = stator.alpha4(alpha3=alpha3, D4toD2=D4toD2)
    print(alpha4)
    c6m = stator.c6m(c1m=c1m)
    b6 = stator.b6(c6m=c6m, D6=190.0)
    print(b6)
    alpha5 = stator.alpha5(alpha4=alpha4, b3=b3, b6=b6)
    print(alpha5)


