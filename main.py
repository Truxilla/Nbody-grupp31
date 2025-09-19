from collections import namedtuple
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt

from planet import Planet
import solver

N = int(sys.argv[1])
filename = sys.argv[2]
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

timespan = (0, 10)
timeVector, result = solver.solveNbody(
    func=solver.particleForce,
    timespan=timespan,
    initialState=np.array(data),
    deltaTime=0.1
)


xs = [data[i].position[0] for i in range(N)]
ys = [data[i].position[1] for i in range(N)]
sizes = [72 * data[i].brightness for i in range(N)]

print(xs, ys)
xs += [1, 1, 0, 0]
ys += [1, 0, 1, 0]
sizes += [0, 0, 0, 0]
fig, ax = plt.subplots()
ax.scatter(xs, ys, sizes)
plt.show()
