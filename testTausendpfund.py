import json
import os
import numpy as np

from EPLogger import Logger

from Helper.Modules import *
from Helper.ConstructionHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass, SetReportingFrequency

from Helper.ScheduleHelper import CreateOfficeSchedule, DefaultOfficeSchedules
from Helper.RunPeriodHelper import SetRunPeriod
from EnumTypes import Frequency

import pandas as pd
from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction

RepoPath = '/home/ubuntu/repos/EPObjects/'

simulate, trainRegressor, trainGenerator = True, True, True

with open(f'{os.getcwd()}/Tausendpfund.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

epObjects += SetRunPeriod()

# SetReportingFrequency(epObjects, Frequency.Annual)

InitialiseZoneSurfaces(epObjects)
SetInternalMass(epObjects, 25)
epObjects += list(CreateOfficeSchedule(2017, DefaultOfficeSchedules, f'{RepoPath}/Test/IDFFiles/Schedule.txt'))

externalSurfaceArea = sum([x.ExternalSurfaceArea for x in epObjects if isinstance(x, Zone)])
netVolume = sum([x.NetVolume for x in epObjects if isinstance(x, Zone)])
ach = round(0.1 + 0.07 * 6.6 * externalSurfaceArea / netVolume, 5)

zonelistVariables = dict(
    Office = dict(Lights = 6.0, Equipment = 15,),
    Toilet = dict(Lights = 4.5, Equipment = 5,),
    Stairs = dict(Lights = 4.5, Equipment = 5,),
    Corridor = dict(Lights = 4.5, Equipment = 10,),
    Service = dict(Lights = 1.0, Equipment = 25,),
    Technic = dict(Lights = 1.0, Equipment = 10,),
)

zoneLists = list(x for x in epObjects if isinstance(x, ZoneList)) 
for zoneList in zoneLists:
    epObjects += [zoneList.GetThermostatObject()]
    epObjects += [zoneList.GetLightsObject(zonelistVariables[zoneList.Name]['Lights'])]
    epObjects += [zoneList.GetElectricEquipmentObject(zonelistVariables[zoneList.Name]['Equipment'])]
    epObjects += [zoneList.GetInfiltrationObject(ach)]
    epObjects += [zoneList.GetDefaultVentilationObject(zoneList.Name != 'Office')]
    # epObjects += [zoneList.GetNaturalVentilationObject()]

for zone in [x for x in epObjects if isinstance(x, Zone)]:
    zoneListName = next(x for x in zoneLists if zone.Name in x.IDF).Name
    if "Office" in zone.Name: epObjects += [zone.GetPeopleObject(4, zoneListName)]
    epObjects += [zone.GetWaterToAirHeatPumpObject(zoneListName)]

from Probabilistic.Parameter import ProbabilisticParameters
nSamples = 200

Logger.StartTask('Generating Samples')

pps = ProbabilisticParameters.ReadCsv('Probabilistic/1.csv')
samples = pps.GenerateSamplesAsDF(nSamples,)

Logger.StartTask('Generating IDF files')

if simulate:
    os.system(f'rm Test/IDFFiles/*.csv')
    os.system(f'rm Test/IDFFiles/*.idf')
    os.system(f'rm Test/IDFFiles/*.dxf')
    os.system(f'rm Test/IDFFiles/*.err')
    for i, sample in samples.iterrows():
        objs = list(epObjects)

        CreateConstructions(sample, objs)
        SetBestMatchConstruction(objs)

        with open(f'Test/IDFFiles/{i}.idf', 'w') as f:
            f.write('\n'.join((x.IDF for x in objs)))

    Logger.StartTask('Simulations')
    os.system(f'python3 runEP.py {os.getcwd()}/Test')
    Logger.FinishTask('Simulations')

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
target2017 = np.array([5.423,5.728,4.453,2.751,1.142,2.441,0.800,2.405,1.623,4.226,6.361,4.722])
target2018 = np.array([6.167,6.519,3.963,0.228,0.359,4.630,1.577,2.731,0.391,5.793,4.283,9.222])

# target2017 = np.array((target2017, target2018)).mean(axis=0)
# targetValues = np.array([np.array(target2017).sum() for _ in range(100)])
targetValues = np.concatenate(([target2017 for _ in range(50)], [target2017 for _ in range(50)]))

np.random.shuffle(targetValues)

revScalingDF_X = pps.GetScalingDF()
m = GetGenerator(hyperparameters, 20, samples.columns, f'Test/MLModel/Generator', f'{r.FilePath}.h5', targetValues, revScalingDF=revScalingDF_X, training=simulate or trainRegressor or trainGenerator)

Logger.FinishTask('Training generator')
Logger.StartTask('Determining parameters')

dfs = m.Predict(10,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

Logger.PrintSummary()