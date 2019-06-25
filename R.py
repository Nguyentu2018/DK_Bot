from math import sin,cos,atan2,pi
import numpy as np

def fkine2(joint, unit='deg'):
    if unit == 'deg':
        j = np.array(joint) * pi / 180
        j[2] = j[2] * 180 / pi
    if unit == 'rad':
        j = np.array(joint)
    tx = 350 * cos(j[0] + j[1]) + 350 * cos(j[0]) + (
                4967757600021511 * j[2] * sin(j[0] + j[1])) / 40564819207303340847894502572032
    ty = 350 * sin(j[0] + j[1]) + 350 * sin(j[0]) - (
                4967757600021511 * j[2] * cos(j[0] + j[1])) / 40564819207303340847894502572032
    tz = -j[2]

    ax = (4967757600021511*sin(j[0] + j[1]))/40564819207303340847894502572032
    ay = -(4967757600021511*cos(j[0] + j[1]))/40564819207303340847894502572032
    az = -1

    ox = sin(j[0] + j[1] - j[3])
    oy = -cos(j[0] + j[1] - j[3])
    oz = (4967757600021511*cos(j[3]))/40564819207303340847894502572032

    nx = cos(j[0] + j[1] - j[3])
    ny = sin(j[0] + j[1] - j[3])
    nz = (4967757600021511*sin(j[3]))/40564819207303340847894502572032

    T = np.array([[nx, ox, ax, tx],
                 [ny, oy, ay, ty],
                 [nz, oz, az, tz],
                 [0, 0, 0, 1]])
    # print(T)
    return T


def fkine(joint, unit='deg'):
    if unit == 'deg':
        j = np.array(joint) * pi/180
        j[2] = j[2]*180/pi
    if unit == 'rad':
        j = np.array(joint)
    x = 350*cos(j[0] + j[1]) + 350*cos(j[0]) + (4967757600021511*j[2]*sin(j[0] + j[1]))/40564819207303340847894502572032
    y = 350*sin(j[0] + j[1]) + 350*sin(j[0]) - (4967757600021511*j[2]*cos(j[0] + j[1]))/40564819207303340847894502572032
    z = -j[2]
    # print(x, y, z)
    return x, y, z


def ikine(position, otp, q4):
    tx = position[0]
    ty = position[1]
    tz = position[2]
    j = np.array([0, 0, 0, 0], float)

    if otp[0] == 1:
        j[0] = atan2(- tx ** 2 - ty ** 2,
                     (-(- tx ** 4 - 2 * tx ** 2 * ty ** 2 + 490000 * tx ** 2 - ty ** 4 + 490000 * ty ** 2) ** 0.5).real) - atan2(-tx, -ty)
    else:
        j[0]= - atan2(-tx, -ty) + atan2(- tx ** 2 - ty ** 2,
                                      ((- tx ** 4 - 2 * tx ** 2 * ty ** 2 + 490000 * tx ** 2 - ty ** 4 + 490000 * ty ** 2) ** 0.5).real)
    if j[0] > pi/2 or j[0] < -pi/2:
        j[0] = 2*pi + j[0]
    c1 = cos(j[0])
    s1 = sin(j[0])
    if otp[1] == 1:
        j[1] = - atan2(c1*tx + s1*ty - 350, c1*ty - s1*tx) + atan2(350, (-(tx**2 - 700*c1*tx + ty**2 - 700*s1*ty)**0.5).real)
    else:
        j[1] = - atan2(c1*tx + s1*ty - 350, c1*ty - s1*tx) + atan2(350, ((tx**2 - 700*c1*tx + ty**2 - 700*s1*ty)**0.5).real)
    c2 = cos(j[1])
    s2 = sin(j[1])

    j[2] = -tz * pi/180

    ax = (4967757600021511 * sin(j[0] + j[1])) / 40564819207303340847894502572032
    ay = -(4967757600021511 * cos(j[0] + j[1])) / 40564819207303340847894502572032
    if otp[2] == 1:
        j[3] = np.angle(-(c1 + s1*1j)*(c2 + s2*1j)*(ay + ax*1j))
        j[3] = j[3] + q4 * pi / 180
    else:
        j[3] = np.angle((c1 + s1*1j)*(c2 + s2*1j)*(ay + ax*1j))
        j[3] = j[3] + q4 * pi / 180
    if j[3] > pi or j[3] < -pi:
        j[3] = 2*pi + j[3]
    j = j*180/pi
    print(j)

# j = [90, 90, 50, -45]
# # t1 = time.time()
# fkine2([0, 0, 0, 0])
# # x, y, z = fkine(j)
# ikine([350, 350, -50],[1,0,1],0)
# # print(time.time()-t1)
# #
