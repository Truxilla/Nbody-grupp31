import numpy as np

from planet import Planet

epsilon = 0.001


def particleAcceleration(i, N, masses, positions, tickNumber):
    gravity = 100/N

    # Calculate differences in position (r) between particle i and each particle
    # as an array of vectors [[xDiff1, yDiff1], [xDiff2, yDiff2], ...]
    differences = -(positions[tickNumber - 1] - positions[tickNumber - 1, i])

    # Calculate the distance from i to each other particle
    differences_squared = differences * differences
    distances_squared = differences_squared[:, 0] + differences_squared[:, 1]
    distances = np.sqrt(distances_squared)

    # Calculate the force for each particle on i
    denominators = (distances + epsilon)**3
    x = masses/denominators
    forces = x.reshape(N, 1) * differences

    # 0 force for j = i
    forces[i] = forces[i] * 0

    # Sum the per-particle forces to get the total force for the particle
    totalForce = np.sum(forces, axis = 0)

    return totalForce * -gravity


def updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime):
    acceleration = particleAcceleration(i, N, masses, positions, tickNumber)
    # v_i = v_(i-1) + a_i * dt
    velocities[tickNumber, i] = velocities[tickNumber - 1, i] + acceleration * deltaTime
    # s_i = s_(i-1) + v_i * dt
    positions[tickNumber, i] = positions[tickNumber - 1, i] + velocities[tickNumber, i] * deltaTime


def doTick(N, masses, positions, velocities, tickNumber, deltaTime):
    for i in range(N):
        updateParticle(i, N, masses, positions, velocities, tickNumber, deltaTime)


def solveNbody(timespan, initialState, deltaTime):
    timeVector = np.arange(timespan[0], timespan[1], deltaTime)
    deltaTimeVector = np.ones_like(timeVector) * deltaTime

    if timeVector[-1] < timespan[1]:
        timeVector = np.append(timeVector, timespan[1])
        deltaTimeVector = np.append(
            deltaTimeVector, timeVector[-1] - timeVector[-2]
        )

    outputVectorArray = np.zeros((len(timeVector), len(initialState)), dtype=object)
    outputVectorArray[0, :] = initialState

    # Amount of planets/stars
    N = len(initialState)

    # Create a table where masses[i] is the mass of the i:th body
    masses = np.zeros(N, dtype=float)
    for i, p in zip(range(N), initialState):
        masses[i] = p.mass

    # Create a table where brightnesses[i] is the brightness of the i:th body
    brightnesses = np.zeros(N, dtype=float)
    for i, p in zip(range(N), initialState):
        brightnesses[i] = p.brightness

    # Create a table where positions[t, i] is the position [x, y] of the i:th body after t time steps
    # and fill it with the initial state t = 0
    positions = np.zeros((len(timeVector), N, 2), dtype=float)
    for i, p in zip(range(N), initialState):
        positions[0, i] = p.position

    # Create a table where velocities[t, i] is the velocity [vx, vy] of the i:th body after t time steps
    # and fill it with the initial state t = 0
    velocities = np.zeros((len(timeVector), N, 2), dtype=float)
    for i, p in zip(range(N), initialState):
        velocities[0, i] = p.velocity

    for tickNumber in range(1, len(timeVector)):
        # Perform the actual computations
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

    return outputVectorArray


def particleAccelerationOptimized(i, N, masses, positions, tickNumber):
    """ Slightly faster version (~40%) of particleAcceleration
        which was used to generate some of the longer simulation
        and simulations with more objects.
        It basically works the same as particleAcceleration but uses
        np.einsum to speed up some array operations.
    """
    gravity = 100/N

    # Calculate differences in position (r) between particle i and each particle
    # as an array of vectors [[xDiff1, yDiff1], [xDiff2, yDiff2], ...]
    differences = positions[tickNumber - 1, i] - positions[tickNumber - 1]

    # First compute xDiff^2+yDiff^2 for each difference and then
    # Take the square root to get an array of the distances from
    # i to each particle
    distances_squared = np.einsum("ij,ij->i", differences, differences)
    distances = np.sqrt(distances_squared) + epsilon

    # Calculate m_j/r^3 for each particle
    denominators = 1/(distances * distances**2)
    x = masses * denominators

    # Calculate the gravitational acceleration exerted on the particle by each
    # other particle and sum the result to get the total acceleration
    totalForce = np.einsum("i, ij->j", x, differences)

    return -gravity * totalForce
