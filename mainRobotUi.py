from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import serial.tools.list_ports
import time
import g2
import Stt
import json
import R

class MyThread(QThread):
    # bien data
    data = pyqtSignal(str)
    # bien ngat cua vong lap while
    STT = 1
    # ham duoc chay khi goi self.start()
    def run(self):
        try:
            g2.open()
            w.lb_stt_com.setText(g2.s.port + " connect OK")
            g2.send('$sv=2')
            g2.send('g54')
            time.sleep(1)
            g2.send('$sv=1')
            g2.send('$si=100')

        except:
            error = g2.s.port + " connect ERROR"
            w.lb_stt_com.setText(error)
            self.STT = 0
        while self.STT:
            if g2.s.in_waiting:  # Or: while ser.inWaiting():
                data = g2.read()
                data = data.decode()
                self.data.emit(data)
            # else:
            time.sleep(0.1)


class window(QtWidgets.QMainWindow):
    gcode = ''
    OK = 0
    datahienthi = ''
    def __init__(self, nameUi):
        QtWidgets.QWidget.__init__(self)
        # load giao dien
        uic.loadUi(nameUi, self)
        
        self.ScrollBar_Speed.sliderReleased.connect(self.ScrollBarSpeed)
        self.Speed = self.ScrollBar_Speed.value() * 100
        self.ScrollBar_Jerk.sliderReleased.connect(self.ScrollBarJerk)

        self.btn_Stop.clicked.connect(self.btnStop)
        self.btn_Pause.clicked.connect(self.btnPause)
        self.btn_Resume.clicked.connect(self.btnResume)
        self.btn_Run.clicked.connect(self.btnRun)
        self.btn_ZeroAll.clicked.connect(self.btnZeroAll)

        self.btn_X1.clicked.connect(self.btnX1)
        self.btn_X2.clicked.connect(self.btnX2)
        self.btn_Y1.clicked.connect(self.btnY1)
        self.btn_Y2.clicked.connect(self.btnY2)
        self.btn_Z1.clicked.connect(self.btnZ1)
        self.btn_Z2.clicked.connect(self.btnZ2)
        self.btn_U1.clicked.connect(self.btnU1)
        self.btn_U2.clicked.connect(self.btnU2)

        self.btn_SendMDI.clicked.connect(self.btnSendMDI)
        self.btn_ClearMDI.clicked.connect(self.btnClearMDI)

        self.thread = MyThread()
        comg2 = [comport.device for comport in serial.tools.list_ports.comports()]
        self.cbb_comg2.addItems(comg2)
        self.thread.data.connect(self.setStatus)
        self.btn_Connectg2.clicked.connect(self.btnConnectg2)
        self.show()

    def btnZeroAll(self):
        g2.send('g90g0x0y0z0u0')
    def ScrollBarSpeed(self):
        self.Speed = self.ScrollBar_Speed.value()*100
    def ScrollBarJerk(self):
        self.Jerk = self.ScrollBar_Jerk.value() * 10
        jerk = str(self.Jerk)
        g2.send('$xjm=' + jerk)
        g2.send('$yjm=' + jerk)
        g2.send('$zjm=' + jerk)
        g2.send('$ujm=' + jerk)

    def btnStop(self):
        g2.send('!')
        time.sleep(0.1)
        g2.send('%')
        print('Stop')
    def btnPause(self):
        g2.send('!')
        print('pause')
    def btnResume(self):
        g2.send('~')
        print('resume')
    def btnRun(self):
        g2.send('~')
        print('Run')

    def btnConnectg2(self):
        if g2.s.is_open:
            self.thread.STT = 0
            g2.close()
            time.sleep(0.5)
        cbb_comg2Text = self.cbb_comg2.currentText()
        g2.com(cbb_comg2Text)
        self.thread.STT = 1
        self.thread.start()

    def btnX1(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01x' + step +'f'+ vel
        g2.send(cmd)
    def btnX2(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01x-' + step +'f'+ vel
        g2.send(cmd)
    def btnY1(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01y' + step +'f'+ vel
        g2.send(cmd)
    def btnY2(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01y-' + step +'f'+ vel
        g2.send(cmd)
    def btnZ1(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01z' + step +'f'+ vel
        g2.send(cmd)
    def btnZ2(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01z-' + step +'f'+ vel
        g2.send(cmd)
    def btnU1(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01u' + step +'f'+ vel
        g2.send(cmd)
    def btnU2(self):
        step = str(self.SpinBox_Step.value())
        vel = str(self.Speed)
        cmd = 'g91g01u-' + step +'f'+ vel
        g2.send(cmd)

    def btnSendMDI(self):
        cmd = self.ld_stt.text()
        if cmd != '':
            g2.send('g90')
            g2.send(cmd)
        self.ld_stt.setText('')

    def btnClearMDI(self):
        self.textEdit_MDI.clear()
        self.datahienthi = ''

    def setStatus(self, c):
        data = json.loads(c)
        # chi hien thi khi o tab MDI
        if self.tabWidget.currentIndex() == 2:
            self.datahienthi = self.datahienthi + c
            self.textEdit_MDI.setText(self.datahienthi)
        # lay ra ten cua cac lop trong data
        for d in data:
            # neu trong data co lop f
            if d == 'f':
                # so 1 la lay gia tri thu 2 cua lop "f":[1,0,1]
                val = data[d][1]
                status = Stt.codes(int(val))
                self.lb_sttCode.setText(status)
                # print(status, val)

            if d == 'r':
                self.OK = 1

            # neu trong data co lop sr
            if d == 'sr':
                # lay cac lop co trong lop sr
                for sr in data[d]:
                    # neu trong lop sr co lop stat
                    if sr == 'stat':
                        # lay gia tri stat
                        val = data[d][sr]
                        status = Stt.machine(int(val))
                        self.lb_sttMachine.setText(status)
                    if sr == 'posx':
                        val = data[d][sr]
                        self.lb_x.setText(str(val))
                    if sr == 'posy':
                        val = data[d][sr]
                        self.lb_y.setText(str(val))
                    if sr == 'posz':
                        val = data[d][sr]
                        self.lb_z.setText(str(val))
                    if sr == 'posu':
                        val = data[d][sr]
                        self.lb_u.setText(str(val))
                    if sr == 'vel':
                        val = data[d][sr]
                        self.lb_vel.setText(str(val))
        self.setStatusPos()

    def setStatusPos(self):
        if self.lb_x.text() != "null":
            x = float(self.lb_x.text())
            y = float(self.lb_y.text())
            z = float(self.lb_z.text())
            u = float(self.lb_u.text())
            j = [x, y, z, u]
            pos = R.fkine(j)
            self.lb_px.setText(str(round(pos[0], 5)))
            self.lb_py.setText(str(round(pos[1], 5)))
            self.lb_pz.setText(str(round(pos[2], 5)))


if __name__ == "__main__":
    # khoi tao app
    app = QtWidgets.QApplication([])
    # load UI
    w = window("RobotUi.ui")
    app.exec()