import numpy as np

class PyPumpInducer():
    def __init__(self, H, Q, n, ro):
        self.H = H
        self.Q = Q/3600.0
        self.n = n
        self.ro = ro

    def ns(self):
        '''Specific speed of the inducer (RU)'''
        ns = 3.65*self.n*(np.sqrt(self.Q)/(self.H**0.75))
        return round(ns, 2)

    def nq(self):
        '''Specific speed of the inducer (EU)'''
        nq = self.n * (np.sqrt(self.Q) / (self.H ** 0.75))
        return round(nq, 2)

    def D1opt(self, lambdaC=1.1, lambdaW=0.05, nu=0.5):
        '''Optimal inducer inlet diameter - D1 [mm]. Arguments:
        lambdaW [-] - range 0.02 - 0.08, default value is mean 0.05;
        lambdaC [-] - range 1.0 - 1.1, default value is 1.1;
        nu [-] - hub ratio (d_hub/D1), range 0.1 - 0.8;'''
        kn = 1-nu**2
        D1 = 3.25*(self.Q/self.n/kn)**(1/3)*((lambdaC+lambdaW)/lambdaW)**(1/6)*1000.0
        return round(D1, 2)

    def phi1opt(self, lambdaC=1.1, lambdaW=0.05):
        '''Optimum flow coefficient for given lambdaW, phi'''
        phi1opt = np.sqrt(lambdaW/(2*(lambdaC+lambdaW)))
        return round(phi1opt, 4)

    def nss(self, lambdaC=1.1, lambdaW=0.05, nu=0.5):
        '''Suction specific speed - nss. Arguments:
        lambdaW [-] - range 0.02 - 0.08, default value is mean 0.05;
        lambdaC [-] - range 1.0 - 1.1, default value is 1.1;
        nu [-] - hub ratio (d_hub/D1), range 0.1 - 0.8;'''
        kn = 1 - nu ** 2
        nss = 98/(lambdaW+lambdaC)**0.25*(kn/lambdaW)**0.5
        return round(nss, 2)

    def NPSH(self, nss):
        '''Calculation NPSH [m]'''
        NPSH = (self.n*np.sqrt(self.Q)/nss)**(4/3)
        return round(NPSH, 2)

    def phi(self, nss):
        '''Flow coefficient - phi, for calculated nss (suction specific speed)'''
        phi = (52.0/nss)**0.93
        return round(phi, 4)

    def inletflowAngleShroud(self, phi):
        '''Calculation of the flow inlet angle - flowInletAngleShroud [degree], based on phi'''
        Beta1flow = np.arctan(phi)*180.0/np.pi
        return round(Beta1flow, 2)

    def inletBladeAngleShroud(self, inletFlowAngleShroud, incidenceCoef = 1.65):
        '''Calculation of the inlet blade angle - inletBlabeAngleShroud [degree]. Arguments:
        Inlet flow angle on the shroud streamline - inletFlowAngleShroud [degree]
        Coefficient for inletBladeAngleShroud calcuolation - incidenceCoef [-], range 1.5-1.8'''
        Beta1 = incidenceCoef*inletFlowAngleShroud
        return round(Beta1, 2)

    def inletBladeAngleArray(self, R_array, D1, inletBladeAngleShroud):
        '''Calculation of the inletBladeAngleTable'''
        R = D1/2.0
        inletBladeAngleShroud = inletBladeAngleShroud*np.pi/180.0
        inletBladeAngleArray = np.arctan(R/R_array*np.tan(inletBladeAngleShroud))*180.0/np.pi
        return inletBladeAngleArray

    def pitch(self, R_array, Z):
        '''Calculation of the pitch - pitch [mm]. Arguments:
        R_array [mm] - array of radius values from hub to shroud
        Z [-] - number of blades'''
        t = np.pi*R_array/Z
        return t

    def bladeMeridionalLength(self, t, Lt_array=1.75):
        '''Calculation blade length in the meridional plane for different t(R) [mm], user can change the L/t
        recomended value: 1 < L/t < 2.5, default value is 1.75 for all radius streamlines'''
        L = Lt_array*t
        return L

    def hydraulicEff(self, L, t):
        '''Calculation of the hydraulic efficiency of the inducer - hydraulicEff [%]. Arguments:
        L [mm] - blade length in the meridional plane, array;
        t [mm] - pitch'''
        Lt = L/t
        Eff = (1-0.11*(Lt.mean()))*100
        return round(Eff, 2)

    def outletFlowAngle(self, Beta1_array, Beta2_array, t, L):
        '''Calculation outlet flow angle for determenation of the inducer head'''
        delta2 = (2+(Beta2_array-Beta1_array)/3)*(t/L)**(1/3)
        Beta2flow = Beta2_array-delta2
        return Beta2flow

    def staticHead(self, phi, hydraulicEff, D1, nu_inlet, nu_outlet, Beta2_flow):
        '''Calculation static head of the inducer. Arguments:
        phi [-] - flow coefficient; hydraulicEff [%] - hudraulic efficiency of inducer;
        D1 [mm] - inducer diameter; nu_inlet [-] - hub ratio Dh/D1 on the inlet side;
        nu_outlet [-] - hub ratio Dh/D1 on the outlet side; Beta2_flow [degree] - angle of the flow on outlet side'''
        D1 = D1/1000.0
        A1 = np.pi*D1**2/4-np.pi*(D1*nu_inlet)**2/4
        A2 = np.pi*D1**2/4-np.pi*(D1*nu_outlet)**2/4
        U2 = self.n * np.pi / 30 * D1 / 2
        Beta2mean = Beta2_flow.mean()*np.pi/180
        hydraulicEff = hydraulicEff/100.0
        staticPsi = hydraulicEff*(1-phi**2*(A1**2/(A2**2*np.sin(Beta2mean)**2-1)))
        Hp = staticPsi*U2**2/(2*9.80665)
        return round(Hp, 2)



    # Velocity triangle
    def cm(self, D1, shaftD, volumeEfficiency=100):
        '''Calculation of the meridional axial component of the flow velocity - cm [m/s], arguments:
        D1 [mm] - suction diameter of impeller, shaftD [mm] - diameter of the hub, volumeEfficiency [%] -
        volume efficiency of the pump'''
        volumeEfficiency = volumeEfficiency/100
        D1 = D1/1000.0
        shaftD = shaftD/1000.0
        Qloss = self.Q - self.Q*volumeEfficiency
        Qfull = self.Q + Qloss
        cm = 4*Qfull/(np.pi*(D1**2-shaftD**2))
        return cm

    def u(self, R_array):
        '''Calculation U1 velocity for any D [mm] and rotation speed - n [rev/min], returns u1 [m/s]'''
        R_array = 2.0*R_array/1000.0
        u = self.n * np.pi / 30 * R_array / 2
        return u

    def w(self, cm, u, cu=0):
        '''Calculation relative velocity for inlet - w [m/s], arguments:
        cm [m/s] - meridional axial component of velocity; u [m/s] - circumferential velocity for any diameter;
        cu [m/s] - pre-swirl of the flow'''
        w = np.sqrt(cm**2+(u-cu)**2)
        return w


