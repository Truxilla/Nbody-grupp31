import copy
import numpy as np

from planet import Planet

epsilon = 0.001


def particleForce(
    i, N, masses, positions, velocities, tickNumber
):
    gravity = 100/N

    differences = -(positions[tickNumber - 1] - positions[tickNumber - 1, i])
    differences_squared = differences * differences

    distances_squared = differences_squared[:, 0] + differences_squared[:, 1]

    distances = np.sqrt(distances_squared)

    denominators = (distances + epsilon)**3
    x = masses/denominators
    result = x.reshape(N, 1) * differences

    # 0 force for j = i
    result[i] = result[i] * 0

    totalForce = np.sum(result, axis = 0)

    return totalForce * -gravity * masses[i]


def particleAcceleration(i, N, masses, positions, velocities, tickNumber):
    return particleForce(i, N, masses, positions, velocities, tickNumber) / masses[i]


def updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime):
    acceleration = particleAcceleration(i, N, masses, positions, velocities, tickNumber)
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
            deltaTimeVector, timeVector[-1] - timeVector[-2]
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

    positions = np.zeros((len(timeVector), N, 2), dtype=float)
    for i, p in zip(range(N), initialState):
        positions[0, i] = p.position

    velocities = np.zeros((len(timeVector), N, 2), dtype=float)
    for i, p in zip(range(N), initialState):
        velocities[0, i] = p.velocity

    for tickNumber in range(1, len(timeVector)):
        print(f"Tick {tickNumber}")
        doTick(N, masses, positions, velocities, tickNumber, deltaTimeVector[tickNumber])

    for tickNumber in range(1, len(timeVector)):
        for i in range(N):
            outputVectorArray[tickNumber, i] = Planet(
                positions[tickNumber, i],
                masses[i],
                velocities[tickNumber, i],
                brightnesses[i]
            )
    return timeVector, outputVectorArray
