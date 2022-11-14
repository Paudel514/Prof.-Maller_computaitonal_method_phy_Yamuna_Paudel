import numpy as np
from scipy import integrate
import scipy.integrate as intergrate
from math import exp
from scipy.integrate import quad
from random import random

# a=1.0
# b=0.0
# N=1000
# h=(b-a)/N
# def integrand(x):
#     return ((x**(-1/2))//np.exp(x)+1)


# #given weight of function
# def weight_f(x):
#     return x**(-1/2)

# def prob_dist(x):
#     return 1/(2*x**(1/2))


# def prob_ran():
    # return (np.random.random())**2
#non-divergent integrand g(x)
# def gint(x):
#     return 1/(1+np.exp(x))


# given weight function w(x):
def fw(x):
    return x**(-1/2)

#probability distribution is represent as  p(x)
def fp(x):
    return 1/(2*x**(1/2))

#probability distro p(x) after transformation formula
def pdistro():
    return (np.random.random())**2

#original integrand f(x), divergent
def fint(x):
    return (x**(-1/2))/(1+np.exp(x))

#non-divergent integrand g(x)
def ndi(x): # ngi(non divergent integrand)
    return 1/(1+np.exp(x))

N = 1000000
Int = 0
wint = (integrate.quad(lambda x: fw(x), 0, 1)[0])
for i in range(N):
    x = pdistro()
    Int += 2*ndi(x)/N #integral(w(x))=2

print("The pdf p(x) is obtained from the weight w(x) as w(x)/integral(w(x)), where integral(w(x))=2 bw 0 and 1")
print("The transformation formula for p(x) is x(z)=z^2, with z uniform random number bw 0 and 1")
print("The integral computed with Monte Carlo with importance sampling is {}".format(Int))
print("The integral computed with scipy is {}".format(integrate.quad(lambda x: fint(x), 0, 1)[0]))