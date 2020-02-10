import numpy as np

class PyPumpRadialImpeller():
    def __init__(self, H, Q, n, i, ro):
        self.H = H
        self.Q = Q
        self.n = n
        self.i = i
        self.Hi = H/i
        self.ro = ro

    def ns(self):
        '''Specific speed of the pump (RU)'''
        ns = 3.65*self.n*(np.sqrt(self.Q)/(self.Hi**0.75))
        return round(ns, 2)

    def nq(self):
        '''Specific speed of the pump (EU)'''
        nq = self.n * (np.sqrt(self.Q) / (self.Hi ** 0.75))
        return round(nq, 2)

    def psi(self, ft=1.05):
        '''Calculation of the recommended head coefficient - psi, choose ft - from 1.0 to 1.1
         for steep and stability of H-Q curve ft value has to be less'''
        psi = 1.21*ft*np.e**(-0.77*self.nq()/100.0)
        return round(psi, 2)

    def D2(self, psi):
        '''Calculation of recommended diameter of impeller D2 [mm] with defined head coefficient - psi'''
        D2 = 84.6 / self.n * np.sqrt(self.Hi / psi) * 1000
        return round(D2, 2)

    def b2(self, D2):
        '''Calculation recommended outlet width of the impeller - b2 [mm] with defined - D2 [mm]'''
        b2_to_D2 = 0.017+0.262*self.nq()/100-0.08*(self.nq()/100)**2+0.0093*(self.nq()/100)**3
        b2 = D2*b2_to_D2
        return round(b2, 2)

    def HydraulicEfficiencyRadialPumpSingleStage(self):
        '''Estimation of the centrifugal (radial) single stage pump hydraulic efficiency [%]. Hydraulic
        efficiency value based on specific speed - nq (nq<=100), and volume flow rate - Q [m^3/s]'''
        if self.Q > 1.0:
            a = 0.5
        else:
            a = 1
        m = 0.08*a*(1.0/self.Q)**0.15*(45/self.nq())**0.06
        HydraulicEff = 1-0.055*(1.0/self.Q)**m-0.2*(0.26-np.log10(self.nq()/25))**2*(1.0/self.Q)**0.1
        return round(HydraulicEff*100, 2)

    def HydraulicEfficiencyRadialPumpMultistage(self):
        '''Estimation of the centrifugal (radial) multistage pump hydraulic efficiency [%]. Hydraulic efficiency
        value based on specific speed - nq (nq<=60), and volume flow rate - Q [m^3/s]'''
        if self.Q > 1.0:
            a = 0.5
        else:
            a = 1
        m = 0.08*a*(1.0/self.Q)**0.15*(45/self.nq())**0.06
        HydraulicEff = 1-0.065*(1.0/self.Q)**m-0.23*(0.3-np.log10(self.nq()/23))**2*(1.0/self.Q)**0.05
        return round(HydraulicEff * 100, 2)

    def EfficiencyRadialSingleStageSingeEntry(self):
        '''Estimation of the centrifugal (radial) pump efficiency [%] which is single stage and single entry
        Efficiency value based on specific speed - nq (nq<=100), and volume flow rate - Q [m^3/s]'''
        if self.Q>1.0:
            a = 0.5
        else:
            a = 1.0
        m = 0.1*a*(1.0/self.Q)**0.15*(45.0/self.nq())**0.06
        Efficiency = 1-0.095*(1.0/self.Q)**m-0.3*(0.35-np.log10(self.nq()/23.0))**2*(1.0/self.Q)**0.05
        return round(Efficiency*100, 2)

    def EfficiencyRadialMultistageSingleEntry(self):
        '''Estimation of the centrifugal (radial) multistage pump efficiency [%] which is single entry. Efficiency
        value based on specific speed - nq (nq<=60), and volume flow rate - Q [m^3/s]'''
        if self.Q > 1.0:
            a = 0.5
        else:
            a = 1.0
        m = 0.1 * a * (1.0 / self.Q) ** 0.15 * (45.0 / self.nq()) ** 0.06
        Efficiency = 1-0.116*(1.0/self.Q)**m-0.4*(0.26-np.log10(self.nq()/25))**2
        return round(Efficiency*100, 2)

    def EfficiencyRadialSingleStageDoubleEntry(self):
        '''Estimation of the centrifugal (radial) single stage pump efficiency [%] which is double entry. Efficiency
        value based on specific speed - nq (nq<=50), and volume flow rate - Q [m^3/s]'''
        if self.Q > 1.0:
            a = 0.5
        else:
            a = 1.0
        m = 0.1 * a * (1.0 / self.Q) ** 0.15 * (45.0 / self.nq()) ** 0.06
        Efficiency = 1-0.095*(1.0/self.Q)**m-0.35*(0.35-np.log10(self.nq()/17.7))**2*(1.0/self.Q)**0.05
        return round(Efficiency*100, 2)

    def shaftD(self, Pmax, factorSafety=1.1, Tau=15000000):
        '''Calculation of the shaft diameter - dw[mm], based on maximal power on shaft - Pmax [W],
         material property - Tau [N/m^2], and user's factor safety for increasing shaft diameter value'''
        dw = 3.65*(Pmax/self.n/Tau)**(1/3)
        return factorSafety*dw*1000.0

    def D1LambdaMethod(self, shaftD, lambdaC=1.15, lambdaW=0.2):
        '''Calculation recommended suction diameter - D1 [mm] based on two chosen coefficients lambdaC and lambdaW
         in general (1.1 < lambdaC < 1.2) and (0.1 < lambdaW < 0.3), shaftD - shaft diameter [mm]'''
        shaftD = shaftD/1000.0
        D1 = np.sqrt(shaftD**2+10.6*(self.Q/self.n)**(2/3)*((lambdaC+lambdaW)/lambdaW)**(1/3))
        return D1*1000.0

    def D1RelativeVelocityMinimum(self, shaftD, D2, psi, VolEff, fd=1.15):
        '''Calculation recommended suction diameter - D1 [mm] for minimum relative velocity (recommended for
        second (and following) stages of multistage pumps)
        shaftD - shaft diameter [mm], D2 - impeller diameter [mm], psi - head coefficient [-], nq - specific speed,
        VolEff - volume efficiency [%], fd - factor: for normal impellers 1.05<fd<1.15, for suction impellers
         1.15<fd<1.25'''
        shaftD = shaftD/D2
        VolEff = VolEff/100.0
        D1rel = fd*np.sqrt(shaftD**2+1.48*10**-3*psi*(self.nq()**1.33/(VolEff)**0.67))
        D1 = D2*D1rel
        return D1

    def D1RudnevMethod(self, shaftD, VolEff, alpha=0.08):
        '''Calculation recommended suction diameter - D1 [mm] based on alpha coefficient (Rudnev method),
        0.06 < alpha < 0.1 (default alpha = 0.08). shaftD - shaft diameter of the pump [mm],
        VolEff - volume efficiency [%]'''
        shaftD = shaftD/1000.0
        Qloss = self.Q*VolEff/100
        Qk = self.Q+Qloss
        V0 = alpha*(Qk*self.n**2)**(1/3)
        D1 = np.sqrt(4*Qk/np.pi/V0+shaftD**2)
        return D1*1000.0

    def Pmax(self, Efficiency):
        '''Estimation maximal power on shaft of the pump - Pmax [W], Efficiency - efficiency of the pump [%]'''
        Efficiency = Efficiency/100.0
        P = self.Q*self.H*self.ro*9.81/Efficiency
        if P<1000.0:
            k = 1.35
        elif P>=1000 and P<2000:
            k = 1.3
        elif P>=2000 and P<5000:
            k = 1.2
        elif P>=5000 and P<50000:
            k = 1.1
        elif P>=50000:
            k = 1.05
        Pmax = P*k
        return Pmax

    def VolumeEffEstimation(self):
        '''Estimation volume efficiency based on specific speed (RU), VolEff [%]'''
        VolEff = 1/(1+0.68/self.ns()**(2/3))
        return VolEff*100.0

    def bladeThickness(self, D2):
        '''Calculation blade thickness - e [mm] for D2 [mm], function returns e [mm]. Range of the value
        0.016 < e/D2 < 0.022 '''
        D2 = D2/1000.0
        if self.Hi > 600:
            e = 0.022*D2
        else:
            e = 0.019*D2
        return round(e*1000, 2)

    def impellerBladeNumber(self, highCavitaion=False):
        '''Recommended blade number of impeller Z, the range of this value from 5 to 7, for high NPSH and flat
        cavitation curve 5 or 6 number recommended'''
        if highCavitaion == True:
            Z = 5
        else:
            Z = 7

    # INLET VELOCITY TRIANGLE
    def c1m (self, D1, shaftD, volumeEfficiency=100):
        '''Calculation of the meridional axial component of the flow velocity - c1m [m/s], arguments:
        D1 [mm] - suction diameter of impeller, shaftD [mm] - diameter of the hub, volumeEfficiency [%] -
        volume efficiency of the pump'''
        volumeEfficiency = volumeEfficiency/100
        D1 = D1/1000.0
        shaftD = shaftD/1000.0
        Qloss = self.Q - self.Q*volumeEfficiency
        Qfull = self.Q + Qloss
        c1m = 4*Qfull/(np.pi*(D1**2-shaftD**2))
        return round(c1m, 2)

    def u1 (self, D):
        '''Calculation U1 velocity for any D [mm] and rotation speed - n [rev/min], returns u1 [m/s]'''
        D = D/1000.0
        u1 = self.n * np.pi / 30 * D / 2
        return round(u1, 2)

    def w1 (self, c1m, u1, c1u=0):
        '''Calculation relative velocity for inlet - w1 [m/s], arguments:
        c1m [m/s] - meridional axial component of velocity; u1 [m/s] - circumferential velocity for any diameter;
        c1u [m/s] - pre-swirl of the flow'''
        w1 = np.sqrt(c1m**2+(u1-c1u)**2)
        return round(w1, 2)

    def inletFlowCoefficient(self, c1m, u1):
        '''Calculation flow coefficient for inlet - phi [-], arguments:
        c1m [m/s] - meridional axial component of velocity; u1 [m/s] - circumferential velocity for any diameter;'''
        phi = c1m/u1
        return round(phi, 2)

    def inletFlowAngleRelative (self, c1m, u1, c1u=0):
        '''Calculation of the flow angle for inlet, arguments: c1m [m/s] - meridional axial component of velocity;
        u1 [m/s] - circumferential velocity for any diameter;  c1u [m/s] - pre-swirl of the flow'''
        Beta1withoutBlock = np.arctan(c1m / (u1 - c1u))*180/np.pi
        return round(Beta1withoutBlock, 2)

    def inletBladeAngle(self, c1m, u1, D1, Z, e1, i=2, c1u=0):
        '''Calculation of the blade angle for inlet, arguments: c1m [m/s] - meridional axial component of velocity;
         u1 [m/s] - circumferential velocity for any diameter; D1 [mm] - suction diameter of impeller;
         Z - number of the blades; e1 [mm] - thickness of the blade inlet; i [degree] - incidence angle;
         c1u [m/s] - pre-swirl of the flow'''
        D1 = D1/1000.0
        e1 = e1/1000.0
        Beta1withoutBlock = np.arctan(c1m/(u1-c1u))
        tau1 = (1-Z*e1/(np.pi*D1*np.sin(Beta1withoutBlock)))**(-1)
        Beta1flow = np.arctan(c1m*tau1/(u1-c1u))*180/np.pi
        Beta1 = Beta1flow+i
        return round(Beta1, 2)

    # OUTLET VELOCITY TRIANGLE
    def u2(self, D2):
        '''Calculation U2 velocity for D2 [mm] and rotation speed - n [rev/min], returns U2 [m/s]'''
        D2 = D2/1000.0
        U2 = self.n * np.pi / 30 * D2 / 2
        return round(U2, 2)

    def c2m(self, D2, b2, volumeEfficiency=100):
        '''Calculation meridional axial component of velocity - c2m [m/s], arguments:'''
        volumeEfficiency = volumeEfficiency/100
        D2 = D2/1000.0
        b2 = b2/1000.0
        Qloss = self.Q - self.Q*volumeEfficiency
        Qfull = self.Q + Qloss
        A2 = np.pi*D2*b2
        c2m = Qfull/A2
        return round(c2m, 2)

    def c2u(self, hydraulicEff, u2, u1=0, c1u=0):
        '''Calculation circumferential component of absolute velocity - c2u [m/s], arguments:
        hydraulicEff [%] - hydraulic efficiency of the pump; u2 [m/s] - circumferential speed
        c1u [m/s] - pre-swirl of the flow'''
        hydraulicEff = hydraulicEff/100.0
        c2u = 9.80666*self.Hi/hydraulicEff/u2+u1*c1u/u2
        return round(c2u, 2)

    def outletFlowAngleRelative(self, c2m, c2u, u2, e2, Z, D2, Beta2):
        '''Calculation relative outlet angle without blockage - Beta2flow [degree], arguments:
        c2m [m/s] - meridional component of absolute velocity;
        c2u [m/s] - circumferential component of absolute velocity; u2 [m/s] - circumferential speed
        e2 [mm] - thickness trailing edge
        Z [-] - number of blades
        D2 [mm] - impeller diameter
        Beta2 [degree] - user's value of Beta2'''
        e2 = e2/1000.0
        D2 = D2/1000.0
        Beta2 = Beta2*np.pi/180.0
        w2u = u2-c2u
        tau2 = (1 - e2 * Z / (np.pi * D2 * np.sin(Beta2))) ** (-1)
        Beta2flow = np.arctan(c2m*tau2 / w2u) * 180 / np.pi
        return round(Beta2flow, 2)

    def impellerHead(self, c2m, u2, e2, Z, D2, hydraulicEff, Beta2):
        '''Calculation of the impeller pump head - H [m], arguments:
        c2m [m/s] - meridional component of absolute velocity;
        u2 [m/s] - circumferential speed; e2 [mm] - thickness trailing edge; Z [-] - number of blades
        D2 [mm] - impeller diameter; hydraulicEff [%] - hydraulic efficiency of the pump;
        Beta2 [degree] - user's value of Beta2'''
        e2 = e2/1000.0
        D2 = D2/1000.0
        Beta2 = Beta2*np.pi/180
        hydraulicEff = hydraulicEff/100.0+(1-(hydraulicEff/100.0))/2.0
        tau2 = (1 - e2 * Z / (np.pi * D2 * np.sin(Beta2))) ** (-1)
        gamma = 0.98 * (1 - np.sin(Beta2) ** 0.5 / Z ** 0.7)
        c2u_pred = u2 * (gamma - c2m * tau2 / (u2 * np.tan(Beta2)))
        Head = hydraulicEff*u2*c2u_pred/9.80666
        return round(Head, 2)

    def pumpHead(self, c2m, u2, e2, Z, D2, hydraulicEff, Beta2):
        '''Calculation of the impeller pump head - H [m], arguments:
        c2m [m/s] - meridional component of absolute velocity;
        u2 [m/s] - circumferential speed; e2 [mm] - thickness trailing edge; Z [-] - number of blades
        D2 [mm] - impeller diameter; hydraulicEff [%] - hydraulic efficiency of the pump;
        Beta2 [degree] - user's value of Beta2'''
        e2 = e2/1000.0
        D2 = D2/1000.0
        Beta2 = Beta2*np.pi/180
        hydraulicEff = hydraulicEff/100
        tau2 = (1 - e2 * Z / (np.pi * D2 * np.sin(Beta2))) ** (-1)
        gamma = 0.98 * (1 - np.sin(Beta2) ** 0.5 / Z ** 0.7)
        c2u_pred = u2 * (gamma - c2m * tau2 / (u2 * np.tan(Beta2)))
        Head = hydraulicEff*u2*c2u_pred/9.80666
        return round(Head, 2)

