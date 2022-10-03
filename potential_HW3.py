import numpy as np
import matplotlib.pyplot as plt
import math


N=1000
q1=1# #charge +C
q2=-1# #charge -C
x=10 # in cm
y=0
# permittivity of free space
esp0=8.854e-12

# define the constant without relative distance of charge
# k=1/(4*math.pi*abs0) 
def potential_V(q1,q2,x,y):
    x1=np.sqrt((x+0.05)**2 + y**2)
    y1=np.sqrt((x-0.05)**2 + y**2)
    k1=1/(4*np.pi*esp0*x1)
    k2=1/(4*np.pi*esp0*y1)
    return q1/(k1) + q2/(k2)

ax1,ax2,Nx= -0.5,0.5,100
by1,by2,Ny= ax1,ax2,Nx

#define the potential array
V=[]

for j in np.linspace(by1,by2,Ny):
    row=[]
    for i in  np.linspace(ax1,ax2,Nx):
        row.append(potential_V(q1,q2,i,j))
    V.append(row)

V_pot=np.array(V)
plt.imshow(V_pot)
plt.title('test potential')
plt.xlabel('x')
plt.ylabel('y')


# def funcder(f,x,y): partial derivatives
#     def partial_x(f, x, y):
#         f(x+h/2,y)-f(x-h/2,y)


# Electric field calculation

def Par_diff(x,y,N):
    d_dx=[]
    d_dy=[]
    h=1e-5 #step size
    for j in np.linspace(by1,by2,N):
        row_x=[]
        row_y=[]
        for j in np.linspace(by1, by2, N):
            row_x.append((potential_V(q1,q2,i+h/2,j)- potential_V(q1,q2,i-h/2,j))/(-h))
            row_y.append((potential_V(q1,q2,i,j+h/2)- potential_V(q1,q2,i,j-h/2))/(-h))
        d_dx.append(row_x)
        d_dy.append(row_y)
    return np.array(d_dx), np.array(d_dy)
ex, ey=Par_diff(ax1,ax2,Ny)


#plot electric field
X, Y=np.meshgrid(np.linspace(ax1,ax2,Nx),np.linspace(by1, by2, Ny))
fig,axes=plt.subplots(nrows=1,ncols=2)
plt.subplots_adjust(hspace=0.5,wspace=0.5)
axes[0].imshow(V_pot)
axes[0].set_title('Calculated Potential for +C and -C')
axes[1].streamplot(X,Y,ex,ey)
axes[1].set_title('Calcuted electric field')
axes[0].set_xlabel('x (m)')
axes[1].set_xlabel('x (m)')
axes[0].set_ylabel('y (m)')
axes[1].set_ylabel('y (m)')



plt.show()