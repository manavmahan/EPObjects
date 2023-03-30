import json
import os
import numpy as np
import pandas as pd

from pathlib import Path
Home = str(Path.home())

from EPLogger import Logger

from Helper.Modules import *

from Helper.ConstructionHelper import CreateConstructions, SetBestMatchConstruction, InitialiseZoneSurfaces, SetInternalMass, SetReportingFrequency, SetBestMatchInternalMass
from Helper.InfiltrationHelper import SetBestMatchPermeability

from Helper.ScheduleHelper import GetOfficeSchedules, SetBestMatchSetpoints
from Helper.RunPeriodHelper import GetRunPeriodsFromFile
from Helper.HVACHelper.HeatPumpWithBoiler import AddHeatPumps, AddHeatPumpsWithBoiler
from Helper.HVACHelper.SystemEfficiencyHelper import SetBestMatchSystemParameter
from Helper.ShadingHelper import AddShading

from Helper.InternalHeatGainsHelper import SetBestMatchInternalHeatGains

from Probabilistic.EnergyPredictions import EnergyPrediction, ProbabilisticEnergyPrediction
from Probabilistic.Parameter import ProbabilisticParameters

ProjectDirectory = f'{Home}/repos/EPObjects/Tausendpfund/'
NumSamples = 10

simulate, trainRegressor, trainGenerator = True, False, True
number = 1

with open(f'{ProjectDirectory}/Geometry.json') as f:
    epObjects = json.load(f, cls=IDFJsonDecoder)

runPeriods, consumption = GetRunPeriodsFromFile(f'{ProjectDirectory}/Consumption.csv')

epObjects += runPeriods
epObjects += GetOfficeSchedules(f'{ProjectDirectory}/Schedules.json', f'{ProjectDirectory}/ScheduleTypes.json')
InitialiseZoneSurfaces(epObjects)
SetInternalMass(epObjects, 25)

zonelistVariables = dict(
    Office = dict(People = 24.0, Lights = 6.0, Equipment = 15,),
    Toilet = dict(People = 48.0, Lights = 4.5, Equipment = 5,),
    Stairs = dict(People = 48.0, Lights = 4.5, Equipment = 5,),
    Corridor = dict(People = 48.0, Lights = 4.5, Equipment = 10,),
    Service = dict(People = 100.0, Lights = 1.0, Equipment = 25,),
    Technic = dict(People = 100.0, Lights = 1.0, Equipment = 10,),
)

zones = list(x for x in epObjects if isinstance(x, Zone))
for zone in zones:
    epObjects += [zone.GetInfiltrationObject(0.3)]

zoneLists = list(x for x in epObjects if isinstance(x, ZoneList)) 
for zoneList in zoneLists:
    epObjects += [zoneList.GetPeopleObject(zonelistVariables[zoneList.Name]['People'])]
    epObjects += [zoneList.GetThermostatObject()]
    epObjects += [zoneList.GetLightsObject(zonelistVariables[zoneList.Name]['Lights'])]
    epObjects += [zoneList.GetElectricEquipmentObject(zonelistVariables[zoneList.Name]['Equipment'])]
    epObjects += [zoneList.GetDefaultVentilationObject(zoneList.Name != 'Office')]

AddHeatPumps(epObjects)
AddShading(epObjects)

Logger.StartTask('Generating Samples')

pps = ProbabilisticParameters.ReadCsv(f'{ProjectDirectory}/Parameters.csv')
samples = pps.GenerateSamplesAsDF(NumSamples,)

Logger.StartTask('Generating IDF files')

if simulate:
    idfFolder = f'{ProjectDirectory}/IDFFiles-{number}'
    if not os.path.isdir(idfFolder): os.mkdir(idfFolder)
    os.system(f'rm {idfFolder}/*.csv')
    os.system(f'rm {idfFolder}/*.idf')
    os.system(f'rm {idfFolder}/*.dxf')
    os.system(f'rm {idfFolder}/*.err')
    for i, sample in samples.iterrows():
        objs = list(epObjects)

        CreateConstructions(sample, objs)

        SetBestMatchConstruction(objs)

        SetBestMatchInternalMass(sample, objs)
        SetBestMatchPermeability(sample, objs)
        SetBestMatchSetpoints(sample, objs)
        SetBestMatchInternalHeatGains(sample, objs)
        SetBestMatchSystemParameter(sample, objs)

        with open(f'{idfFolder}/{i}.idf', 'w') as f:
            f.write('\n'.join((x.IDF for x in objs)))

    Logger.StartTask('Simulations')
    os.system(f'python3 runEP.py {ProjectDirectory}')
    Logger.FinishTask('Simulations')

Logger.StartTask('Reading files')

pEnergies = []
for i in range(NumSamples):
    data = pd.read_csv(f'{idfFolder}/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    data.index = range(len(data))
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)

Logger.StartTask('Training regressor')
from Helper.MLHelper import GetGenerator, GetRegressor, GetScalingLayer

MLFolder = f'{ProjectDirectory}/MLModel-{number}'
if not os.path.isdir(MLFolder): os.mkdir(MLFolder)

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

r = GetRegressor(hyperparameters[:4], samples.columns, d.Values['Total'].columns, f'{MLFolder}/Regressor', samples, d.Values['Total'], scalingDF_X=pps.GetScalingDF() , training=simulate or trainRegressor)

Logger.FinishTask('Training regressor')

Logger.StartTask('Training generator')
col = ["NN", "RC", "LR",]
N1 = [100, 200, 400,]
N2 = [5, 10, 20]
RC = [1e-3, 1e-4, 1e-5,]
LR = [1e-2, 3e-3, 1e-3,]

nn = [[nn1, nn2] for nn1 in N1 for nn2 in N2]
hyperparameters = pd.DataFrame([[n, r, l,] 
                                    for n in nn
                                    for r in RC
                                    for l in LR
                                ], columns = col).sample(frac=1,)
hyperparameters.index = range(len(hyperparameters))

consumption = consumption.values.T
targetValues = consumption[[np.random.randint(0, len(consumption)) for _ in range(50)]]

revScalingDF_X = pps.GetScalingDFFromFile(f'{ProjectDirectory}/Parameters.csv')
m = GetGenerator(hyperparameters, 1000, samples.columns, f'{MLFolder}/Generator', f'{r.FilePath}.h5', targetValues, revScalingDF=revScalingDF_X, training=simulate or trainRegressor or trainGenerator)

Logger.FinishTask('Training generator')
Logger.StartTask('Determining parameters')

dfs = m.Predict(10,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

Logger.PrintSummary()