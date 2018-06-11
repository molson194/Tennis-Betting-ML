import pickle


def predict(id1, id2):
    modelInput = open('model.pkl', 'rb')
    model = pickle.load(modelInput)
    modelInput.close()

    offsetInput = open('offset.pkl', 'rb')
    offset = pickle.load(offsetInput)
    offsetInput.close()

    minCol = offset["min"]
    maxCol = offset["max"]

    playerDataInput = open('playerData.pkl', 'rb')
    playerData = pickle.load(playerDataInput)
    playerDataInput.close()

    if id1 in playerData and id2 in playerData:
        pt = []
        pt.append(playerData[id1]["Current Elo Rank"] /
                  (playerData[id1]["Current Elo Rank"] +
                   playerData[id2]["Current Elo Rank"]))
        pt.append(playerData[id1]["1st Serve Won %"])
        pt.append(playerData[id2]["1st Serve Won %"])
        pt.append(playerData[id1]["2nd Serve Won %"])
        pt.append(playerData[id2]["2nd Serve Won %"])
        pt.append(playerData[id1]["1st Srv. Return Won %"])
        pt.append(playerData[id2]["1st Srv. Return Won %"])
        pt.append(playerData[id1]["2nd Srv. Return Won %"])
        pt.append(playerData[id2]["2nd Srv. Return Won %"])

        for i in range(0, len(pt)):
            pt[i] = (pt[i] - minCol[i]) / (maxCol[i] - minCol[i])

        pred = model.predict([pt])
        prob = model.predict_proba([pt])

        # print('Prediction: ', end="")
        # print(id1)
        # print(id2)
        # print(pred)
        # print('Probability: ', end="")
        # print(prob[0][pred[0]])
        return prob[0][pred[0]]
    else:
        print("Player IDs not valid")
        return 0
