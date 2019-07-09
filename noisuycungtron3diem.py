import matplotlib.pyplot as plt
from sympy import Eq, linsolve, symbols
from math import sqrt

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
    I = [S.args[0][0], S.args[0][1]]
    # bk R
    R = sqrt(I[0]**2 + I[1]**2 - S.args[0][2])
    return I, R
    print(I, R)