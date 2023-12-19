import re
import cirq
import tqdm
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from noise._simplex import noise4

from quantum_circuit import *
from qn_random_num_gen import *

T = qn_random_float_generator_128(0, 2*np.pi)
R = np.array(qn_random_float_generator_128(0, 1))
P = np.zeros((points_num,2))

X,Y = P[:,0], P[:,1]
X[:] = R*np.cos(T)
Y[:] = R*np.sin(T)
intensity_inner = 1.001 - np.power(np.sqrt(X**2 + Y**2), 0.75)
intensity_outer = np.power(np.sqrt(X**2 + Y**2), 0.15)
X[:] = X*radius +  width//2
Y[:] = Y*radius + height//2

def update(*args):
    global P, time, pbar

    time += 2*0.002
    P_ = np.zeros((points_num,2))
    cos_t = 1.5*np.cos(2*np.pi*time)
    sin_t = 1.5*np.sin(2*np.pi*time)
    for i in range(points_num):
        x, y = P[i]
        dx = noise4(scale*x, scale*y, cos_t, sin_t, 2)
        dx *= length * (intensity_inner[i] + intensity_outer[i])
        dy = noise4(100+scale*x, 200+scale*y, cos_t, sin_t, 2)
        dy *= length * (intensity_inner[i] + intensity_outer[i])
        P_[i] = x + dx, y +dy
    pbar.update(1)
    scatter.set_offsets(P_)

# set background color
def set_background(color=''): # """#303030"""
    ax.set_facecolor(color)
    fig.set_facecolor(color)

fig = plt.figure(figsize=(7,7))
ax = plt.subplot(1,1,1, aspect=1, frameon=False)
scatter = plt.scatter(X, Y, s=1.5, edgecolor="none", facecolor="yellow", alpha=.55)

set_background(color='black')

ax.set_xticks([])
ax.set_yticks([])

ax.text(0.55, 1.11, "Quantum", size=30,
        name="Source Sans Pro", weight=600,
        ha="right", va="top", transform=ax.transAxes, color='white')
ax.text(0.55, 1.11 - 0.0025, " Creature", size=30,
        name="Source Sans Pro", weight=100,
        ha="left", va="top", transform=ax.transAxes, color='white')



anim = animation.FuncAnimation(fig, update, frames=frames, interval=60)
pbar = tqdm.tqdm(total=frames)
anim.save('qn_creature.gif', writer='imagemagick', fps=60)
pbar.close()
plt.show()

