# Tennis Betting Algorithm Using Machine Learning

## Data.py

Scrapes web data from ultimatetennisstatistics. Data includes player constants, yearly performance, and recent matches.

## Train.py

For each match and set of opponents, use performance data and match result to create a model using SVM.

Problem: the performance data is present and includes the data from the recent matches.

## Predict.py

Given two players and the model, predict the winner and the likelihood of the prediction.

## Test.py

Store upcoming matches from ESPN and line data from bookmaker. On previously stored matches and lines, find the results on ESPN. Calculate the predicted winner and compare the prediction to the line.

Problem: Cannot split the test data into train and test data. Have to use forward data because no websites have historic line data.
