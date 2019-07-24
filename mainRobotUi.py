from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QTableWidgetItem
from math import pi
import serial.tools.list_ports
import g2
import Stt
import json
import R
from robopy.base.transforms import tr2rpy
import time
import Program as pg
import test

class MyThreadJog(QThread):
    # bien ngat cua vong lap while
    STT = 0
    # ham duoc chay khi goi self.start()
    def run(self):
        while self.STT:
            dataJog = w.dataJog
            g2.send(dataJog)
            time.sleep(0.02)

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
            g2.send('$ej=1')
            g2.send('g54')
            time.sleep(1)
            g2.send('$sv=1')
            g2.send('$si=100')
            # setting
            g2.send('$2po=1')
            g2.send('$3po=0')
            g2.send('$4po=0')
            g2.send('$yhd=1')
            g2.send('$zhd=1')
            g2.send('$xtn=-115')
            g2.send('$xtm=115')
            g2.send('$ytn=-30')
            g2.send('$ytm=225')
            g2.send('$ztn=-135')
            g2.send('$ztm=135')
            g2.send('$atn=-45')
            g2.send('$atm=225')
            g2.send('$btn=-180')
            g2.send('$btm=180')
            g2.send('$sl=1')
            g2.send('$xzb=35')
            g2.send('$yzb=5')
            g2.send('$zzb=21')
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
            # time.sleep(0.1)

