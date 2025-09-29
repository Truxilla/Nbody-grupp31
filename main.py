import re
import struct
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from planet import Planet
import solver


def readData(filename, N):
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
    return data


def writeResult(filename, N, result):
    with open(filename, 'wb') as o:
        for i in range(N):
            current = result[-1][i]
            writeable = struct.pack('dddddd', current.position[0], current.position[1], current.mass,
                                    current.velocity[0], current.velocity[1], current.brightness)
            o.write(writeable)


def createAnimation(filename, N, result, steps, sizeFunction):
    xs = [result[0][i].position[0] for i in range(N)]
    ys = [result[0][i].position[1] for i in range(N)]
    sizes = [sizeFunction(result[0][i]) for i in range(N)]

    fig, ax = plt.subplots()

    ax.axis([0, 1, 0, 1])
    ax.set_aspect("equal")
    sc = plt.scatter(x = xs, y = ys, s=sizes)

    def init():
        return sc,

    def animate(t):
        sc.set_offsets([result[t][i].position for i in range(N)])
        print(t)
        return sc,

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func = init,
        frames = steps,
        interval = 20,
        blit = True
    )


    anim.save(
        filename,
        writer = "ffmpeg",
        fps = 30
    )


def main():
    filename = sys.argv[1]

    STEPS = 200
    DELTATIME = 0.00001
    N = int(re.search(r"\w+_N_(\d+).gal", filename).group(1))
    print(filename)
    data = readData(filename, N)

    timespan = (0, STEPS * DELTATIME)
    result = solver.solveNbody(
        timespan=timespan,
        initialState=np.array(data),
        deltaTime=DELTATIME
    )

    writeResult('dst/change_me_output.gal', N, result)

    createAnimation(
        filename="simulation.mp4",
        N=N,
        result=result,
        steps=STEPS,
        sizeFunction=lambda planet: 10 * planet.mass ** (1/3)
    )


if __name__ == "__main__":
    main()
