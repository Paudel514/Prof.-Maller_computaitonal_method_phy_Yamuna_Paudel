import numpy as np
import math
from math import exp
import matplotlib.pyplot as plt

# define the function
def f(x):
    return math.exp(-x**2)
# N=100
a1=0.0
b1=3
dx=0.1 #N=(b1-a1)/dx
# dx1=(b1-a1)/N
N=int((b1-a1)/dx)


#Trapzoide method
s1=dx*(f(a1)+f(b1))/2
for n in range(1,N):
    s1 +=f(a1+n*dx)
print(s1*dx)


# Simpson's rule
s12=dx*(f(a1)+f(b1))/3
for k in range(1,int(N/2)):
    s12 +=4*f(a1+(2*k-1)*dx)
for k in range(1,int(N/2-1)):
    s12 +=2*f(a1+2*k*dx)
integral=s12*dx/3
print(integral)


# plot E(x) as a function of x(upper limit of integrand)
def int_simp(x11):
    N1=1000
    a=0.0
    dx1=(x11-0.0)/N
    s11=(1/3)*f(a) + (1/3)*f(x11)
    for k11 in range(1,int(N1/2)):
        s11 +=4*f(a1+(2*k-1)*dx1)
    for k11 in range(1,int(N/2-1)):
        s11 +=2*f(a+2*k11*dx1)
    return(s11*dx1/3)
x=np.arange(0,3,0.1)
y=[int_simp(i) for i in x]
plt.plot(x,y)

# axes label
plt.xlabel('X')
plt.ylabel('E(x)')
plt.title('Plot E(x) as function of upper limit of  integrand')

# visualization
plt.show()






   






