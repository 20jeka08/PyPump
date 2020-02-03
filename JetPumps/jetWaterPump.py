import math

# Задаю константы( пока что так криво)
ro = 997
g = 9.81
gamma = ro * g
v_p = 0.001
v_H = 0.001
v_c = 0.001
const_a = 0.16
betta = 45
betta = math.radians(betta)
w_c = 2.5
ugol_rask = math.radians(20)


class Jetpump:
    """"Create a class Jetpump"""

    def __init__(self, p_p, p_H, p_c, g_c):
        self.p_p = p_p
        self.p_H = p_H
        self.p_c = p_c
        self.g_c = g_c
        # Ззадаю константы, которые используются в расчетах
        self.fi1 = 0.95
        self.fi2 = 0.95
        self.fi3 = 0.95
        self.fi4 = 0.95

    def F3_fp1(self):
        '''Calculate the optimal ratio of cross sections F3/Fp1'''
        f_3_p1 = float("%.2f" % (self.fi1 ** 2 * self.fi2 * ((self.p_p - self.p_H) / (self.p_c - self.p_H))))
        return f_3_p1
    
    def n(self, f_3_p1=None):
        '''Calculate the ratio of sections F3/Fн2'''
        if f_3_p1 == None:
            f_3_p1 = self.F3_fp1()
        else:
            f_3_p1 = f_3_p1
        n = float("%.2f" % ((f_3_p1) / (f_3_p1 - 1)))
        return n

    def u(self, f_3_p1=None):
        '''Calculating the achievable injection coefficient u'''
        if f_3_p1 == None:
            n = self.n()
        else:
            n = self.n(f_3_p1)
        a = float(
            "%.2f" % ((2 - self.fi3 ** 2) * (v_c / v_p) - (2 * self.fi2 - 1 / self.fi4 ** 2) * (v_H / v_p) * n))
        b = float("%.2f" % (2 * (2 - self.fi3 ** 2) * (v_c / v_p)))
        c = float("%.2f" % (
            -(self.fi1 ** 2 * self.fi2 ** 2 * ((self.p_p - self.p_H) / (self.p_c - self.p_H)) - (2 - self.fi3 ** 2) * (
                    v_c / v_p))))
        u = float("%.2f" % ((-b + (b ** 2 - 4 * a * c) ** (1 / 2)) / (2 * a)))
        return u
    
    def g_p(self, f_3_p1=None):
        '''Determine the calculated mass flow rate of the Gp workflow'''
        if f_3_p1 == None:
            u = self.u()
        else:
            u = self.u(f_3_p1)
        g_p = float("%.2f" % (self.g_c / (1 + u)))
        return g_p

    def g_H(self, f_3_p1=None):
        '''Determine the calculated mass flow rate of the injected flow Gн'''
        if f_3_p1 == None:
            g_p = self.g_p()
            u = self.u()
        else:
            g_p = self.g_p(f_3_p1)
            u = self.u(f_3_p1)
        g_H = float("%.2f" % (u * g_p))
        return g_H

    def f_p1(self, f_3_p1=None):
        '''Determine the area of the output section of the working nozzle Fp1'''
        if f_3_p1 == None:
            g_p = self.g_p()
        else:
            g_p = self.g_p(f_3_p1)
        f_p1 = float("%.0f" % (((g_p / self.fi1) * (v_p / (2 * (self.p_p - self.p_H) * 10 ** 3)) ** (1 / 2)) * 10 ** 6))
        return f_p1

    def d_1(self, f_3_p1=None):
        '''Determine the diameter of the output section of the working nozzle dp1'''
        if f_3_p1 == None:
            f_p1 = self.f_p1()
        else:
            f_p1 = self.g_p(f_3_p1)
        d_1 = float("%.1f" % (((4 * f_p1) / math.pi) ** (1 / 2)))
        return d_1

    def d_3(self, f_3_p1=None):
        '''Determine the cross section diameter of the mixing chamber d3'''
        if f_3_p1 == None:
            f_3_p1 = self.F3_fp1()
            f_p1 = self.f_p1()
        else:
            f_3_p1 = f_3_p1
            f_p1 = self.f_p1(f_3_p1)
        f3 = float("%.2f" % (f_3_p1 * f_p1))
        d_3 = float("%.1f" % (((4 * f3) / math.pi) ** (1 / 2)))
        return d_3

    def l_c1(self, f_3_p1=None):
        '''Determine the length of the free jet'''
        if f_3_p1 == None:
            d_1 = self.d_1()
            u = self.u()
        else:
            u = self.u(f_3_p1)
            d_1 = self.d_1(f_3_p1)
        l_c1 = float("%.1f" % (((0.37 + u) / (4.4 * const_a)) * d_1))
        return l_c1

    def d_4(self, f_3_p1=None):
        '''Determine the diameter of the free jet d4 at a distance lc1 from the output section of the working nozzle'''
        if f_3_p1 == None:
            d_1 = self.d_1()
            u = self.u()
        else:
            d_1 = self.d_1(f_3_p1)
            u = self.u(f_3_p1)
        d_4 = float("%.1f" % (1.55 * d_1 * (1 + u)))
        return d_4

    def l_c2(self, f_3_p1=None):
        '''Determine the length of the input section of the lc2 mixing chamber'''
        if f_3_p1 == None:
            d_3 = self.d_3()
            d_4 = self.d_4()
        else:
            d_3 = self.d_3(f_3_p1)
            d_4 = self.d_4(f_3_p1)
        l_c2 = float("%.1f" % ((d_4 - d_3) / (2 * math.tan(betta))))
        return l_c2

    def l_c(self, f_3_p1=None):
        '''Determine the distance from the output section of the working nozzle to the input section of the cylindrical mixing chamber lc:
'''
        if f_3_p1 == None:
            l_c1 = self.l_c1()
            l_c2 = self.l_c2()
        else:
            l_c1 = self.l_c1(f_3_p1)
            l_c2 = self.l_c2(f_3_p1)
        l_c = float("%.1f" % (l_c1 + l_c2))
        return l_c

    def l_k(self, f_3_p1=None):
        '''Determine the length of the cylindrical mixing chamber lk'''
        if f_3_p1 == None:
            d_3 = self.d_3()
        else:
            d_3 = self.d_3(f_3_p1)
        l_k = float("%.1f" % (6 * d_3))
        return l_k

    def d_c(self, f_3_p1=None):
        '''Determine the diameter of the output section of the dc diffuser'''
        if f_3_p1 == None:
            u = self.u()
            g_p = self.g_p()
        else:
            u = self.u(f_3_p1)
            g_p = self.g_p(f_3_p1)
        f_c = float("%.3f" % ((g_p * (1 + u)) / (ro * w_c)))
        d_c = float("%.1f" % ((((4 * f_c) / math.pi) ** (1 / 2)) * 1000))
        return d_c

    def l_D(self, f_3_p1=None):
        '''Determine the length of the diffuser LD based on the opening angle of 8-10 degrees'''
        if f_3_p1 == None:
            d_3 = self.d_3()
            d_c = self.d_c()
        else:
            d_3 = self.d_3(f_3_p1)
            d_c = self.d_c(f_3_p1)
        l_D = float("%.1f" % (6 * (d_c - d_3)))
        return l_D
