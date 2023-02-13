import json

from Helper.Modules import *
from Helper.IDFHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass

with open('Test/Tausendpfund.json') as f:
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
nSamples = 50

print ('Generating Samples...')
pps = ProbabilisticParameters.ReadCsv('Probabilistic/1.csv')
samples = pps.GenerateSamplesAsDF(nSamples,)

print ('Generating IDF files...')
for i, sample in samples.iterrows():
    objs = list(epObjects)
    
    CreateConstructions(sample, objs)
    SetBestMatchConstruction(objs)

    with open(f'Test/{i}.idf', 'w') as f:
        f.write('\n'.join((x.IDF for x in objs)))

print ('Simulating IDF files...')
import os
os.system('python3 runEP.py /Users/manav/repos/EPObjects/Test/')

print ('Reading IDF files...')
import pandas as pd
from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction

pEnergies = []
for i in range(nSamples):
    data = pd.read_csv(f'Test/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)

print ('Training regressor...')
from MLModels.Generator import Generator, TrainRegressor
from MLModels.MLModel import GetScalingLayer

col = ["NN", "RC", "LR",]
N1 = [50, 100, 200]
N2 = [0,]
REG = [1e-03, 1e-05, 1e-07]
LR = [1e-03, 1e-04, 1e-05]

nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
hyperparameters = pd.DataFrame([[n, r, l,] 
                                    for n in nn
                                    for r in REG
                                    for l in LR
                                ], columns = col).sample(n=8,)

TrainRegressor(hyperparameters, samples, d.Values['Total'], f'Test/MLModel/Regressor')

print ('Training generator...')
m = Generator(10, len(samples.columns), f'Test/MLModel/Generator')
m.TuneHyperparameters(hyperparameters, f'Test/MLModel/Regressor.h5', d.Values['Total'].loc[[0]], GetScalingLayer(samples, True))

print ('Determining parameters...')
import numpy as np

dfs = pd.DataFrame(columns=samples.columns)
for i in range(50):
    ar = m.Predict(100, i).mean(axis=0)
    dfs.loc[i] = ar

for p in dfs.columns:
    print (p, np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 97.5))

print (samples.head(1))