class window(QtWidgets.QMainWindow):
    gcode = ''
    OK = 0
    datahienthi = ''
    dataJog = ''
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
        self.btn_HomeAll.clicked.connect(self.btnHomeAll)
        self.btn_Ready.clicked.connect(self.btnReady)
        self.SpinBox_Step_Run.valueChanged.connect(self.StepRun)
        # self.cbb_Program.currentTextChanged.connect(self.cbbProgram)

        self.btn_X1.pressed.connect(self.btnX1JogPressed)
        self.btn_X2.pressed.connect(self.btnX2JogPressed)
        self.btn_Y1.pressed.connect(self.btnY1JogPressed)
        self.btn_Y2.pressed.connect(self.btnY2JogPressed)
        self.btn_Z1.pressed.connect(self.btnZ1JogPressed)
        self.btn_Z2.pressed.connect(self.btnZ2JogPressed)
        self.btn_A1.pressed.connect(self.btnA1JogPressed)
        self.btn_A2.pressed.connect(self.btnA2JogPressed)
        self.btn_B1.pressed.connect(self.btnB1JogPressed)
        self.btn_B2.pressed.connect(self.btnB2JogPressed)
        # self.btn_C1.pressed.connect(self.btnJogPressed)
        # self.btn_C2.pressed.connect(self.btnJogPressed)
        self.btn_X1.released.connect(self.btnX1JogReleased)
        self.btn_X2.released.connect(self.btnX2JogReleased)
        self.btn_Y1.released.connect(self.btnY1JogReleased)
        self.btn_Y2.released.connect(self.btnY2JogReleased)
        self.btn_Z1.released.connect(self.btnZ1JogReleased)
        self.btn_Z2.released.connect(self.btnZ2JogReleased)
        self.btn_A1.released.connect(self.btnA1JogReleased)
        self.btn_A2.released.connect(self.btnA2JogReleased)
        self.btn_B1.released.connect(self.btnB1JogReleased)
        self.btn_B2.released.connect(self.btnB2JogReleased)
        # self.btn_C1.released.connect(self.btnJogReleased)
        # self.btn_C2.released.connect(self.btnJogReleased)


        self.rb_Left.clicked.connect(self.btnLeftArm)
        self.rb_Right.clicked.connect(self.btnRightArm)
        self.cb_ServoON.clicked.connect(self.btnServoON)
        self.cb_Output1.clicked.connect(self.btnOutput1)
        self.cb_Output2.clicked.connect(self.btnOutput2)
        self.cb_Output3.clicked.connect(self.btnOutput3)
        self.cb_Output4.clicked.connect(self.btnOutput4)
        self.cb_Output5.clicked.connect(self.btnOutput5)
        self.cb_Output6.clicked.connect(self.btnOutput6)
        self.cb_Output7.clicked.connect(self.btnOutput7)
        self.cb_Output8.clicked.connect(self.btnOutput8)
        self.cb_Output9.clicked.connect(self.btnOutput9)

        self.btn_Add.clicked.connect(self.btnAdd)
        self.btn_Inset.clicked.connect(self.btnInset)
        self.btn_Save.clicked.connect(self.btnSave)
        self.btn_Delete.clicked.connect(self.btnDelete)
        self.table.cellClicked.connect(self.on_click)
        self.btn_Load.clicked.connect(self.btnLoad)
        self.btn_Delete_Program.clicked.connect(self.btnDeleteProgram)

        self.btn_PX1.clicked.connect(self.btnPX1)
        self.btn_PX2.clicked.connect(self.btnPX2)
        self.btn_PY1.clicked.connect(self.btnPY1)
        self.btn_PY2.clicked.connect(self.btnPY2)
        self.btn_PZ1.clicked.connect(self.btnPZ1)
        self.btn_PZ2.clicked.connect(self.btnPZ2)

        self.btn_SendMDI.clicked.connect(self.btnSendMDI)
        self.btn_ClearMDI.clicked.connect(self.btnClearMDI)

        self.runThread = RunThread()
        self.thread = MyThread()
        self.jogthread = MyThreadJog()
        comg2 = [comport.device for comport in serial.tools.list_ports.comports()]
        self.cbb_comg2.addItems(comg2)
        self.thread.data.connect(self.setStatus)
        self.btn_Connectg2.clicked.connect(self.btnConnectg2)

        namepg = pg.get_all_nameTableDB()
        name = namepg[::-1]
        if len(name)>0:
            self.loadTable(name[0])
            self.cbb_Program.addItems(name)
        self.table.setSelectionBehavior(1)
        self.table.selectRow(0)

        self.show()
    def cbbProgram(self):
        self.SpinBox_Step_Run.setValue(0)
    def JogPressed(self, joint):
        vel = str(self.Speed)
        if joint == "X1":
            g2.send("$xjm=2000")
            self.dataJog = "g91g1x0.1f" + vel
        if joint == "X2":
            g2.send("$xjm=2000")
            self.dataJog = "g91g1x-0.1f" + vel
        if joint == "Y1":
            g2.send("$yjm=1000")
            self.dataJog = "g91g1y0.1f" + vel
        if joint == "Y2":
            g2.send("$yjm=1000")
            self.dataJog = "g91g1y-0.1f" + vel
        if joint == "Z1":
            g2.send("$zjm=1000")
            self.dataJog = "g91g1z0.1f" + vel
        if joint == "Z2":
            g2.send("$zjm=1000")
            self.dataJog = "g91g1z-0.1f" + vel
        if joint == "A1":
            g2.send("$ajm=10000")
            g2.send("$bjm=10000")
            self.dataJog = "g91g1a0.5b-0.5f" + vel
        if joint == "A2":
            g2.send("$ajm=10000")
            g2.send("$bjm=10000")
            self.dataJog = "g91g1a-0.5b0.5f" + vel
        if joint == "B1":
            g2.send("$bjm=10000")
            self.dataJog = "g91g1b0.5f" + vel
        if joint == "B2":
            g2.send("$bjm=10000")
            self.dataJog = "g91g1b-0.5f" + vel
        self.jogthread.STT = 1
        self.jogthread.start()
    def JogReleased(self, joint):
        jerk = self.ScrollBar_Jerk.value() * 10
        if joint == "X1" or joint == "X2":
            self.jogthread.STT = 0
            g2.send("$xjm=" + str(jerk))
        if joint == "Y1" or joint == "Y2":
            self.jogthread.STT = 0
            g2.send("$yjm=" + str(jerk))
        if joint == "Z1" or joint == "Z2":
            self.jogthread.STT = 0
            g2.send("$zjm=" + str(jerk))
        if joint == "A1" or joint == "A2":
            self.jogthread.STT = 0
            g2.send("$ajm=" + str(jerk))
        if joint == "B1" or joint == "B2":
            self.jogthread.STT = 0
            g2.send("$bjm=" + str(jerk))

    def btnX1JogPressed(self):
        self.JogPressed("X1")
    def btnX1JogReleased(self):
        self.JogReleased("X1")
    def btnX2JogPressed(self):
        self.JogPressed("X2")
    def btnX2JogReleased(self):
        self.JogReleased("X2")
    def btnY1JogPressed(self):
        self.JogPressed("Y1")
    def btnY1JogReleased(self):
        self.JogReleased("Y1")
    def btnY2JogPressed(self):
        self.JogPressed("Y2")
    def btnY2JogReleased(self):
        self.JogReleased("Y2")
    def btnZ1JogPressed(self):
        self.JogPressed("Z1")
    def btnZ1JogReleased(self):
        self.JogReleased("Z1")
    def btnZ2JogPressed(self):
        self.JogPressed("Z2")
    def btnZ2JogReleased(self):
        self.JogReleased("Z2")
    def btnA1JogPressed(self):
        self.JogPressed("A1")
    def btnA1JogReleased(self):
        self.JogReleased("A1")
    def btnA2JogPressed(self):
        self.JogPressed("A2")
    def btnA2JogReleased(self):
        self.JogReleased("A2")
    def btnB1JogPressed(self):
        self.JogPressed("B1")
    def btnB1JogReleased(self):
        self.JogReleased("B1")
    def btnB2JogPressed(self):
        self.JogPressed("B2")
    def btnB2JogReleased(self):
        self.JogReleased("B2")


    def btnReady(self):
        g2.send('g90g0x0y120z120a120b-30')
    def StepRun(self):
        r = self.SpinBox_Step_Run.value()
        name1 = self.cbb_Program.currentText()
        rCount = self.table.rowCount() - 1
        if r > rCount:
            r = rCount
            self.SpinBox_Step_Run.setValue(r)
            print("error")
        # self.table.selectRow(r)
        gcode, error, i = test.RunStep(name1, r)
        if error:
            message = "Build Error"
            QMessageBox.about(self, "Program Error", message)
        else:
            self.gcode = gcode
            self.OK = 1
            self.runThread.sttRun = 1
            self.runThread.start()
            self.table.selectRow(i+1)
            # self.SpinBox_Step_Run.setValue(i)

    def btnDeleteProgram(self):
        name1 = self.cbb_Program.currentText()
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you want Delete " + name1 + " ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            pg.del_and_update(name1)
            self.cbb_Program.clear()
            name2 = pg.get_all_nameTableDB()
            self.cbb_Program.addItems(name2[::-1])
            self.loadTable(name2[0])
            message = name1 + " has been delete"
            QMessageBox.about(self, "Delete", message)
        else:
            print('No clicked.')

    def btnLoad(self):
        namepg = self.cbb_Program.currentText()
        self.loadTable(namepg)

    def btnSave(self):
        r = self.table.rowCount()
        c = self.table.columnCount()
        data = []
        error = 0
        for row in range(1, r):
            d = []
            for column in range(c):
                item = self.table.item(row, column).text()
                if column == 5:
                    d.append(item)
                else:
                    try:
                        d.append(float(item))
                    except:
                        error = 1
                        message = "row: " + str(row+1) + " Column: " + str(column+1) + " must be number!"
                        QMessageBox.about(self, "Program Error", message)
                        break
            if error:
                break
            else:
                data.append(d)
        if error == 0:
            namepg = self.cbb_Program.currentText()
            pg.del_and_update(namepg)
            pg.create_table(namepg)
            for r in range(len(data)):
                pg.data_entry(namepg, data[r])
            pg.conn.commit()
            message = namepg + " save Ok"
            QMessageBox.about(self, "Save", message)
            name2 = pg.get_all_nameTableDB()
            self.cbb_Program.clear()
            self.cbb_Program.addItems(name2[::-1])
            self.loadTable(namepg)

    def loadTable(self, name):
        try:
            r = self.table.rowCount()
            if r > 1:
                for i in range(1, r):
                    self.table.removeRow(1)
            data = pg.read_from_db(name)
            self.table.setItem(0, 0, QTableWidgetItem("X"))
            self.table.setItem(0, 1, QTableWidgetItem("Y"))
            self.table.setItem(0, 2, QTableWidgetItem("Z"))
            self.table.setItem(0, 3, QTableWidgetItem("A"))
            self.table.setItem(0, 4, QTableWidgetItem("B"))
            self.table.setItem(0, 5, QTableWidgetItem("MODE"))
            self.table.setItem(0, 6, QTableWidgetItem("VEL %"))
            for r in range(len(data)):
                row = r + 1
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(data[r][0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(data[r][1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(data[r][2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(data[r][3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(data[r][4])))
                self.table.setItem(row, 5, QTableWidgetItem(str(data[r][5])))
                self.table.setItem(row, 6, QTableWidgetItem(str(data[r][6])))
        except:
            print("error")
            QMessageBox.about(self, "Load Error", "File name no found!")

    def btnDelete(self):
        hang = self.table.currentRow()
        if hang != 0:
            self.table.removeRow(hang)
    def btnInset(self):
        hang = self.table.currentRow()
        self.table.insertRow(hang)
    def on_click(self):
        cot =  self.table.currentColumn()
        hang = self.table.currentRow()
        item = self.table.item(hang, cot)

    def btnAdd(self):
        self.table.setItem(0, 0, QTableWidgetItem("X"))
        self.table.setItem(0, 1, QTableWidgetItem("Y"))
        self.table.setItem(0, 2, QTableWidgetItem("Z"))
        self.table.setItem(0, 3, QTableWidgetItem("A"))
        self.table.setItem(0, 4, QTableWidgetItem("B"))
        self.table.setItem(0, 5, QTableWidgetItem("MODE"))
        self.table.setItem(0, 6, QTableWidgetItem("VEL %"))
        hang = self.table.rowCount()
        self.table.insertRow(hang)
        x = float(self.lb_x.text())
        y = float(self.lb_y.text())
        z = float(self.lb_z.text())
        a = float(self.lb_a.text())
        b = float(self.lb_b.text()) - 90 + a
        self.table.setItem(hang, 0, QTableWidgetItem(str(round(x, 4))))
        self.table.setItem(hang, 1, QTableWidgetItem(str(round(y, 4))))
        self.table.setItem(hang, 2, QTableWidgetItem(str(round(z, 4))))
        self.table.setItem(hang, 3, QTableWidgetItem(str(round(a, 4))))
        self.table.setItem(hang, 4, QTableWidgetItem(str(round(b, 4))))
        self.table.setItem(hang, 5, QTableWidgetItem("P"))
        self.table.setItem(hang, 6, QTableWidgetItem("15"))

    def btnHomeAll(self):
        g2.send('g28.2x0y0z0')
        g2.send('g28.3x0y90z0a90b0')
    def btnOutput1(self):
        if self.cb_Output1.isChecked():
            g2.send('$out1=1')
        else:
            g2.send('$out1=0')
    def btnOutput2(self):
        if self.cb_Output2.isChecked():
            g2.send('$out2=1')
        else:
            g2.send('$out2=0')
    def btnOutput3(self):
        if self.cb_Output3.isChecked():
            g2.send('$out3=1')
        else:
            g2.send('$out3=0')
    def btnOutput4(self):
        if self.cb_Output4.isChecked():
            g2.send('$out4=1')
        else:
            g2.send('$out4=0')

    def btnOutput5(self):
        if self.cb_Output5.isChecked():
            g2.send('$out5=1')
        else:
            g2.send('$out5=0')
    def btnOutput6(self):
        if self.cb_Output6.isChecked():
            g2.send('$out6=1')
        else:
            g2.send('$out6=0')
    def btnOutput7(self):
        if self.cb_Output7.isChecked():
            g2.send('$out7=1')
        else:
            g2.send('$out7=0')
    def btnOutput8(self):
        if self.cb_Output8.isChecked():
            g2.send('$out8=1')
        else:
            g2.send('$out8=0')
    def btnOutput9(self):
        if self.cb_Output9.isChecked():
            g2.send('$out9=1')
        else:
            g2.send('$out9=0')
    def btnServoON(self):
        if self.cb_ServoON.isChecked():
            g2.send('$out1=1')
        else:
            g2.send('$out1=0')
    def btnLeftArm(self):
        self.P_program('none')
    def btnRightArm(self):
        self.P_program('none')

    def P_program(self, p):
        px = float(self.lb_px.text())
        py = float(self.lb_py.text())
        pz = float(self.lb_pz.text())
        rad = pi/180
        x = float(self.lb_x.text())*rad
        y = float(self.lb_y.text())*rad
        z = float(self.lb_z.text())*rad
        a = float(self.lb_a.text())*rad
        b = float(self.lb_b.text())*rad - 90*rad + a

        step = self.SpinBox_Step.value()

        if self.rb_Left.isChecked():
            otp = [1, 1, 0]
        else:
            otp = [0, 0, 0]
        if p == 'PX1':
            px = px + step
        if p == 'PX2':
            px = px - step
        if p == 'PY1':
            py = py + step
        if p == 'PY2':
            py = py - step
        if p == 'PZ1':
            pz = pz + step
        if p == 'PZ2':
            pz = pz - step

        j, limit = R.ikine([px, py, pz], [x, y, z, a, b], otp)
        if limit and self.cb_ApplyLimit.isChecked():
            QMessageBox.about(self, "Error", "Joint is limit!")
        else:
            vel = str(self.Speed)
            cmd = 'g90g01x' + str(round(j[0], 4)) \
                  + 'y' + str(round(j[1], 4)) \
                  + 'z' + str(round(j[2], 4)) \
                  + 'a' + str(round(j[3], 4)) \
                  + 'b' + str(round(j[4] + 90 - j[3], 4)) \
                  + 'f' + vel
            g2.send(cmd)

    def btnPX1(self):
        self.P_program('PX1')

    def btnPX2(self):
        self.P_program('PX2')

    def btnPY1(self):
        self.P_program('PY1')

    def btnPY2(self):
        self.P_program('PY2')
    def btnPZ1(self):
        self.P_program('PZ1')
    def btnPZ2(self):
        self.P_program('PZ2')

    def btnZeroAll(self):
        g2.send('g90g0x0y90z0a90b0c0')
    def ScrollBarSpeed(self):
        self.Speed = self.ScrollBar_Speed.value()*100
    def ScrollBarJerk(self):
        self.Jerk = self.ScrollBar_Jerk.value() * 10
        jerk = str(self.Jerk)
        g2.send('$xjm=' + jerk)
        g2.send('$yjm=' + jerk)
        g2.send('$zjm=' + jerk)
        g2.send('$ajm=' + jerk)
        g2.send('$bjm=' + jerk)
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
        name1 = self.cbb_Program.currentText()
        self.gcode, error = test.Run(name1)
        if error:
            message = "Build Error"
            QMessageBox.about(self, "Program Error", message)
        else:
            self.runThread.sttRun = 1
            self.runThread.start()
    def btnConnectg2(self):
        if g2.s.is_open:
            self.thread.STT = 0
            g2.close()
            time.sleep(0.5)
        cbb_comg2Text = self.cbb_comg2.currentText()
        g2.com(cbb_comg2Text)
        self.thread.STT = 1
        self.thread.start()
    def btnSendMDI(self):
        cmd = self.ld_stt.text()
        if cmd != '':
            g2.send(cmd)
        self.ld_stt.setText('')
    def btnClearMDI(self):
        self.textEdit_MDI.clear()
        self.datahienthi = ''
    def setStatus(self, c):
        data = json.loads(c)
        # chi hien thi khi o tab MDI
        if self.tabWidget_1.currentIndex() == 2:
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
                    if sr == 'posa':
                        val = data[d][sr]
                        self.lb_a.setText(str(val))
                    if sr == 'posb':
                        val = data[d][sr]
                        self.lb_b.setText(str(val))
                    if sr == 'posc':
                        val = data[d][sr]
                        self.lb_c.setText(str(val))
                    if sr == 'vel':
                        val = data[d][sr]
                        self.lb_vel.setText(str(val))
                self.setStatusPos()

    def setStatusPos(self):
        if self.lb_x.text() != "null":
            x = float(self.lb_x.text())
            y = float(self.lb_y.text())
            z = float(self.lb_z.text())
            a = float(self.lb_a.text())
            b = float(self.lb_b.text())
            # c = float(self.lb_c.text())
            j = [x, y, z, a, b]
            T = R.fkine2(j)
            self.T = T
            rpy = tr2rpy(T, 'deg', 'xyz')
            self.lb_px.setText(str(round(T[0, 3], 5)))
            self.lb_py.setText(str(round(T[1, 3], 5)))
            self.lb_pz.setText(str(round(T[2, 3], 5)))
            self.lb_roll.setText(str(round(rpy[0, 0], 5)))
            self.lb_pitch.setText(str(round(rpy[0, 1], 5)))
            self.lb_yam.setText(str(round(rpy[0, 2], 5)))

class RunThread(QThread):
    sttRun = 0
    i = 3
    def run(self):
        if len(w.gcode) > 4:
            for n in range(0, 4):
                cmd = w.gcode[n]
                g2.send(cmd)
        else:
            self.i = 0

        print(w.OK)
        while self.sttRun:
            time.sleep(0.001)
            if w.OK:
                w.OK = 0
                if self.i == len(w.gcode):
                    print('#'*50)
                    w.lb_Line.setText("Done*********")
                    self.i = 3
                    break
                w.lb_Line.setText(str(self.i))
                cmd = w.gcode[self.i]
                g2.send(cmd)
                self.i += 1

if __name__ == "__main__":
    # khoi tao app
    app = QtWidgets.QApplication([])
    # load UI
    w = window("RobotUi.ui")
    app.exec()
