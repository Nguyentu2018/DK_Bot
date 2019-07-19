import math
from math import sin, cos, atan2, pi, sqrt
import numpy as np
from robopy.base.transforms import tr2rpy

def fkine2(joint, unit='deg'):
    if unit == 'deg':
        j = np.array(joint) * pi / 180
    if unit == 'rad':
        j = np.array(joint)
    tx = (cos(j[1] - j[0] + j[2]) + cos(j[0] - j[1]) + (cos(j[0] + j[1]) + cos(j[0] + j[1] + j[2]))) * 125 - 55 * sin(j[0])
    ty = (sin(j[0] + j[1]) - sin(j[1] - j[0] + j[2]) + sin(j[0] - j[1]) + sin(j[0] + j[1] + j[2])) * 125 + 55 * cos(j[0])
    tz = 250 * (sin(j[1] + j[2]) + sin(j[1])) + 300

    nx = cos(j[4])*((81129638414606686663546605165575*cos(j[0] + j[1] + j[2] + j[3]))/162259276829213363391578010288128 + (81129638414606676728031405122553*cos(j[1] - j[0] + j[2] + j[3]))/162259276829213363391578010288128) - sin(j[4])*((403032377821159498335588895202304015643716683825*sin(j[0] + j[1] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 + (403032377821159448978357750059338280708391237583*sin(j[1] - j[0] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 - sin(j[0]))
    ny = cos(j[4])*((81129638414606686663546605165575*sin(j[0] + j[1] + j[2] + j[3]))/162259276829213363391578010288128 - (81129638414606676728031405122553*sin(j[1] - j[0] + j[2] + j[3]))/162259276829213363391578010288128) - sin(j[4])*((403032377821159448978357750059338280708391237583*cos(j[1] - j[0] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 - (403032377821159498335588895202304015643716683825*cos(j[0] + j[1] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 + cos(j[0]))
    nz = cos(j[4])*sin(j[1] + j[2] + j[3]) + sin(j[4])*((4967757600021511*cos(j[1] + j[2] + j[3]))/81129638414606681695789005144064 + 4967757600021511/81129638414606681695789005144064)

    ax = (81129638414606686663546605165575*sin(j[0] + j[1] + j[2] + j[3]))/162259276829213363391578010288128 + (81129638414606676728031405122553*sin(j[1] - j[0] + j[2] + j[3]))/162259276829213363391578010288128 + (4967757600021511*sin(j[0]))/81129638414606681695789005144064
    ay = (81129638414606676728031405122553*cos(j[1] - j[0] + j[2] + j[3]))/162259276829213363391578010288128 - (81129638414606686663546605165575*cos(j[0] + j[1] + j[2] + j[3]))/162259276829213363391578010288128 - (4967757600021511*cos(j[0]))/81129638414606681695789005144064
    az = 24678615572571482867467662723121/6582018229284824168619876730229402019930943462534319453394436096 - cos(j[1] + j[2] + j[3])

    ox = - sin(j[4])*((81129638414606686663546605165575*cos(j[0] + j[1] + j[2] + j[3]))/162259276829213363391578010288128 + (81129638414606676728031405122553*cos(j[1] - j[0] + j[2] + j[3]))/162259276829213363391578010288128) - cos(j[4])*((403032377821159498335588895202304015643716683825*sin(j[0] + j[1] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 + (403032377821159448978357750059338280708391237583*sin(j[1] - j[0] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 - sin(j[0]))
    oy = - (sin(j[4])*(81129638414606686663546605165575*sin(j[0] + j[1] + j[2] + j[3]) - 81129638414606676728031405122553*sin(j[1] - j[0] + j[2] + j[3])))/162259276829213363391578010288128 - cos(j[4])*((403032377821159448978357750059338280708391237583*cos(j[1] - j[0] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 - (403032377821159498335588895202304015643716683825*cos(j[0] + j[1] + j[2] + j[3]))/13164036458569648337239753460458804039861886925068638906788872192 + cos(j[0]))
    oz = cos(j[4])*((4967757600021511*cos(j[1] + j[2] + j[3]))/81129638414606681695789005144064 + 4967757600021511/81129638414606681695789005144064) - sin(j[4])*sin(j[1] + j[2] + j[3])
 

    T = np.array([[nx, ox, ax, tx],
                 [ny, oy, ay, ty],
                 [nz, oz, az, tz],
                 [0, 0, 0, 1]])
    return T


def fkine(joint, unit='deg'):
    if unit == 'deg':
        j = np.array(joint) * pi/180
    if unit == 'rad':
        j = np.array(joint)
    tx = (cos(j[1] - j[0] + j[2]) + cos(j[0] - j[1]) + (cos(j[0] + j[1]) + cos(j[0] + j[1] + j[2]))) * 125 - 55 * sin(
        j[0])
    ty = (sin(j[0] + j[1]) - sin(j[1] - j[0] + j[2]) + sin(j[0] - j[1]) + sin(j[0] + j[1] + j[2])) * 125 + 55 * cos(
        j[0])
    tz = 250 * (sin(j[1] + j[2]) + sin(j[1])) + 300
    pos = np.array([tx, ty, tz], float)
    return pos


def ikine(position, qlast, otp):
    tx = position[0]
    ty = position[1]
    tz = position[2]
    # roll = position[3]
    j = np.array([0, 0, 0, 0, 0], float)

    if otp[0] == 1:
        j[0] = - atan2(-ty, tx) + atan2(-55.0, -sqrt(tx**2+ty**2-3025.0).real)
    else:
        j[0] = - atan2(-ty, tx) + atan2(-55.0, sqrt(tx**2+ty**2-3025.0).real)
    # if j[0] > pi/2 or j[0] < -pi/2:
    #     j[0] = 2*pi + j[0]
    C1 = cos(j[0])
    S1 = sin(j[0])
    if otp[1] == 1:
        j[1] = atan2(tz*6.0e2-ty**2-tz**2-C1**2*tx**2+C1**2*ty**2-C1*S1*tx*ty*2.0-9.0e4, (-sqrt(tz*-4.2e7-ty**2*tz**2*2.0+ty**2*tz*1.2e3-ty**2*1.8e5-ty**4-tz**2*2.9e5+tz**3*1.2e3-tz**4+C1**2*tx**2*7.0e4-C1**4*tx**4+C1**2*ty**2*6.8e5+C1**2*ty**4*2.0-C1**4*ty**2*7.5e5-C1**4*ty**4+C1**6*ty**2*2.5e5+S1**6*ty**2*2.5e5+C1**2*tx**2*tz*1.2e3-C1**2*ty**2*tz*1.2e3-C1**2*tx**2*ty**2*6.0+C1**4*tx**2*ty**2*6.0-C1**2*tx**2*tz**2*2.0+C1**2*ty**2*tz**2*2.0-C1*S1*tx*ty**3*4.0+C1*S1**3*tx*ty*5.0e5+C1**3*S1*tx*ty*5.0e5+C1**3*S1*tx*ty**3*4.0-C1**3*S1*tx**3*ty*4.0-C1*S1*tx*ty*3.6e5+C1*S1*tx*ty*tz*2.4e3-C1*S1*tx*ty*tz**2*4.0+1.44e10)).real)-atan2(C1*tx*-5.0e2-S1**3*ty*5.0e2-C1**2*S1*ty*5.0e2, tz*-5.0e2+1.5e5)
    else:
        j[1] = atan2(tz*6.0e2-ty**2-tz**2-C1**2*tx**2+C1**2*ty**2-C1*S1*tx*ty*2.0-9.0e4, (sqrt(tz*-4.2e7-ty**2*tz**2*2.0+ty**2*tz*1.2e3-ty**2*1.8e5-ty**4-tz**2*2.9e5+tz**3*1.2e3-tz**4+C1**2*tx**2*7.0e4-C1**4*tx**4+C1**2*ty**2*6.8e5+C1**2*ty**4*2.0-C1**4*ty**2*7.5e5-C1**4*ty**4+C1**6*ty**2*2.5e5+S1**6*ty**2*2.5e5+C1**2*tx**2*tz*1.2e3-C1**2*ty**2*tz*1.2e3-C1**2*tx**2*ty**2*6.0+C1**4*tx**2*ty**2*6.0-C1**2*tx**2*tz**2*2.0+C1**2*ty**2*tz**2*2.0-C1*S1*tx*ty**3*4.0+C1*S1**3*tx*ty*5.0e5+C1**3*S1*tx*ty*5.0e5+C1**3*S1*tx*ty**3*4.0-C1**3*S1*tx**3*ty*4.0-C1*S1*tx*ty*3.6e5+C1*S1*tx*ty*tz*2.4e3-C1*S1*tx*ty*tz**2*4.0+1.44e10)).real)-atan2(C1*tx*-5.0e2-S1**3*ty*5.0e2-C1**2*S1*ty*5.0e2, tz*-5.0e2+1.5e5)
    # if j[1]>135*pi/180:
    #     j[1] = j[1] - 360*pi/180

    C2 = cos(j[1])
    S2 = sin(j[1])

    if otp[2] == 1:
        j[2] = atan2(2.5e2, (-sqrt(S2*1.5e5-tz*6.0e2-S2*tz*5.0e2+ty**2+tz**2+C1**2*tx**2-C1**2*ty**2-C1*C2*tx*5.0e2-C2*S1*ty*5.0e2+C1*S1*tx*ty*2.0+9.0e4)).real)-atan2(S2*-3.0e2+S2*tz+C1*C2*tx+C2*S1*ty-2.5e2, C2*-3.0e2+C2*tz-C1*S2*tx-S1*S2*ty)
    else:
        j[2] = atan2(2.5e2, (sqrt(S2*1.5e5-tz*6.0e2-S2*tz*5.0e2+ty**2+tz**2+C1**2*tx**2-C1**2*ty**2-C1*C2*tx*5.0e2-C2*S1*ty*5.0e2+C1*S1*tx*ty*2.0+9.0e4)).real)-atan2(S2*-3.0e2+S2*tz+C1*C2*tx+C2*S1*ty-2.5e2, C2*-3.0e2+C2*tz-C1*S2*tx-S1*S2*ty)
    if j[2]>135*pi/180 or j[2]<-135*pi/180:
        j[2] = j[2] - 2*pi
        print("erro2")

    o123 = qlast[1] + qlast[2] + qlast[3]
    o04 = qlast[4] - qlast[0]
    j[3] = -j[2] - j[1] + o123
    j[4] = j[0] + o04

    j = j * 180 / pi

    limit = checkLimit(j, position)
    return j, limit

def checkLimit(joint, position):
    min = np.array([-180, -45, -135, -90, -180], float)
    max = np.array([180, 225, 135, 270, 180], float)
    j = joint
    posOld = np.array([position[0], position[1], position[2]], float)
    for i in range(0, 4):
        if j[i] >= min[i] and j[i] <= max[i]:
            if i == 3:
                limit = False
        else:
            print('j[' + str(i) + '] is limit')
            limit = True
            break
    posNew = fkine(j)

    c = abs(posOld-posNew)
    lm = 0
    for i in range(0, 3):
        if c[i] > 1:
            lm = lm+1
        if lm > 1:
            limit = True
            print('limit Carter ' + str(i))
    return limit

# vl = [0, 0, 0, 0, 0]
# a, limit = ikine([350, 55.0, 250], vl, [0, 0, 0])
# b = fkine2(a)
# rpy = tr2rpy(b, 'deg', 'xyz')
# print(a)
# print(b, limit)
# print(rpy[0, 2])