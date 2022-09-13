import numpy as np
import matplotlib.pyplot as plt
a=np.array([1,2,3,4,5])# create from list
ones=np.ones(5,dtype=np.bool)#fill the values
z=np.zeros(5,dtype=np.float)#dtype can set the data type
t=np.full(5,3)#an array of fice 3s
x=np.arange(0,5,1)# step by 1
y=np.linspace(0,1,5)
print(a+5)
# next file
ones=np.ones([2,2],dtype=np.bool)# the shape can be the list
z=np.zeros((222),dtype=np.float)
t=np.full([5,2],3)
#line plot
x=np.linspace(0,2*np.pi,100)
y=np.sin(x)
plt.plot(x,y, color='green',linestyle='dashed')
plt.show()
plt.title('Trig Functions')