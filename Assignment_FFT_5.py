import string
import numpy as np
from numpy import loadtxt
import dcst
import matplotlib.pyplot as plt
from cmath import exp, pi
from numpy import zeros
from numpy .fft import rfft, irfft
import argparse


#(a and b)


def rfft(a):
    N=len(a)
    c=zeros(N//2+1,complex)
    for k in range(N//2 +1):
        for n in range(N):
            c[k] +=a[n]*exp(-2j*pi*k*n*N)
    return c
a=np.loadtxt("dow.txt")
c=rfft(a)
plt.plot(a)
plt.xlabel('Business days')
plt.ylabel('Value')

plt.title('data plot for Dow Jones.txt')
print("Coefficient of Discrete FT is = ",c)




# (c)######
########

def fft_smooth_func(data,x):
    fft_coef=np.fft.rfft(data)
    remain_fft_coeff=fft_coef.size *x/100
    fft_coef[int(remain_fft_coeff):]=0
    return np.fft.irfft(fft_coef)

x=int(input("Enter percentage of coefficients to keep from raw dow data: "))
#####7.4(d)#########

x=int(10)
new_value_dow_c= fft_smooth_func(a,x)
plt.plot(new_value_dow_c)


## ####7.4(e)#### ####

x=int(2)
new_value_dow_e=fft_smooth_func(a,x)
plt.plot(new_value_dow_e)
plt.legend(["raw data(a)","smoothed data(d(10%))","smoothed data(e(2%))"])
print("\n\nCOMMENT(d): when we chnage the setting with fourier transrom coefficient to zero, it smooth the data(data points are less noisy).\n\n")


plt.show()



### problem(7.6)####
dow2=loadtxt("dow2.txt",float)
plt.plot(dow2)
x=int(2)
new_value_dow2=fft_smooth_func(dow2,x)
plt.plot(new_value_dow2)
plt.xlabel("Business days from 2004 to 2008")
plt.ylabel("Values")
plt.title("Dow2")
plt.legend(["Raw data for dow2","Smoothed Dow2(2%)"])

plt.show()

#### Discrete cosine transform 
def cosine_func(data, x):
    dct_coeff=dcst.dct(data)
    remaining_dct_coeff=dct_coeff.size * x/100
    dct_coeff[int(remaining_dct_coeff):]=0
    return dcst.idct(dct_coeff)
smoothed_dow2=fft_smooth_func(dow2,x)
smoothed_dow22=cosine_func(dow2,x)
plt.plot(dow2)
plt.xlabel('closing days')
plt.ylabel('closing values')
plt.plot(smoothed_dow22)
plt.legend('raw data','dct smoothed')
plt.xlabel('Closing days')
plt.title('Dicrete cosine transform to remove edge detortion ')
plt.show()







parser = argparse.ArgumentParser("Smooth the Dow closing values.")
parser.add_argument("dowfile", choices=['dow','dow2'], help="run with dow or dow2")
parser.add_argument("transform", choices=['dft','dct'], help="run with dft or dct")                                                                           
parser.add_argument("--percent","--p", type=int, default=10, help="percentage (integer value) of Fourier coefficients to keep, default is 10")
args = parser.parse_args()

dow_file = args.dowfile
transform_type = args.transform2
percent_val = args.percent
__name__=="__main__"

