import pandas as pd
from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction

pEnergies = []
for i in range(1, 3):
    data = pd.read_csv(f'Test/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)
for e in d.Values:
    print (e, d.Values[e])