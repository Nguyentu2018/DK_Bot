import Program as pg
import R
import numpy as np

def Run(self, name):
    data = pg.read_from_db(name)
    gcode = []
    i = 0
    error = False
    while i < len(data) and not error:
        self.table.selectRow(i+1)
        #neu mode la p thi di chuyen theo diem
        if data[i][4] == 'P':
            #gcode.append("#" * 20 + " Position " + "#" * 20)
            row = list(data[i])
            # xoa mode
            row.remove(row[4])
            # xoa vel
            row.remove(row[4])
            # tinh dong hoc nghich
            j, error = R.ikine(row, [1, 0])
            # neu khong co loi
            if error == 0:
                cmd = 'G0X' + str(round(j[0], 4)) + ' Y' + str(round(j[1], 4)) + ' Z' + str(round(j[2], 4)) \
                      + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5])
                gcode.append(cmd)

        if data[i][4] == 'L':
            #gcode.append("#" * 20 + " Line " + "#" * 20)
            p1 = list(data[i])
            p1.remove(p1[4])
            p1.remove(p1[4])

            p2 = list(data[i+1])
            p2.remove(p2[4])
            p2.remove(p2[4])
            i = i + 1
            n = 99
            step = np.linspace(p1, p2, n)
            step1 = step.tolist()
            for a in range(n):
                j, error = R.ikine(step1[a], [1, 0])
                # neu khong co loi
                if error == 0:
                    cmd = 'G0X' + str(round(j[0], 4)) + ' Y' + str(round(j[1], 4)) + ' Z' + str(round(j[2], 4)) \
                          + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5])
                    gcode.append(cmd)
                else:
                    print("error in " + str(a))
                    break

        if data[i][4] == 'C':
            #gcode.append("#"*20 +" Cricle "+ "#"*20)
            p1 = list(data[i])
            bk = p1[5]
            p1.remove(p1[5])
            p1.remove(p1[4])

            n = 100
            step = np.linspace(0, 2*np.pi, n)
            x = []
            y = []
            for t in step:
                px = bk * np.cos(t) + p1[0]
                x.append(float(px))
            for t in step:
                py = bk * np.sin(t) + p1[1]
                y.append(float(py))
            for a in range(n):
                pos = [x[a], y[a], p1[2], p1[3]]
                j, error = R.ikine(pos, [1, 0])
                # neu khong co loi
                if error == 0:
                    cmd = 'G0X' + str(round(j[0], 4)) + ' Y' + str(round(j[1], 4)) + ' Z' + str(round(j[2], 4)) \
                          + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5])
                    gcode.append(cmd)
                else:
                    print("error in " + str(i))
                    break
        i = i + 1
    [print(gcode[r]) for r in range(len(gcode))]
    print(len(gcode))
    return gcode
