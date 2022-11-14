import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

np.random.seed(25)# number of random points

def generateRandomLines(dt, N):
    dX = np.sqrt(dt) * np.random.randn(1, N)
    X = np.cumsum(dX, axis=1)

    dY = np.sqrt(dt) * np.random.randn(1, N)
    Y = np.cumsum(dY, axis=1)

    lineData = np.vstack((X, Y))

    return lineData

# Returns Line2D objects
def updateLines(num, dataLines, lines):
    for u, v in zip(lines, dataLines):
        u.set_data(v[0:2, :num])

    return lines

N = 100# Number of points
T = 5.0
dt = T/(N-1)


fig, ax = plt.subplots()

data = [generateRandomLines(dt, N)]

ax = plt.axes(xlim=(-2.0, 2.0), ylim=(-3.0, 2.0) )

ax.set_xlabel('X(t)')
ax.set_ylabel('Y(t)')
ax.set_title('Brownian motion')

## Create a list of line2D objects
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1])[0] for dat in data]


## Create the animation object
anim = animation.FuncAnimation(fig, updateLines, N+1, fargs=(data, lines), 
interval=20, repeat=True, blit=False)

plt.tight_layout()
plt.show()