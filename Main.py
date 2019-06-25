from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
import serial.tools.list_ports
import time
import g2
import Stt
import json
import ecd

class EncoderThread(QThread):
    # bien data
    data = pyqtSignal(str)
    # bien ngat cua vong lap while
    STT = 1
    # ham duoc chay khi goi self.start()
    def run(self):
        try:
            ecd.open()
            w.lb_stt_com.setText(ecd.s.port +" connect OK")
            w.widget_2.setEnabled(True)
            w.widget_3.setEnabled(True)
        except:
            error = ecd.s.port + " connect ERROR"
            w.lb_stt_com.setText(error)
            self.STT = 0
            w.widget_2.setEnabled(False)
            w.widget_3.setEnabled(False)
        while self.STT:
            if ecd.s.in_waiting:  # Or: while ser.inWaiting():
                try:
                    data = ecd.read()
                    data = data.decode()
                    self.data.emit(data)
                except:
                    pass




class MyThread(QThread):
    # bien data
    data = pyqtSignal(str)
    # bien ngat cua vong lap while
    STT = 1
    # ham duoc chay khi goi self.start()
    def run(self):
        try:
            g2.open()
            w.widget.setEnabled(True)
            w.lb_stt_com.setText(g2.s.port + " connect OK")
        except:
            error = g2.s.port + " connect ERROR"
            w.lb_stt_com.setText(error)
            self.STT = 0
            w.widget.setEnabled(False)
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
        self.btn_Run.clicked.connect(self.btnRun)
        self.Step.valueChanged.connect(self.btnStep)
        self.btn_Stop.clicked.connect(self.btnStop)
        self.btn_Open.clicked.connect(self.btnOpen)
        self.btn_SendMDI.clicked.connect(self.btnSendMDI)
        self.btn_HomeBe.clicked.connect(self.btnHomeBe)
        self.btn_HomeXoay.clicked.connect(self.btnHomeXoay)
        self.btn_HomeKhuon.clicked.connect(self.btnHomeKhuon)
        self.btn_HomeDay.clicked.connect(self.btnHomeDay)
        self.btn_HomeAll.clicked.connect(self.btnHomeAll)
        self.btn_StopG2.clicked.connect(self.btnStopG2)

        self.btn_Be1.clicked.connect(self.btnBe1)
        self.btn_Be2.clicked.connect(self.btnBe2)
        self.btn_Xoay1.clicked.connect(self.btnXoay1)
        self.btn_Xoay2.clicked.connect(self.btnXoay2)
        self.btn_Day1.clicked.connect(self.btnDay1)
        self.btn_Day2.clicked.connect(self.btnDay2)
        self.btn_Khuon1.clicked.connect(self.btnKhuon1)
        self.btn_Khuon2.clicked.connect(self.btnKhuon2)

        self.cb_Khuon.stateChanged.connect(self.cbKhuon)
        self.cb_CutDay.stateChanged.connect(self.cbCutDay)
        self.cb_KepEncoder.stateChanged.connect(self.cbKepEncoder)
        self.cb_ResetEncoder.stateChanged.connect(self.cbResetEncoder)
        self.btn_Connectg2.clicked.connect(self.btnConnectg2)
        self.btn_Connectecd.clicked.connect(self.btnConnectecd)


        self.thread = MyThread()
        comg2 = [comport.device for comport in serial.tools.list_ports.comports()]
        self.cbb_comg2.addItems(comg2)
        self.thread.data.connect(self.setStatus)

        self.Encoderthread = EncoderThread()
        comecd = [comport.device for comport in serial.tools.list_ports.comports()]
        self.cbb_comecd.addItems(comecd)
        self.Encoderthread.data.connect(self.setEncoder)

        self.runThread = RunThread()
        self.show()

    def btnConnectg2(self):
        if g2.s.is_open:
            self.thread.STT = 0
            g2.close()
            time.sleep(0.5)
        cbb_comg2Text = self.cbb_comg2.currentText()
        g2.com(cbb_comg2Text)
        self.thread.STT = 1
        self.thread.start()

    def btnConnectecd(self):
        if ecd.s.is_open:
            self.Encoderthread.STT = 0
            ecd.close()
            time.sleep(0.5)
        cbb_comecdText = self.cbb_comecd.currentText()
        ecd.com(cbb_comecdText)
        self.Encoderthread.STT = 1
        self.Encoderthread.start()

    def cbKhuon(self, state):
        if state:
            ecd.send('A1B0*')
        else:
            ecd.send('A1B1*')
    def cbCutDay(self, state):
        if state:
            ecd.send('A2B0*')
        else:
            ecd.send('A2B1*')
    def cbKepEncoder(self, state):
        if state:
            ecd.send('A3B0*')
        else:
            ecd.send('A3B1*')
    def cbResetEncoder(self, state):
        if state:
            ecd.send('A4B0*')
        else:
            ecd.send('A4B1*')

    def btnStopG2(self):
        self.runThread.sttRun = 0
        g2.send('!')
        time.sleep(0.1)
        g2.send('%')
    def btnBe1(self):
        pos = self.lineEdit_4.text()
        vel = self.lineEdit_2.text()
        cmd = 'g91g01x' + pos +'f'+ vel
        g2.send(cmd)
    def btnBe2(self):
        pos = self.lineEdit_4.text()
        vel = self.lineEdit_2.text()
        cmd = 'g91g01x-' + pos +'f'+ vel
        g2.send(cmd)
    def btnXoay1(self):
        pos = self.lineEdit_6.text()
        vel = self.lineEdit.text()
        cmd = 'g91g01y' + pos +'f'+ vel
        g2.send(cmd)
    def btnXoay2(self):
        pos = self.lineEdit_6.text()
        vel = self.lineEdit.text()
        cmd = 'g91g01y-' + pos +'f'+ vel
        g2.send(cmd)
    def btnDay1(self):
        pos = self.lineEdit_5.text()
        vel = self.lineEdit_3.text()
        cmd = 'g91g01z' + pos +'f'+ vel
        g2.send(cmd)
    def btnDay2(self):
        pos = self.lineEdit_5.text()
        vel = self.lineEdit_3.text()
        cmd = 'g91g01z-' + pos +'f'+ vel
        g2.send(cmd)
    def btnKhuon1(self):
        pos = self.lineEdit_7.text()
        vel = self.lineEdit_8.text()
        cmd = 'g91g01u' + pos +'f'+ vel
        g2.send(cmd)
    def btnKhuon2(self):
        pos = self.lineEdit_7.text()
        vel = self.lineEdit_8.text()
        cmd = 'g91g01u-' + pos +'f'+ vel
        g2.send(cmd)

    def btnHomeBe(self):
        g2.send('g90g0x0')
        #lay text tu text edit
        a = self.edit_Program.toPlainText()
        x = a.split()
        print(a)
        print(x)
    def btnHomeXoay(self):
        g2.send('g90g0y0')
    def btnHomeKhuon(self):
        g2.send('g90g0u0')
    def btnHomeDay(self):
        g2.send('g90g0z0')
    def btnHomeAll(self):
        g2.send('g90g0x0y0u0')
        g2.send('G10 L20 P2 Z0')

    def btnSendMDI(self):
        cmd = self.ld_stt.text()
        print(cmd)
        g2.send(cmd)

    def setEncoder(self, c):
        try:
            if c != "":
                b = c.rstrip("\r\n")
                w.lb_Encoder.setText(b)
        except:
            print("ERROR2")


    def setStatus(self, c):
        data = json.loads(c)
        # lay ra ten cua cac lop trong data
        for d in data:
            # neu trong data co lop f
            if d == 'f':
                # so 1 la lay gia tri thu 2 cua lop "f":[1,0,1]
                # <=>val = 0
                val = data[d][1]
                status = Stt.codes(int(val))
                self.lb_stt.setText(status)
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
                        self.lb_stt.setText(status)
                    if sr == 'posx':
                        val = data[d][sr]
                        self.lb_Be.setText(str(val))
                    if sr == 'posy':
                        val = data[d][sr]
                        self.lb_Xoay.setText(str(val))
                    if sr == 'posz':
                        val = data[d][sr]
                        self.lb_Day.setText(str(val))
                    if sr == 'posu':
                        val = data[d][sr]
                        self.lb_Khuon.setText(str(val))
                    if sr == 'vel':
                        val = data[d][sr]
                        self.lb_Velocity.setText(str(val))
    def btnRun(self):
        self.runThread.sttRun = 1
        self.runThread.start()

    def btnStep(self):
        try:
            value = self.Step.value()
            if value >= len(self.program):
                self.Step.setValue(value-1)
                value = value -1
            line = self.program[value].upper()
            w.lb_Stt.setText(line)
        except:
            print('error')


    def btnStop(self):
        print('Stop')
        self.runThread.sttRun = 0

    def btnOpen(self):
        try:
            fileName = 'ct1.txt'
            f = open(fileName)
            self.program = f.readlines()
            f.close()
            f = open(fileName)
            program = f.read()
            f.close()
            self.edit_Program.setText(program)
        except:
            self.edit_Program.setText('Error File')

