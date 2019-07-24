import Program as pg
import R
import numpy as np
from sympy import Eq, linsolve, symbols
from math import sqrt, pi

def Run(name):
    data = pg.read_from_db(name)
    gcode = ['G90']
    i = 0
    error = False
    while i < len(data) and not error:
        #neu mode la p thi di chuyen theo diem
        if data[i][5] == 'P':
            # gcode.append("#" * 20 + " Position " + "#" * 20)
            row = list(data[i])
            # xoa mode
            row.remove(row[5])
            # xoa vel
            row.remove(row[5])
            # tinh dong hoc nghich
            j = row
            # neu khong co loi
            cmd = 'G1x' + str(round(j[0], 4)) + 'y' + str(round(j[1], 4)) + 'z' + str(round(j[2], 4)) \
                  + 'a' + str(round(j[3], 4)) + 'b' + str(round(j[4] + 90 - j[3], 4)) + 'f' + str(data[i][6] * 200)
            gcode.append(cmd)

        if data[i][5] == 'L':
            #gcode.append("#" * 20 + " Line " + "#" * 20)
            p1 = list(data[i])
            p1.remove(p1[5])
            p1.remove(p1[5])
            rad = pi/180
            j1 = [p1[0]*rad, p1[1]*rad, p1[2]*rad, p1[3]*rad, p1[4]*rad]

            p2 = list(data[i+1])
            p2.remove(p2[5])
            p2.remove(p2[5])

            pos1 = R.fkine(p1)
            pos2 = R.fkine(p2)
            i = i + 1
            n = 1000
            step = np.linspace(pos1, pos2, n)
            step1 = step.tolist()
            for a in range(n):
                j, error = R.ikine(step1[a], j1, [1, 1, 0])
                # neu khong co loi
                if error == 0:
                    cmd = 'G1x' + str(round(j[0], 4)) + 'y' + str(round(j[1], 4)) + 'z' + str(round(j[2], 4)) \
                          + 'a' + str(round(j[3], 4)) + 'b' + str(round(j[4] + 90 - j[3], 4)) + 'f' + str(
                        data[i-1][6] * 200)
                    gcode.append(cmd)
                else:
                    print("error in " + str(a))
                    break

        if data[i][5] == 'C':
            #gcode.append("#"*20 +" Cricle "+ "#"*20)
            p1 = list(data[i])
            bk = p1[6]
            p1.remove(p1[5])
            p1.remove(p1[5])
            pos1 = R.fkine(p1)
            n = 100
            step = np.linspace(0, 2*np.pi, n)
            x = []
            y = []
            for t in step:
                px = bk * np.cos(t) + pos1[0]
                x.append(float(px))
            for t in step:
                py = bk * np.sin(t) + pos1[1]
                y.append(float(py))
            for a in range(n):
                pos = [x[a], y[a], pos1[2]]
                j, error = R.ikine(pos, p1, [1, 1, 0])
                # neu khong co loi
                if error == 0:
                    cmd = 'G1x' + str(round(j[0], 4)) + 'y' + str(round(j[1], 4)) + 'z' + str(round(j[2], 4)) \
                          + 'a' + str(round(j[3], 4)) + 'b' + str(round(j[4] + 90 - j[3], 4)) + 'f' + str(
                        data[i - 1][6] * 200)
                    gcode.append(cmd)
                else:
                    print("error in " + str(a))
                    break
        if data[i][4] == 'C2':
            p1 = list(data[i])
            A = [p1[0], p1[1]]

            p2 = list(data[i+1])
            B = [p2[0], p2[1]]

            p3 = list(data[i+2])
            C = [p3[0], p3[1]]

            tam, bk = C2(A, B, C)

            n = 100
            goc_cung = 360
            step = np.linspace(0, goc_cung * np.pi /180, n)
            x = []
            y = []
            for t in step:
                px = bk * np.cos(t) + tam[0]
                x.append(float(px))
            for t in step:
                py = bk * np.sin(t) + tam[1]
                y.append(float(py))
            for a in range(n):
                pos = [x[a], y[a], p1[2], p1[3]]
                j, error = R.ikine(pos, [1, 0])
                # neu khong co loi
                if error == 0:
                    cmd = 'G0X' + str(round(j[0], 4)) + ' Y' + str(round(j[1], 4)) + ' Z' + str(round(j[2], 4)) \
                          + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5]*200)
                    gcode.append(cmd)
                else:
                    print("error in " + str(i))
                    break
            i += 2
        i += 1
    [print(gcode[r]) for r in range(len(gcode))]
    print(len(gcode))
    return gcode, error

