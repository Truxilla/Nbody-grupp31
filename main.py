import re
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from planet import Planet
import solver

filename = sys.argv[1]

STEPS = 200
DELTATIME = 0.00001
N = int(re.search(r"\w+_N_(\d+).gal", filename).group(1))
print(filename)


data = []
with open(f"{filename}", "rb") as f:
    for i in range(N):
        (x, y, mass, vx, vy, brightness) = struct.unpack('dddddd', f.read(8*6))
        data.append(
            Planet(
                np.array([x, y]),
                mass,
                np.array([vx, vy]),
                brightness
            )
        )


timespan = (0, STEPS * DELTATIME)
timeVector, result = solver.solveNbody(
    timespan=timespan,
    initialState=np.array(data),
    deltaTime=DELTATIME
)


xs = [data[i].position[0] for i in range(N)]
ys = [data[i].position[1] for i in range(N)]
sizes = [72 * data[i].brightness for i in range(N)]


with open(f"{'dst/' + 'change_me' + '_output.gal'}", 'wb') as o:
    for i in range(N):
        current = result[-1][i]
        writeable = struct.pack('dddddd', current.position[0], current.position[1], current.mass,
                                current.velocity[0], current.velocity[1], current.brightness)
        o.write(writeable)


fig, ax = plt.subplots()

ax.axis([0, 1, 0, 1])
sc = plt.scatter(x = xs, y = ys)

def init():
    return sc,

def animate(t):
    sc.set_offsets(np.array([result[t][i].position for i in range(N)]))

    return sc,

anim = animation.FuncAnimation(
    fig,
    animate,
    init_func = init,
    frames = 200,
    interval = 20,
    blit = True
)


anim.save(
    "simulation.mp4",
    writer = "ffmpeg",
    fps = 30
)