# def check_next():
# #     while
# #     w.lb_stt.text()

class RunThread(QThread):
    sttRun = 0
    n = 0
    def run(self):
        print('Run')
        # ct = w.program
        a = w.edit_Program.toPlainText()
        a = a.upper()
        ct = a.split()
        print(ct)
        SL_Dat = w.Step_SL.value()
        SL = int(w.edit_SL.text())
        try:
            for i in range(SL, SL_Dat):
                if self.sttRun == 0:
                    break
                for n in range(0, len(ct)):
                    if n == len(ct)-1:
                        w.edit_SL.setText(str(i + 1))
                        g2.send('g90g0x0y0u0')
                        g2.send('G10 L20 P2 Z0')
                    if self.sttRun == 0:
                        break
                    line = ct[n]
                    if line == 'K1':
                        print('Nâng khuôn ')
                        w.lb_Stt.setText('Nâng khuôn')
                        ecd.send('A1B0*')

                    if line == 'K0':
                        print('Hạ khuôn ')
                        w.lb_Stt.setText('Hạ khuôn')
                        ecd.send('A1B1*')

                    if line[0] == 'A':
                        goc = line.lstrip('A')
                        print('Bẻ trước ' + goc)
                        w.lb_Stt.setText('Bẻ trước ' + goc)
                        g2.send('g90g01x' + goc +'f10000')
                        while w.lb_stt.text()!='Next':
                            time.sleep(0.1)
                            pass

                    if line[0] == 'B':
                        goc = line.lstrip('B')
                        print('Bẻ sau ' + goc)
                        w.lb_Stt.setText('Bẻ sau ' + goc)
                        g2.send('g90g01x' + goc + 'f10000')
                        while w.lb_stt.text() != 'Next':
                            time.sleep(0.1)
                            pass

                    if line[0] == 'X':
                        goc = line.lstrip('X')
                        print('Xoay ' + goc)
                        w.lb_Stt.setText('Xoay ' + goc)
                        g2.send('g90g01Y' + goc + 'f1000')
                        while w.lb_stt.text() != 'Next':
                            time.sleep(0.1)
                            pass

                    if line[0] == 'D':
                        feed = line.lstrip('D')
                        print('Đẩy dây ' + feed)
                        w.lb_Stt.setText('Đẩy dây ' + feed)
                        g2.send('g91g01Z' + feed + 'f1000')
                        while w.lb_stt.text() != 'Next':
                            time.sleep(0.1)
                            pass
                    time.sleep(0.1)

        except:
            print("END")
        self.n = 0
        self.sttRun = 0
        print('Stop....')
        w.lb_Stt.setText('Stop ')



if __name__ == "__main__":
    # khoi tao app
    app = QtWidgets.QApplication([])
    # load UI
    w = window("RobotUi.ui")
    app.exec()