def RunStep(name, i):
    i -= 1
    if i == -1:
        i = 0
    data = pg.read_from_db(name)
    gcode = ['G90']
    error = False
    #neu mode la p thi di chuyen theo diem
    if data[i][5] == 'P':
        #gcode.append("#" * 20 + " Position " + "#" * 20)
        row = list(data[i])
        # xoa mode
        row.remove(row[5])
        # xoa vel
        row.remove(row[5])
        # tinh dong hoc nghich
        j = row
        # neu khong co loi
        cmd = 'G1x' + str(round(j[0], 4)) + 'y' + str(round(j[1], 4)) + 'z' + str(round(j[2], 4)) \
              + 'a' + str(round(j[3], 4)) + 'b' + str(round(j[4] + 90 - j[3], 4)) + 'f' + str(data[i][6]*200)
        gcode.append(cmd)

    if data[i][5] == 'L':
        # gcode.append("#" * 20 + " Line " + "#" * 20)
        p1 = list(data[i])
        p1.remove(p1[5])
        p1.remove(p1[5])
        rad = pi / 180
        j1 = [p1[0] * rad, p1[1] * rad, p1[2] * rad, p1[3] * rad, p1[4] * rad]

        p2 = list(data[i + 1])
        p2.remove(p2[5])
        p2.remove(p2[5])

        pos1 = R.fkine(p1)
        pos2 = R.fkine(p2)
        i = i + 1
        n = 99
        step = np.linspace(pos1, pos2, n)
        step1 = step.tolist()
        for a in range(n):
            j, error = R.ikine(step1[a], j1, [1, 1, 0])
            # neu khong co loi
            if error == 0:
                cmd = 'G1x' + str(round(j[0], 4)) + 'y' + str(round(j[1], 4)) + 'z' + str(round(j[2], 4)) \
                      + 'a' + str(round(j[3], 4)) + 'b' + str(round(j[4] + 90 - j[3], 4)) + 'f' + str(
                    data[i - 1][6] * 200)
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
                      + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5]*200)
                gcode.append(cmd)
            else:
                print("error in " + str(i))
                break
    if data[i][4] == 'C2':
        p1 = list(data[i])
        A = [p1[0], p1[1]]

        p2 = list(data[i+1])
        B = [p2[0], p2[1]]

        p3 = list(data[i+2])
        C = [p3[0], p3[1]]

        tam, bk = C2(A, B, C)

        n = 100
        goc_cung = 360
        step = np.linspace(0, goc_cung * np.pi /180, n)
        x = []
        y = []
        for t in step:
            px = bk * np.cos(t) + tam[0]
            x.append(float(px))
        for t in step:
            py = bk * np.sin(t) + tam[1]
            y.append(float(py))
        for a in range(n):
            pos = [x[a], y[a], p1[2], p1[3]]
            j, error = R.ikine(pos, [1, 0])
            # neu khong co loi
            if error == 0:
                cmd = 'G0X' + str(round(j[0], 4)) + ' Y' + str(round(j[1], 4)) + ' Z' + str(round(j[2], 4)) \
                      + ' A' + str(round(j[3], 4)) + ' F' + str(data[i][5]*200)
                gcode.append(cmd)
            else:
                print("error in " + str(i))
                break
        i += 3
    [print(gcode[r]) for r in range(len(gcode))]
    print(len(gcode))
    return gcode, error, i
def C2(A, B, C):
    """
    %phuong trinh duong tron x**2 + y**2 -2ax - 2by + c = 0
    %trong do tam I(a,b), c = a**2 + b**2 -R**2
    %ban kinh R = Sqrt(a**2 + b**2 - c)
    """
    # A = [1, 0]
    # B = [0, 1]
    # C = [-1, 0]
    a, b, c = symbols('a b c')
    #%thay diem A B C vao ta co:
    pt1 = Eq(A[0]**2 + A[1]**2 - 2*a*A[0] - 2*b*A[1] + c, 0)
    pt2 = Eq(B[0]**2 +B[1]**2 - 2*a*B[0] - 2*b*B[1] + c, 0)
    pt3 = Eq(C[0]**2 + C[1]**2 - 2*a*C[0] - 2*b*C[1] + c, 0)
    S = linsolve([pt1, pt2, pt3], (a, b, c))
    # tam I
    tam = [S.args[0][0], S.args[0][1]]
    # bk R
    bk = sqrt(tam[0]**2 + tam[1]**2 - S.args[0][2])
    print(tam, bk)
    return tam, bk
# data = pg.read_from_db('chuongtrinh1')
# gc, err, i = RunStep('chuongtrinh1', 1)
# print(err, i)