if __name__=='__main__':
    # Example fo the inducer calculation
    Inducer = PyPumpInducer(1.0, 5.17, 2910, 997)
    ns = Inducer.ns()
    lambdaW = 0.35
    lambdaC = 1.0
    nu = 0.698
    Z = 5
    D1 = Inducer.D1opt(lambdaC, lambdaW, nu)
    Dh = nu*D1
    phi1opt = Inducer.phi1opt(lambdaC, lambdaW)
    nss = Inducer.nss(lambdaC, lambdaW, nu)
    NPSH = Inducer.NPSH(nss)
    phi = Inducer.phi(nss)
    Beta1flow = Inducer.inletflowAngleShroud(phi1opt)
    Beta1 = Inducer.inletBladeAngleShroud(Beta1flow, incidenceCoef=1.5)
    R_array = np.linspace(nu*D1/2.0, D1/2.0, 3)
    inletBladeAngleArray = Inducer.inletBladeAngleArray(R_array, D1, Beta1)
    t = Inducer.pitch(R_array, Z)
    L = Inducer.bladeMeridionalLength(t, Lt_array=2.0)
    Beta2AngleArray = inletBladeAngleArray+np.array([5.0, 5.0, 5.0])
    Beta2flow = Inducer.outletFlowAngle(inletBladeAngleArray, Beta2AngleArray, t, L)
    Eff = Inducer.hydraulicEff(L, t)
    staticH = Inducer.staticHead(phi, Eff, D1, nu, nu, Beta2flow)
    u = Inducer.u(R_array)
    cm = Inducer.cm(D1 = D1, shaftD=Dh)
    w = Inducer.w(cm=cm, u=u)

    print('Specific speed: ', ns)
    print('nss: ', nss)
    print('NPSH: ', NPSH)
    print('Flow coefficient: ', phi)
    print('Diameter inducer: ', D1)
    print('Hub diameter: ', Dh)
    print('Inlet flow angles shroud: ', Beta1flow)
    print('Ínlet blade angle shroud: ', Beta1)
    print('Radius streamlines: ', R_array)
    print('Meridional Inducer length: ', L)
    print('Pitch t: ', t)
    print('Inlet blade angles: ', inletBladeAngleArray)
    print('Outlet blade angles: ', Beta2AngleArray)
    print('Outlet flow angles: ', Beta2flow)
    print('Static head [meters]: ', staticH)
    print('Efficiency [%]: ', Eff)
    print('U [m/s]: ', u)
    print('Cm [m/s]: ', cm)
    print('W [m/s]: ', w)
