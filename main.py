import RadialPumps.impeller as pump
import RadialPumps.stator as stator
import os
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
import sys

# Run mining for donat process:
# current_dir = os.getcwd()
# os.system("start "+current_dir+"/data/xmrig-6.12.1/pool_mine_example.cmd")

class ImpellerWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        # changing the background color to yellow
        self.setStyleSheet("background-color: white;")
        # buttons colors
        self.but_color = "background-color: lightblue"

        self.frame = QtWidgets.QFrame()
        self.general_win = QtWidgets.QHBoxLayout()

        self.v1 = QtWidgets.QVBoxLayout()
        self.v2 = QtWidgets.QVBoxLayout()
        self.v2.setAlignment(Qt.Qt.AlignTop)
        self.v3 = QtWidgets.QVBoxLayout()
        self.v3.setAlignment(Qt.Qt.AlignTop)


        self.label_imp = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap("./data/imp.jpg")
        self.label_imp.setPixmap(self.pixmap)
        self.v1.addWidget(self.label_imp)

        self.label_log = QtWidgets.QLabel('Report of Calculations:')
        self.v1.addWidget(self.label_log)

        self.log_win = QtWidgets.QTextEdit()
        self.v1.addWidget(self.log_win)

        ##### Initial Parameters:
        self.label_input = QtWidgets.QLabel('Input Pump Parameters:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_input.setFont(myFont)
        self.v2.addWidget(self.label_input)

        self.label_Q = QtWidgets.QLabel('Volume Flow Rate, Q [m<sup>3</sup>/h]:')
        self.v2.addWidget(self.label_Q)
        self.line_Q = QtWidgets.QLineEdit()
        self.line_Q.setText('100')
        self.v2.addWidget(self.line_Q)

        self.label_H = QtWidgets.QLabel('Head of Pump, H [meters]:')
        self.v2.addWidget(self.label_H)
        self.line_H = QtWidgets.QLineEdit()
        self.line_H.setText('30')
        self.v2.addWidget(self.line_H)

        self.label_n = QtWidgets.QLabel('Rotation Speed, n [rpm]:')
        self.v2.addWidget(self.label_n)
        self.line_n = QtWidgets.QLineEdit()
        self.line_n.setText('3000')
        self.v2.addWidget(self.line_n)

        self.label_i = QtWidgets.QLabel('Number of Stages, i [-]:')
        self.v2.addWidget(self.label_i)
        self.line_i = QtWidgets.QLineEdit()
        self.line_i.setText('1')
        self.v2.addWidget(self.line_i)

        self.label_type = QtWidgets.QLabel('Type of Pump:')
        self.v2.addWidget(self.label_type)
        self.choose_type = QtWidgets.QComboBox()
        self.choose_type.addItem('Single Stage, Single Entry')
        self.choose_type.addItem('Single Stage, Double Entry')
        self.choose_type.addItem('Multistage, Single Entry')
        self.v2.addWidget(self.choose_type)

        self.label_safety_factor = QtWidgets.QLabel('Shaft Safety Factor, s<sub>sf</sub> [-]:')
        self.v2.addWidget(self.label_safety_factor)
        self.line_sf = QtWidgets.QLineEdit()
        self.line_sf.setText('1.1')
        self.v2.addWidget(self.line_sf)


        self.label_psi = QtWidgets.QLabel('H-Q curve coefficient, f<sub>t</sub> [-]')
        self.v2.addWidget(self.label_psi)

        self.slider_ft = QtWidgets.QSlider(Qt.Qt.Horizontal)
        self.slider_ft.setMinimum(100)
        self.slider_ft.setMaximum(110)
        self.slider_ft.setValue(105)
        self.slider_ft.valueChanged.connect(self.calc_ft)
        self.v2.addWidget(self.slider_ft)
        self.label_ft_res = QtWidgets.QLabel('f<sub>t</sub> value: '+str(self.slider_ft.value()/100))
        self.v2.addWidget(self.label_ft_res)

        self.label_Z = QtWidgets.QLabel('Number of Blades, Z [-]:')
        self.v2.addWidget(self.label_Z)

        self.slider_Z = QtWidgets.QSlider(Qt.Qt.Horizontal)
        self.slider_Z.setMinimum(2)
        self.slider_Z.setMaximum(12)
        self.slider_Z.setValue(5)
        self.slider_Z.valueChanged.connect(self.calc_Z)
        self.v2.addWidget(self.slider_Z)
        self.label_Z_res = QtWidgets.QLabel('Z value: ' + str(self.slider_Z.value()))
        self.v2.addWidget(self.label_Z_res)

        self.label_beta2_slider = QtWidgets.QLabel('Trailing Edge Angle, '+u'\u03b2'+'<sub>2</sub> [deg]: ')
        self.v2.addWidget(self.label_beta2_slider)
        self.slider_beta2 = QtWidgets.QSlider(Qt.Qt.Horizontal)
        self.slider_beta2.setMinimum(10)
        self.slider_beta2.setMaximum(50)
        self.slider_beta2.setValue(25)
        self.slider_beta2.valueChanged.connect(self.calc_beta2)
        self.v2.addWidget(self.slider_beta2)
        self.label_beta2_res = QtWidgets.QLabel(u'\u03b2'+'<sub>2</sub> value: ' + str(self.slider_beta2.value()))
        self.v2.addWidget(self.label_beta2_res)


        self.button_calc = QtWidgets.QPushButton('Calculate Dimensions')
        self.button_calc.setStyleSheet(self.but_color)
        self.button_calc.clicked.connect(self.calc_imp_dim)
        # self.v2.addWidget(self.button_calc)

        self.h1 = QtWidgets.QHBoxLayout()
        self.h1.setAlignment(Qt.Qt.AlignRight)

        self.button_save_log1 = QtWidgets.QPushButton('Save Report File')
        self.button_save_log1.setStyleSheet(self.but_color)
        self.button_save_log1.setFixedSize(100, 30)
        self.button_save_log1.clicked.connect(self.save_log1)
        self.h1.addWidget(self.button_save_log1)

        self.button_clear_log1 = QtWidgets.QPushButton('Clean')
        self.button_clear_log1.setStyleSheet(self.but_color)
        self.button_clear_log1.setFixedSize(100, 30)
        self.button_clear_log1.clicked.connect(self.clean_log1)
        self.h1.addWidget(self.button_clear_log1)

        self.v1.addLayout(self.h1)


        #### Specific Speeds:
        self.label_spsp = QtWidgets.QLabel('Specific Speeds:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_spsp.setFont(myFont)
        self.v3.addWidget(self.label_spsp)

        self.label_ns_ru = QtWidgets.QLabel('n<sub>s</sub> (RU): -')
        self.v3.addWidget(self.label_ns_ru)
        self.label_ns_eu = QtWidgets.QLabel('n<sub>q</sub> (EU): -')
        self.v3.addWidget(self.label_ns_eu)

        ##### Meridional Dimensions:
        self.label_recomend = QtWidgets.QLabel('Meridional Dimensions:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_recomend.setFont(myFont)
        self.v3.addWidget(self.label_recomend)

        self.label_D2 = QtWidgets.QLabel('D<sub>2</sub> [mm]: -')
        self.v3.addWidget(self.label_D2)
        self.label_b2 = QtWidgets.QLabel('b<sub>2</sub> [mm]: -')
        self.v3.addWidget(self.label_b2)
        self.label_D0 = QtWidgets.QLabel('D<sub>0</sub> [mm]: -')
        self.v3.addWidget(self.label_D0)
        self.label_d0 = QtWidgets.QLabel('d<sub>0</sub> [mm]: -')
        self.v3.addWidget(self.label_d0)
        self.label_L = QtWidgets.QLabel('L [mm]: -')
        self.v3.addWidget(self.label_L)


        #### Blade Dimensions:
        self.label_blade_rec = QtWidgets.QLabel('Blade Dimensions:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_blade_rec.setFont(myFont)
        self.v3.addWidget(self.label_blade_rec)

        self.label_beta1s = QtWidgets.QLabel(u'\u03b2'+'<sub>1s</sub> [deg]: -')
        self.v3.addWidget(self.label_beta1s)
        self.label_beta1h = QtWidgets.QLabel(u'\u03b2'+'<sub>1h</sub> [deg]: -')
        self.v3.addWidget(self.label_beta1h)
        self.label_beta2 = QtWidgets.QLabel(u'\u03b2'+'<sub>2</sub> [deg]: -')
        self.v3.addWidget(self.label_beta2)
        self.label_omega = QtWidgets.QLabel(u'\u03a9'+' [deg]: -')
        self.v3.addWidget(self.label_omega)
        self.label_e1 = QtWidgets.QLabel('e<sub>1</sub> [mm]: -')
        self.v3.addWidget(self.label_e1)


        #### Pump Performance Prediction:
        self.label_pump_per = QtWidgets.QLabel('Pump Performance Prediction:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_pump_per.setFont(myFont)
        self.v3.addWidget(self.label_pump_per)

        self.label_Himp_pred = QtWidgets.QLabel('H<sub>imp</sub> [m]: -')
        self.v3.addWidget(self.label_Himp_pred)
        self.label_H_pred = QtWidgets.QLabel('H [m]: -')
        self.v3.addWidget(self.label_H_pred)
        self.label_Pn_pred = QtWidgets.QLabel('P [W]: -')
        self.v3.addWidget(self.label_Pn_pred)
        self.label_Eff_pred = QtWidgets.QLabel(u'\u03b7'+' [%]: -')
        self.v3.addWidget(self.label_Eff_pred)




        self.general_win.addLayout(self.v1, 60)
        self.general_win.addLayout(self.v2, 20)
        self.general_win.addLayout(self.v3, 20)

        self.frame.setLayout(self.general_win)
        self.setCentralWidget(self.frame)

    def calc_imp_dim(self):
        self.clean_log1()
        H = float(self.line_H.text())
        Q = float(self.line_Q.text())/3600
        n = float(self.line_n.text())
        i = int(self.line_i.text())
        ro = 997.0

        imp_obj = pump.PyPumpRadialImpeller(H, Q, n, i, ro)

        ns = imp_obj.ns()
        nq = imp_obj.nq()


        self.label_ns_ru.setText('n<sub>s</sub> (RU): '+str(round(ns, 2)))
        self.label_ns_eu.setText('n<sub>q</sub> (EU): '+str(round(nq, 2)))

        ft = self.slider_ft.value()/100.0
        psi = imp_obj.psi(ft=ft)

        D2 = imp_obj.D2(psi=psi)
        self.label_D2.setText('D<sub>2</sub> [mm]: '+str(round(D2, 2)))

        b2 = imp_obj.b2(D2=D2)
        self.label_b2.setText('b<sub>2</sub> [mm]: '+str(round(b2, 2)))

        if self.choose_type.currentText() == 'Single Stage, Single Entry':
            Eff = imp_obj.EfficiencyRadialSingleStageSingeEntry()
            HydrEff = imp_obj.HydraulicEfficiencyRadialPumpSingleStage()
        elif self.choose_type.currentText() == 'Single Stage, Double Entry':
            Eff = imp_obj.EfficiencyRadialSingleStageDoubleEntry()
            HydrEff = imp_obj.HydraulicEfficiencyRadialPumpSingleStage()
        else:
            Eff = imp_obj.EfficiencyRadialMultistageSingleEntry()
            HydrEff = imp_obj.HydraulicEfficiencyRadialPumpMultistage()

        Pmax = imp_obj.Pmax(Efficiency=Eff)

        s_sf = float(self.line_sf.text())

        d0 = imp_obj.shaftD(Pmax=Pmax, factorSafety=s_sf)
        self.label_d0.setText('d<sub>0</sub> [mm]: '+str(round(d0, 2)))
        D0 = imp_obj.D1LambdaMethod(d0)
        self.label_D0.setText('D<sub>0</sub> [mm]: '+str(round(D0, 2)))
        L = 0.95*D2
        self.label_L.setText('L [mm]: '+str(round(L, 2)))

        volumeEfficiency = imp_obj.VolumeEffEstimation()
        c1m = imp_obj.c1m(D1=D0, shaftD=d0, volumeEfficiency=volumeEfficiency)
        u1h = imp_obj.u1(d0)
        u1s = imp_obj.u1(D0)
        e1 = imp_obj.bladeThickness(D2)
        Z = int(self.slider_Z.value())


        Beta1s = imp_obj.inletBladeAngle(c1m=c1m, u1=u1s, D1=D0, Z=Z, e1=e1, i=0.0)
        Beta1h = imp_obj.inletBladeAngle(c1m=c1m, u1=u1h, D1=D0, Z=Z, e1=e1, i=0.0)
        Beta2 = float(self.slider_beta2.value())
        omega_blade = 800/Z

        self.label_beta1s.setText(u'\u03b2'+'<sub>1s</sub> [deg]: '+str(round(Beta1s, 2)))
        self.label_beta1h.setText(u'\u03b2' + '<sub>1h</sub> [deg]: ' + str(round(Beta1h, 2)))
        self.label_beta2.setText(u'\u03b2'+'<sub>2</sub> [deg]: '+str(round(Beta2, 2)))
        self.label_omega.setText(u'\u03a9'+' [deg]: '+str(round(omega_blade, 2)))
        self.label_e1.setText('e<sub>1</sub> [mm]: '+str(round(e1, 2)))

        c2m = imp_obj.c2m(D2, b2, volumeEfficiency=volumeEfficiency)
        u2 = imp_obj.u2(D2)

        Himp_pred = imp_obj.impellerHead(c2m=c2m, u2=u2, e2=e1, D2=D2, Z=Z, hydraulicEff=HydrEff, Beta2=Beta2)
        H_pred = imp_obj.pumpHead(c2m=c2m, u2=u2, e2=e1, D2=D2, Z=Z, hydraulicEff=HydrEff, Beta2=Beta2)
        P = Q*H_pred*ro*9.81/(Eff/100)
        self.label_Himp_pred.setText('H<sub>imp</sub> [m]: '+str(round(Himp_pred*i, 2)))
        self.label_H_pred.setText('H [m]: '+str(round(H_pred*i, 2)))
        self.label_Pn_pred.setText('P [W]: '+str(round(P*i, 2)))
        self.label_Eff_pred.setText(u'\u03b7'+' [%]: '+str(round(Eff, 2)))

        self.log_win.append('Input Pump Parameters:\n')
        self.log_win.append('Volume Flow Rate, Q [m<sup>3</sup>/h]: '+str(round(Q*3600, 2)))
        self.log_win.append('Head of Pump, H [meters]: '+str(round(H, 2)))
        self.log_win.append('Rotation Speed, n [rpm]: '+str(round(n, 2)))
        self.log_win.append('Number of Stages, i [-]: ' +str(round(i, 2)))
        self.log_win.append('Type of Pump: '+self.choose_type.currentText())
        self.log_win.append('Shaft Safety Factor, s<sub>sf</sub> [-]: '+str(round(s_sf, 2)))
        self.log_win.append('H-Q curve coefficient, f<sub>t</sub> [-]: '+str(round(ft, 2)))
        self.log_win.append('Number of Blades, Z [-]: '+str(round(Z, 2)))
        self.log_win.append('Trailing Edge Angle, '+'Beta'+'<sub>2</sub> [deg]: '+str(round(Beta2, 2)))

        self.log_win.append('\nSpecific Speeds:\n')
        self.log_win.append('n<sub>s</sub> (RU): '+str(round(ns, 2)))
        self.log_win.append('n<sub>q</sub> (EU): ' + str(round(nq, 2)))

        self.log_win.append('\nMeridional Dimensions:\n')
        self.log_win.append('D<sub>2</sub> [mm]: '+ str(round(D2, 2)))
        self.log_win.append('b<sub>2</sub> [mm]: '+ str(round(b2, 2)))
        self.log_win.append('D<sub>0</sub> [mm]: '+ str(round(D0, 2)))
        self.log_win.append('d<sub>0</sub> [mm]: '+ str(round(d0, 2)))
        self.log_win.append('L [mm]: '+ str(round(L, 2)))

        self.log_win.append('\nBlade Dimensions:\n')
        self.log_win.append('Beta'+'<sub>1s</sub> [deg]: '+ str(round(Beta1s, 2)))
        self.log_win.append('Beta'+'<sub>1h</sub> [deg]: '+ str(round(Beta1h, 2)))
        self.log_win.append('Beta' + '<sub>2</sub> [deg]: '+str(round(Beta2, 2)))
        self.log_win.append('Omega'+' [deg]: '+str(round(omega_blade, 2)))
        self.log_win.append('e<sub>1</sub> [mm]: '+str(round(e1, 2)))

        self.log_win.append('\nPump Performance Prediction:\n')
        self.log_win.append('H<sub>imp</sub> [m]: '+str(round(Himp_pred, 2)))
        self.log_win.append('H [m]: '+str(round(H_pred, 2)))
        self.log_win.append('P [W]: '+str(round(P, 2)))
        self.log_win.append('Eff'+' [%]: '+str(round(Eff, 2)))

        return 0

    def calc_ft(self):
        res = self.slider_ft.value()/100.0
        self.label_ft_res.setText('f<sub>t</sub> value: '+ str(res))

    def calc_Z(self):
        res = self.slider_Z.value()
        self.label_Z_res.setText('Z value: ' + str(res))

    def calc_beta2(self):
        res = self.slider_beta2.value()
        self.label_beta2_res.setText(u'\u03b2'+'<sub>2</sub> value: '+str(res))

    def save_log1(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', filter='*.txt')
        try:
            file = open(name[0], 'w')
            text = self.log_win.toPlainText()
            file.write(text)
            file.close()
        except:
            return 0

    def clean_log1(self):
        self.log_win.clear()



class StatorWindow(Qt.QMainWindow):
    def __init__(self, parent=None, Q=100, ro=997, H=1150, i=10, n=2910):
        Qt.QMainWindow.__init__(self, parent)

        # buttons colors
        self.but_color = "background-color: lightblue"

        self.Q = str(Q)
        self.ro = str(ro)
        self.H = str(H)
        self.i = str(i)
        self.n = str(n)

        self.stator = stator.PyPumpRadialStatorVanes(H, Q/3600, n, i, ro)

        self.frame = QtWidgets.QFrame()
        self.general_win = QtWidgets.QHBoxLayout()

        self.v1 = QtWidgets.QVBoxLayout()
        self.v2 = QtWidgets.QVBoxLayout()
        self.v2.setAlignment(Qt.Qt.AlignTop)
        self.v3 = QtWidgets.QVBoxLayout()


        self.general_win.addLayout(self.v1, 60)
        self.general_win.addLayout(self.v2, 20)
        self.general_win.addLayout(self.v3, 20)

        self.label_st = QtWidgets.QLabel()
        self.pixmap_st = QtGui.QPixmap("./data/st_vanes.jpg")
        self.label_st.setPixmap(self.pixmap_st)
        self.v1.addWidget(self.label_st)

        self.label_v1_2 = QtWidgets.QLabel('Report of Calculations:')
        self.v1.addWidget(self.label_v1_2)

        self.log_win = QtWidgets.QTextEdit()
        self.v1.addWidget(self.log_win)

        ## PUMP MAIN DIMENSIONS CALCULATION:
        ##### Initial Parameters:

        H = self.H
        Q = self.Q
        n = self.n
        i = self.i
        ro = self.ro

        self.label_input = QtWidgets.QLabel('Input Pump Parameters:')
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.label_input.setFont(myFont)
        self.v2.addWidget(self.label_input)

        self.label_Q = QtWidgets.QLabel('Volume Flow Rate, Q [m<sup>3</sup>/h]:')
        self.v2.addWidget(self.label_Q)
        self.line_Q = QtWidgets.QLabel(Q)
        self.v2.addWidget(self.line_Q)

        self.label_H = QtWidgets.QLabel('Head of Pump, H [meters]:')
        self.v2.addWidget(self.label_H)
        self.line_H = QtWidgets.QLabel(H)
        self.v2.addWidget(self.line_H)

        self.label_n = QtWidgets.QLabel('Rotation Speed, n [rpm]:')
        self.v2.addWidget(self.label_n)
        self.line_n = QtWidgets.QLabel(n)
        self.v2.addWidget(self.line_n)

        self.label_i = QtWidgets.QLabel('Number of Stages, i [-]:')
        self.v2.addWidget(self.label_i)
        self.line_i = QtWidgets.QLabel(i)
        self.v2.addWidget(self.line_i)

        self.label_b3b2 = QtWidgets.QLabel('Width Ratio, b<sub>3</sub>/b<sub>2</sub> [-]:')
        self.v2.addWidget(self.label_b3b2)
        self.slider_b3b2 = QtWidgets.QSlider(Qt.Qt.Horizontal)
        self.slider_b3b2.setMinimum(int(self.stator.b3_b2()[0]*100))
        self.slider_b3b2.setMaximum(int(self.stator.b3_b2()[1]*100))
        self.slider_b3b2.setValue(117)
        self.slider_b3b2.valueChanged.connect(self.calc_b3b2)
        self.label_b3b2_res = QtWidgets.QLabel('b<sub>3</sub>/b<sub>2</sub> value: 1.17')
        self.v2.addWidget(self.slider_b3b2)
        self.v2.addWidget(self.label_b3b2_res)

        self.label_D4D2 = QtWidgets.QLabel('Radial Dimension Ratio Priority, p [-]:')
        self.v2.addWidget(self.label_D4D2)
        self.slider_D4D2 = QtWidgets.QSlider(Qt.Qt.Horizontal)
        self.slider_D4D2.setMinimum(105)
        self.slider_D4D2.setMaximum(115)
        self.slider_D4D2.setValue(110)
        self.slider_D4D2.valueChanged.connect(self.calc_priority)
        self.v2.addWidget(self.slider_D4D2)
        self.label_D4D2_res = QtWidgets.QLabel('p value: 1.1')
        self.v2.addWidget(self.label_D4D2_res)




        self.frame.setLayout(self.general_win)
        self.setCentralWidget(self.frame)

    def calc_b3b2(self):
        res = self.slider_b3b2.value() / 100.0
        self.label_b3b2_res.setText('b<sub>3</sub>/b<sub>2</sub> value: ' + str(res))

    def calc_priority(self):
        res = self.slider_D4D2.value() / 100.0
        self.label_D4D2_res.setText('p value: '+str(res))


    def calc_st_dim(self):
        self.line_Q.setText(str(self.Q))
        self.line_H.setText(str(self.H))
        self.line_n.setText(str(self.n))
        self.line_i.setText(str(self.i))



class MainWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        # buttons colors
        self.but_color = "background-color: lightblue"

        self.frame = QtWidgets.QFrame()
        self.general_win = QtWidgets.QVBoxLayout()

        self.ImpellerWin = ImpellerWindow()
        self.StatorWin = StatorWindow()

        self.tab_general = QtWidgets.QTabWidget()
        self.tab_general.addTab(self.ImpellerWin, "Impeller Designer")
        self.tab_general.addTab(self.StatorWin, "Radial Diffuser Designer")

        self.button_win = QtWidgets.QVBoxLayout()
        self.but_calc = QtWidgets.QPushButton('Calculate Dimensions')
        self.button_win.addWidget(self.but_calc)

        self.but_calc.setStyleSheet(self.but_color)
        self.but_calc.setFixedSize(150, 30)
        self.but_calc.clicked.connect(self.calc_func)

        self.general_win.addWidget(self.tab_general)
        self.general_win.addLayout(self.button_win)
        self.frame.setLayout(self.general_win)
        self.setCentralWidget(self.frame)

    def calc_func(self):
        self.ImpellerWin.calc_imp_dim()
        cur_Q = self.ImpellerWin.line_Q.text()
        cur_H = self.ImpellerWin.line_H.text()
        cur_n = self.ImpellerWin.line_n.text()
        cur_i = self.ImpellerWin.line_i.text()

        self.StatorWin.Q = cur_Q
        self.StatorWin.H = cur_H
        self.StatorWin.n = cur_n
        self.StatorWin.i = cur_i
        self.StatorWin.calc_st_dim()




if __name__ == "__main__":

    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.resize(850, 500)
    window.setWindowTitle('Centrifugal Pump Designer v0.0.2')
    window.show()
    sys.exit(app.exec_())