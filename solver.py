import numpy as np

from planet import Planet

epsilon = 0.001


def particleAcceleration(
    i, N, masses, positions, tickNumber
):
    gravity = 100/N

    differences = positions[tickNumber - 1, i] - positions[tickNumber - 1]

    distances_squared = np.einsum("ij,ij->i", differences, differences)
    distances = np.sqrt(distances_squared) + epsilon

    denominators = 1/(distances * distances**2)
    x = masses * denominators

    totalForce = np.einsum("i, ij->j", x, differences)

    return -gravity * totalForce


def updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime):
    acceleration = particleAcceleration(i, N, masses, positions, tickNumber)
    velocities[tickNumber, i] = velocities[tickNumber - 1, i] + acceleration * deltaTime
    positions[tickNumber, i] = positions[tickNumber - 1, i] + velocities[tickNumber, i] * deltaTime


def c1(N, masses, positions, velocities, tickNumber, deltaTime):
    gravity = 100/N
    differences = positions[tickNumber - 1][:, np.newaxis] - positions[tickNumber - 1]
    distances_squared = np.einsum("...ij,...ij->...i", differences, differences)
    distances = (np.sqrt(distances_squared) + epsilon)

    denominators = 1/(distances * distances**2)
    x = masses * denominators

    acceleration = np.einsum("...i, ...ij->...j", x, differences)

    velocities[tickNumber] = velocities[tickNumber - 1] + acceleration * -gravity * deltaTime
    positions[tickNumber] = positions[tickNumber - 1] + velocities[tickNumber] * deltaTime

def c2(N, masses, positions, velocities, tickNumber, deltaTime):
    for i in range(N):
        updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime)


def doTick(N, masses, positions, velocities, tickNumber, deltaTime):
    #c1(N, masses, positions, velocities, tickNumber, deltaTime)
    c2(N, masses, positions, velocities, tickNumber, deltaTime)


    # differences = np.einsum("")
    # for i in range(N):
    #     pass
        #updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime)

        #x = np.einsum("ij,kl ->ikjl", positions[tickNumber - 1], neg_positions)
        # print(x.shape)
        # differences = differences
        # print(neg_positions)
        # print(positions[tickNumber - 1, i])
        # print(differences)
        # print(differences.shape)
        # exit(1)
        # differences = positions[tickNumber - 1, i] + neg_positions


        # return -gravity * totalForce
        # acceleration = particleAcceleration(i, N, masses, positions, tickNumber)


def solveNbody(timespan, initialState, deltaTime, *args):
    timeVector = np.arange(timespan[0], timespan[1], deltaTime)
    deltaTimeVector = np.ones_like(timeVector) * deltaTime

    if timeVector[-1] < timespan[1]:
        timeVector = np.append(timeVector, timespan[1])
        deltaTimeVector = np.append(
            deltaTimeVector, timeVector[-1] - timeVector[-2]
        )

    outputVectorArray = np.zeros((len(timeVector), len(initialState)), dtype=object)
    outputVectorArray[0, :] = initialState

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
