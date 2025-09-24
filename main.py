import cProfile
import re
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt

from planet import Planet
import solver

filename = sys.argv[1]

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
        print(data[-1])

timespan = (0, 200 * DELTATIME)

#cProfile.run("""
timeVector, result = solver.solveNbody(
    func=solver.particleForce,
    timespan=timespan,
    initialState=np.array(data),
    deltaTime=DELTATIME
)#""")


xs = [data[i].position[0] for i in range(N)]
ys = [data[i].position[1] for i in range(N)]
sizes = [72 * data[i].brightness for i in range(N)]


with open(f"{'dst/' + 'change_me' + '_output.gal'}", 'wb') as o:
    for i in range(N):
        current = result[-1][i]
        writeable = struct.pack('dddddd', current.position[0], current.position[1], current.mass,
                                current.velocity[0], current.velocity[1], current.brightness)
        o.write(writeable)


# print(xs, ys)
# xs += [1, 1, 0, 0]
# ys += [1, 0, 1, 0]
# sizes += [0, 0, 0, 0]
# fig, ax = plt.subplots()
# ax.scatter(xs, ys, sizes)
# plt.show()
