from numpy import linspace
import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as ac



"""
The Lagrange points
GM/r**2-Gm/(R-r)**2 =w**2 *r
"""
m=7.348e22
R=3.844e8
w=2.662e-6
accuracy=1e-12
G = ac.G.value # Graviatational constant
M = ac.M_earth.value
w = 2.662e-6
R = 3.844e8



def lagrangel(x):
    return G*M/(x**2) - G*m/((R-x)**2) - (w**2)*x

def diff(f,x):
    h=1e-5
    return (f(x+(h/2))-f(x-(h/2)))/h

def newton(f, x, tol):
    while abs(f(x)) > tol:
        Dx = f(x)/diff(f,x)
        x2 = x - Dx
        x = x2
    return x

print("The Earth-Moon Lagrangian point L1(Newton method) is {:e} m".format(newton(lagrangel,R/2,accuracy)))