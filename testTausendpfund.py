import json
import os
import numpy as np
from Helper.Modules import *
from Helper.IDFHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass

with open(f'{os.getcwd()}/Tausendpfund.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

InitialiseZoneSurfaces(epObjects)
SetInternalMass(epObjects)

externalSurfaceArea = sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])
netVolume = sum([x.NetVolume for x in epObjects if isinstance(x, Zone)])
ach = round(0.1 + 0.07 * 6 * externalSurfaceArea / (0.8 * netVolume), 5)
for zoneList in list(x for x in epObjects if isinstance(x, (ZoneList))):
    epObjects += [zoneList.GetPeopleObject(20)]
    epObjects += [zoneList.GetLightsObject(6)]
    epObjects += [zoneList.GetElectricEquipmentObject(10)]
    epObjects += [zoneList.GetInfiltrationObject(ach)]
    epObjects += [zoneList.GetDefaultVentilationObject()]
    epObjects += [zoneList.GetNaturalVentilationObject()]

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = "Office"
    epObjects += [hvac]

from Probabilistic.Parameter import ProbabilisticParameters
nSamples = 100

print ('Generating Samples...')
pps = ProbabilisticParameters.ReadCsv('Probabilistic/1.csv')
samples = pps.GenerateSamplesAsDF(nSamples,)

print ('Generating IDF files...')
for i, sample in samples.iterrows():
    objs = list(epObjects)
    
    CreateConstructions(sample, objs)
    SetBestMatchConstruction(objs)

    with open(f'Test/IDFFiles/{i}.idf', 'w') as f:
        f.write('\n'.join((x.IDF for x in objs)))

print ('Simulating IDF files...')
import os
os.system(f'python3 runEP.py {os.getcwd()}/Test')

print ('Reading IDF files...')
import pandas as pd
from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction

pEnergies = []
for i in range(nSamples):
    data = pd.read_csv(f'Test/IDFFiles/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)

print ('Training regressor...')
from MLModels.Helper import TrainGenerator, TrainRegressor
from MLModels.Regressor import GetScalingLayer

col = ["NN", "RC", "LR",]
N1 = [5, 10, 20,]
N2 = [0, 5, 10,]
RC = [1e-3, 3e-4, 1e-4,]
LR = [1e-3, 3e-4, 1e-4,]

nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
hyperparameters = pd.DataFrame([[n, r, l,] 
                                    for n in nn
                                    for r in RC
                                    for l in LR
                                ], columns = col).sample(n=4,)
hyperparameters.index = range(len(hyperparameters))

r = TrainRegressor(hyperparameters[:4], samples, d.Values['Total'], f'Test/MLModel/Regressor', scalingDF_X=pps.GetScalingDF() , training=False)

print ('Training generator...')
targetValues = np.array([d.Values['Total'].loc[0] for _ in range(100)])
m = TrainGenerator(hyperparameters, 25, samples.columns, f'Test/MLModel/Generator', f'{r.FilePath}.h5', targetValues, GetScalingLayer(samples, scaledDF=pps.GetScalingDF(), reverse=True), True)

print ('Determining parameters...')
dfs = m.Predict(100,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

print (samples.head(1))