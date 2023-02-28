import json
import os
import numpy as np

from EPLogger import Logger

from Helper.Modules import *
from Helper.IDFHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass, SetReportingFrequency
from Helper.ScheduleHelper import CreateOfficeSchedule, DefaultOfficeSchedules

from EnumTypes import Frequency

import pandas as pd
from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction

RepoPath = '/home/ubuntu/repos/EPObjects/'

simulate, trainRegressor, trainGenerator = True, True, True

with open(f'{os.getcwd()}/Tausendpfund.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

# SetReportingFrequency(epObjects, Frequency.Annual)

InitialiseZoneSurfaces(epObjects)
SetInternalMass(epObjects, 30)
epObjects += list(CreateOfficeSchedule(2017, DefaultOfficeSchedules, f'{RepoPath}/Test/IDFFiles/Schedule.txt'))

externalSurfaceArea = sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])
netVolume = sum([x.NetVolume for x in epObjects if isinstance(x, Zone)])
ach = round(0.1 + 0.07 * 6.0 * externalSurfaceArea / (0.8 * netVolume), 5)

for zoneList in list(x for x in epObjects if isinstance(x, (ZoneList))):
    epObjects += [zoneList.GetPeopleObject(24)]
    epObjects += [zoneList.GetLightsObject(6)]
    epObjects += [zoneList.GetElectricEquipmentObject(12.5)]
    epObjects += [zoneList.GetInfiltrationObject(ach)]
    epObjects += [zoneList.GetDefaultVentilationObject()]
    epObjects += [zoneList.GetNaturalVentilationObject()]

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    hvac = WaterToAirHeatPump(WaterToAirHeatPump.Default)
    hvac.ZoneName = zone.Name
    hvac.TemplateThermostatName = "Office"
    epObjects += [hvac]

from Probabilistic.Parameter import ProbabilisticParameters
nSamples = 120

Logger.StartTask('Generating Samples')

pps = ProbabilisticParameters.ReadCsv('Probabilistic/1.csv')
samples = pps.GenerateSamplesAsDF(nSamples,)

Logger.StartTask('Generating IDF files')

if simulate:
    os.system(f'rm Test/IDFFiles/*.csv')
    for i, sample in samples.iterrows():
        objs = list(epObjects)

        CreateConstructions(sample, objs)
        SetBestMatchConstruction(objs)

        with open(f'Test/IDFFiles/{i}.idf', 'w') as f:
            f.write('\n'.join((x.IDF for x in objs)))

    Logger.StartTask('Simulations')
    os.system(f'python3 runEP.py {os.getcwd()}/Test')

Logger.StartTask('Reading files')

pEnergies = []
for i in range(nSamples):
    data = pd.read_csv(f'Test/IDFFiles/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)

Logger.StartTask('Training regressor')
from Helper.MLHelper import GetGenerator, GetRegressor, GetScalingLayer

col = ["NN", "RC", "LR",]
N1 = [20, 50, 100, 200]
N2 = [0, 5, 10, 20]
RC = [1e-3, 1e-4, 1e-5,]
LR = [1e-2, 3e-3, 1e-3,]

nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
hyperparameters = pd.DataFrame([[n, r, l,] 
                                    for n in nn
                                    for r in RC
                                    for l in LR
                                ], columns = col).sample(n=60,)
hyperparameters.index = range(len(hyperparameters))

r = GetRegressor(hyperparameters[:4], samples.columns, d.Values['Total'].columns, f'Test/MLModel/Regressor', samples, d.Values['Total'], scalingDF_X=pps.GetScalingDF() , training=simulate or trainRegressor)

Logger.FinishTask('Training regressor')

Logger.StartTask('Training generator')
target2017 = np.array([5.795,6.123,4.208,1.49,0.75,3.535,1.189,2.568,1.006,5.01,5.322,6.972])
target2018 = np.array([5.423,5.728,4.453,2.751,1.142,2.441,0.8,2.405,1.623,4.226,6.361,4.722])

target2017 = np.array((target2017, target2018)).mean(axis=0)
# targetValues = np.array([np.array(target2017).sum() for _ in range(100)])
targetValues = np.concatenate(([target2017 for _ in range(50)], [target2017 for _ in range(50)]))

revScalingDF_X = pps.GetScalingDF()
m = GetGenerator(hyperparameters, 20, samples.columns, f'Test/MLModel/Generator', f'{r.FilePath}.h5', targetValues, revScalingDF=revScalingDF_X, training=simulate or trainRegressor or trainGenerator)

Logger.FinishTask('Training generator')
Logger.StartTask('Determining parameters')

dfs = m.Predict(10,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

Logger.PrintSummary()