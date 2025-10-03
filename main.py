import re
import struct
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from planet import Planet
import solver


def readData(filename, N):
    # Create an array that will hold all the data read from the input file
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
            # The last tick for the i:th body
            current = result[-1][i]
            # Packs the six fields as six doubles to write to the output file
            writeable = struct.pack('dddddd', current.position[0], current.position[1], current.mass,
                                    current.velocity[0], current.velocity[1], current.brightness)
            o.write(writeable)


def createAnimation(filename, N, result, steps, sizeFunction, fps):
    xs = [result[0][i].position[0] for i in range(N)]
    ys = [result[0][i].position[1] for i in range(N)]
    sizes = [sizeFunction(result[0][i]) for i in range(N)]

    fig, ax = plt.subplots(figsize=(4.8, 4.8), dpi=200)
    fig.tight_layout()

    ax.axis([0, 1, 0, 1])
    ax.set_aspect("equal")
    sc = plt.scatter(x = xs, y = ys, s=sizes, edgecolors="none")

    def init():
        return sc,

    def animate(t):
        sc.set_offsets([result[t][i].position for i in range(N)])
        print(f"Frame {t + 1}/{steps}")
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
        writer="ffmpeg",
        fps=fps
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("steps", nargs="?", default=200, type=int)
    parser.add_argument("-a", "--animate", type=str)
    parser.add_argument("-m", "--mass", action="store_true")
    parser.add_argument("-s", "--scale", type=float, default=25)
    parser.add_argument("-o", "--outfile", type=str)
    parser.add_argument("-f", "--fps", type=int, default=60)
    parser.add_argument("-d", "--deltatime", type=float, default=0.00001)
    args = parser.parse_args()

    filename = args.filename

    # Parses the number of planets from the filename
    N = int(re.search(r"\w+_N_(\d+).gal", filename).group(1))

    data = readData(filename, N)

    timespan = (0, args.steps * args.deltatime)
    result = solver.solveNbody(
        timespan=timespan,
        initialState=np.array(data),
        deltaTime=args.deltatime
    )

    if args.outfile:
        writeResult(args.outfile, N, result)

    if args.animate:
        if args.mass:
            sizeFunction = lambda planet: args.scale * planet.mass ** (1/3)
        else:
            sizeFunction = lambda planet: args.scale * planet.brightness

        createAnimation(
            filename=args.animate,
            N=N,
            result=result,
            steps=args.steps+1,
            sizeFunction=sizeFunction,
            fps=args.fps
        )


if __name__ == "__main__":
    main()
