import copy
import numpy as np

from planet import Planet

epsilon = 0.001


def particleForce(
    i, N, masses, positions, velocities, tickNumber
):
    # numberOfParticles = len(stateArray[0])
    # gravity = 100/numberOfParticles
    gravity = 100/N
    # massI = stateArray[tickNumber - 1][i].mass
    massI = masses[i]

    totalForce = np.array([0.0, 0.0])
    for j in range(N):
        if i != j:
            massJ = masses[j]
            # xDifference = stateArray[tickNumber - 1, i].position[0] - stateArray[tickNumber - 1, j].position[0]
            # yDifference = stateArray[tickNumber - 1, i].position[1] - stateArray[tickNumber - 1, j].position[1]
            # distance = np.sqrt(xDifference ** 2 + yDifference ** 2)
            # totalForce[0] += -gravity * massI * xDifference * (massJ / ((distance + epsilon) ** 3))
            # totalForce[1] += -gravity * massI * yDifference * (massJ / ((distance + epsilon) ** 3))
            # difference = stateArray[tickNumber - 1, i].position - stateArray[tickNumber - 1, j].position
            difference = positions[tickNumber, i] - positions[tickNumber, j]
            distance = np.linalg.norm(difference)
            #print(gravity, massI, difference, massJ, distance, epsilon)
            totalForce += -gravity * massI * difference * difference * (massJ / ((distance + epsilon) ** 3))

    return totalForce


def particleAcceleration(i, N, masses, positions, velocities, tickNumber):
    return particleForce(i, N, masses, positions, velocities, tickNumber) / masses[i]


def updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime):
    acceleration = particleAcceleration(i, N, masses, positions, velocities, tickNumber - 1)
    velocities[tickNumber, i] = velocities[tickNumber - 1, i] + acceleration * deltaTime
    positions[tickNumber, i] = positions[tickNumber - 1, i] + velocities[tickNumber, i] * deltaTime
    # stateArray[tickNumber, i] = copy.deepcopy(stateArray[tickNumber - 1, i])
    # acceleration = particleAcceleration(i, stateArray, tickNumber)
    # stateArray[tickNumber, i].velocity = stateArray[tickNumber - 1, i].velocity + acceleration * deltaTime
    # stateArray[tickNumber, i].position = stateArray[tickNumber - 1, i].position + stateArray[tickNumber][i].velocity * deltaTime


def doTick(N, masses, positions, velocities, tickNumber, deltaTime):
    for i in range(N):
        updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime)


def solveNbody(func, timespan, initialState, deltaTime, *args):
    timeVector = np.arange(timespan[0], timespan[1], deltaTime)
    deltaTimeVector = np.ones_like(timeVector) * deltaTime

    if timeVector[-1] < timespan[1]:
        timeVector = np.append(timeVector, timespan[1])
        deltaTimeVector = np.append(
            deltaTimeVector, timeVector[-1] - timespan[-2]
        )

    outputVectorArray = np.zeros((len(timeVector), len(initialState)), dtype=object)
    outputVectorArray[0, :] = initialState
    print(outputVectorArray)

    N = len(initialState)
    masses = np.zeros(N, dtype=float)
    for i, p in zip(range(N), initialState):
        masses[i] = p.mass

    brightnesses = np.zeros(N, dtype=float)
    for i, p in zip(range(N), initialState):
        brightnesses[i] = p.brightness

    positions = np.zeros((len(timeVector), N, 2))
    for i, p in zip(range(N), initialState):
        positions[0, i] = p.position

    velocities = np.zeros((len(timeVector), N, 2))
    for i, p in zip(range(N), initialState):
        velocities[0, i] = p.velocity

    for tickNumber in range(1, len(timeVector)):
        print(f"Tick {tickNumber}")
        # doTick(outputVectorArray, tickNumber, deltaTime)
        doTick(N, masses, positions, velocities, tickNumber, deltaTime)

    for tickNumber in range(1, len(timeVector)):
        for i in range(N):
            outputVectorArray[tickNumber, i] = Planet(
                positions[tickNumber, i],
                masses[i],
                velocities[tickNumber, i],
                brightnesses[i]
            )
    return timeVector, outputVectorArray