if __name__=='__main__':
    # Example of the impeller pump calculation
    Pump = PyPumpRadialImpeller(53, 5/3600, 2985, 1, 997)
    psi = Pump.psi(ft=1.00)
    D2 = Pump.D2(psi)
    b2 = Pump.b2(D2)
    Eff = Pump.EfficiencyRadialSingleStageSingeEntry()
    HydrEff = Pump.HydraulicEfficiencyRadialPumpSingleStage()
    Pm = Pump.Pmax(Eff)
    shaftD = Pump.shaftD(Pm)
    D1 = Pump.D1LambdaMethod(shaftD)
    c1m = Pump.c1m(D1=D1, shaftD=shaftD, volumeEfficiency=97)
    u1 = Pump.u1(96)
    e1 = Pump.bladeThickness(D2)
    Beta1 = Pump.inletBladeAngle(c1m=c1m,u1=u1, D1=D1, Z=6, e1=1.6, i=0)
    Beta1flow = Pump.inletFlowAngleRelative(c1m=c1m,u1=u1)
    w1 = Pump.w1(c1m, u1)
    c2m = Pump.c2m(D2, b2, volumeEfficiency=97)
    u2 = Pump.u2(D2)
    c2u = Pump.c2u(hydraulicEff=HydrEff, u2=u2)
    beta2flow = Pump.outletFlowAngleRelative(c2m=c2m, c2u=c2u, u2=u2, e2=15.9, D2=D2, Z=6, Beta2=25)
    pumpHead = Pump.pumpHead(c2m=c2m, u2=u2, e2=e1, D2=D2, Z=6, hydraulicEff=HydrEff, Beta2=20.53)
    impellerHead = Pump.impellerHead(c2m=c2m, u2=u2, e2=e1, D2=D2, Z=6, hydraulicEff=HydrEff, Beta2=20.53)
    print (HydrEff)
    print (D2)
    print (b2)
    print (shaftD)
    print (c2u)
