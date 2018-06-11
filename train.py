# TODO: Clean up code
# TODO: Advanced ML (previous matches, fatigue, performance)

# NOTE: Cannot separate data into train and test set because no past line data

import pickle
from sklearn import svm

matchDataInput = open('matchData.pkl', 'rb')
matchData = pickle.load(matchDataInput)
matchDataInput.close()

playerDataInput = open('playerData.pkl', 'rb')
playerData = pickle.load(playerDataInput)
playerDataInput.close()

inputs = []
outputs = []

projectWin = True
for match in matchData:
    idW = match["winnerId"]
    idL = match["loserId"]
    if idW in playerData and idL in playerData:
        nextInput = []

        if projectWin:
            nextInput.append(match["winnerElo"] /
                             (match["winnerElo"] + match["loserElo"]))
            nextInput.append(playerData[idW]["1st Serve Won %"])
            nextInput.append(playerData[idL]["1st Serve Won %"])
            nextInput.append(playerData[idW]["2nd Serve Won %"])
            nextInput.append(playerData[idL]["2nd Serve Won %"])
            nextInput.append(playerData[idW]["1st Srv. Return Won %"])
            nextInput.append(playerData[idL]["1st Srv. Return Won %"])
            nextInput.append(playerData[idW]["2nd Srv. Return Won %"])
            nextInput.append(playerData[idL]["2nd Srv. Return Won %"])
            outputs.append(1)
        else:
            nextInput.append(match["loserElo"] /
                             (match["winnerElo"] + match["loserElo"]))
            nextInput.append(playerData[idL]["1st Serve Won %"])
            nextInput.append(playerData[idW]["1st Serve Won %"])
            nextInput.append(playerData[idL]["2nd Serve Won %"])
            nextInput.append(playerData[idW]["2nd Serve Won %"])
            nextInput.append(playerData[idL]["1st Srv. Return Won %"])
            nextInput.append(playerData[idW]["1st Srv. Return Won %"])
            nextInput.append(playerData[idL]["2nd Srv. Return Won %"])
            nextInput.append(playerData[idW]["2nd Srv. Return Won %"])
            outputs.append(0)

        inputs.append(nextInput)
    projectWin = not projectWin

numFeatures = len(inputs[0])
numInputs = len(inputs)
minCol = [100] * numFeatures
maxCol = [-100] * numFeatures
for input in inputs:
    for i in range(0, numFeatures):
        if input[i] > maxCol[i]:
            maxCol[i] = input[i]
        if input[i] < minCol[i]:
            minCol[i] = input[i]

for i in range(0, numInputs):
    for j in range(0, numFeatures):
        inputs[i][j] = (inputs[i][j] - minCol[j]) / (maxCol[j] - minCol[j])

print(inputs[0:2])

model = svm.SVC()
model.probability = True
model.fit(inputs, outputs)

modelOutput = open('model.pkl', 'wb')
pickle.dump(model, modelOutput)
modelOutput.close()

offsetOutput = open('offset.pkl', 'wb')
pickle.dump({"min": minCol, "max": maxCol}, offsetOutput)
offsetOutput.close()

returnsOutput = open('returns.pkl', 'wb')
pickle.dump(0, returnsOutput)
returnsOutput.close()
