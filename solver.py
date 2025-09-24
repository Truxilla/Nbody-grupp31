import copy
import numpy as np

from planet import Planet

epsilon = 0.001


def particleForce(
    i, stateArray, tickNumber
):
    numberOfParticles = len(stateArray[0])
    gravity = 100/numberOfParticles
    massI = stateArray[tickNumber - 1][i].mass

    totalForce = np.array([0.0, 0.0])
    for j in range(numberOfParticles):
        if i != j:
            massJ = stateArray[tickNumber - 1, j].mass
            xDifference = stateArray[tickNumber - 1, i].position[0] - stateArray[tickNumber - 1, j].position[0]
            yDifference = stateArray[tickNumber - 1, i].position[1] - stateArray[tickNumber - 1, j].position[1]
            distance = np.sqrt(xDifference ** 2 + yDifference ** 2)
            totalForce[0] += -gravity * massI * xDifference * (massJ / ((distance + epsilon) ** 3))
            totalForce[1] += -gravity * massI * yDifference * (massJ / ((distance + epsilon) ** 3))

    return totalForce


def particleAcceleration(i, stateArray, tickNumber):
    return particleForce(i, stateArray, tickNumber) / stateArray[tickNumber - 1, i].mass



def updateParticle(i, stateArray, tickNumber, deltaTime):
    stateArray[tickNumber, i] = copy.deepcopy(stateArray[tickNumber - 1, i])
    acceleration = particleAcceleration(i, stateArray, tickNumber)
    stateArray[tickNumber, i].velocity = stateArray[tickNumber - 1, i].velocity + acceleration * deltaTime
    stateArray[tickNumber, i].position = stateArray[tickNumber - 1, i].position + stateArray[tickNumber, i].velocity * deltaTime


def doTick(stateArray, tickNumber, deltaTime):
    for i in range(stateArray.shape[1]):
        updateParticle(i, stateArray, tickNumber, deltaTime)


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

    for tickNumber in range(1, len(timeVector)):
        doTick(outputVectorArray, tickNumber, deltaTime)

    return timeVector, outputVectorArray
