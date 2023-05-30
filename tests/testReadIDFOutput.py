import pandas as pd
from probabilistic.energy_predictions import EnergyPrediction, ProbabilisticEnergyPrediction

pEnergies = []
for i in range(10):
    data = pd.read_csv(f'Test/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)
print (', '.join(f'{x:.04}' for x in d.Values['Total'].loc[0]))