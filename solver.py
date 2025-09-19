import numpy as np

epsilon = 0.001

def particleForce(
    i, currentState
):
    numberOfParticles = len(currentState)
    gravity = 100/numberOfParticles
    massI = currentState[i].mass

    totalForce = np.array([0, 0])
    for j in range(numberOfParticles):
        if i != j:
            massJ = currentState[j].mass
            xDifference = currentState[i].position[0] - currentState[j].position[0]
            yDifference = currentState[i].position[1] - currentState[j].position[1]
            distance = xDifference ^ 2 + yDifference ^ 2
            totalForce[0] += -gravity * massI * xDifference * (massJ / ((distance + epsilon) ^ 3))
            totalForce[1] += -gravity * massI * xDifference * (massJ / ((distance + epsilon) ^ 3))

    return totalForce


def particleAcceleration(i, initialState):
    return particleForce(i, initialState) / initialState[i].mass


def updateParticle(i, stateArray, deltaTime):



def solveNbody(func, timespan, initialState, deltaTime, *args):
    timeVector = np.arange(timespan[0], timespan[1], deltaTime)
    deltaTimeVector = np.ones_like(timeVector) * deltaTime

    if timeVector[-1] < timespan[1]:
        timeVector = np.append(timeVector, timespan[1])
        deltaTimeVector = np.append(
            deltaTimeVector, timeVector[-1] - timespan[-2]
        )

    outputVectorArray = np.zeros((len(timeVector), len(initialState)))
    outputVectorArray[0, :] = initialState

    for i in range(len(timeVector)):
        outputVectorArray[i+1] = particleForce(outputVectorArray[i])

    return timeVector, outputVectorArray
