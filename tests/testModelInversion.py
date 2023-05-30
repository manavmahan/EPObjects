import json
import os
import numpy as np
import pandas as pd

from pathlib import Path
Home = str(Path.home())

from logger import Logger
from helper.Modules import *

from helper.construction_helper import create_construction_materials, set_best_match_construction, InitialiseZoneSurfaces, set_internal_mass, SetBestMatchInternalMass
from helper.infiltration_helper import SetBestMatchPermeability

from helper.schedule_helper import GetOfficeSchedules, set_setpoints
from helper.run_period_helper import GetRunPeriodsFromFile
from helper.hvac_helper.heatpump_with_boiler import add_heatpumps
from helper.hvac_helper.system_efficiency_helper import SetBestMatchSystemParameter
from helper.shading_helper import AddShading

from helper.internal_heat_gains_helper import SetBestMatchInternalHeatGains

from probabilistic.energy_predictions import EnergyPrediction, ProbabilisticEnergyPrediction
from probabilistic.parameter import ProbabilisticParameters

ProjectDirectory = f'{Home}/repos/EPObjects/Tausendpfund/'
NumSamples = 100

simulate = False
suffix = f'inversion-1'

runPeriods, consumption = GetRunPeriodsFromFile(f'{ProjectDirectory}/Consumption.csv')
pps = ProbabilisticParameters.ReadCsv(f'{ProjectDirectory}/Parameters.csv')
samples = pps.GenerateSamplesAsDF(NumSamples,)

if simulate:
    with open(f'{ProjectDirectory}/Geometry.json') as f:
        epObjects = json.load(f, cls=IDFJsonDecoder)



    epObjects += runPeriods
    epObjects += GetOfficeSchedules(f'{ProjectDirectory}/Schedules.json', f'{ProjectDirectory}/ScheduleTypes.json')
    InitialiseZoneSurfaces(epObjects)
    set_internal_mass(epObjects, 25)

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
        epObjects += [zone.get_infiltration_object(0.3)]

    zoneLists = list(x for x in epObjects if isinstance(x, Zonelist)) 
    for zoneList in zoneLists:
        epObjects += [zoneList.get_people(zonelistVariables[zoneList.Name]['People'])]
        epObjects += [zoneList.get_thermostat()]
        epObjects += [zoneList.get_lights(zonelistVariables[zoneList.Name]['Lights'])]
        epObjects += [zoneList.get_electric_equipment(zonelistVariables[zoneList.Name]['Equipment'])]
        epObjects += [zoneList.get_default_ventilation(zoneList.Name != 'Office')]

    add_heatpumps(epObjects)
    AddShading(epObjects)

    Logger.StartTask('Generating Samples')
    Logger.StartTask('Generating IDF files')

    idfFolder = f'{ProjectDirectory}/IDFFiles-{suffix}'
    if not os.path.isdir(idfFolder): os.mkdir(idfFolder)
    os.system(f'rm {idfFolder}/*.csv')
    os.system(f'rm {idfFolder}/*.idf')
    os.system(f'rm {idfFolder}/*.dxf')
    os.system(f'rm {idfFolder}/*.err')
    for i, sample in samples.iterrows():
        objs = list(epObjects)

        create_construction_materials(sample, objs)

        set_best_match_construction(objs)

        SetBestMatchInternalMass(sample, objs)
        SetBestMatchPermeability(sample, objs)
        set_setpoints(sample, objs)
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
    data = pd.read_csv(f'{ProjectDirectory}/IDFFiles-{suffix}/{i}.csv', index_col=0)
    data = data[[c for c in data.columns if 'Energy' in c]]
    data.index = range(len(data))
    pEnergies += [EnergyPrediction(None, data)]

d = ProbabilisticEnergyPrediction(None, pEnergies)

Logger.StartTask('Training regressor')

from EPObjects.MLModels.MLHelper import GetRegressor, get_scaling_layer

MLFolder = f'{ProjectDirectory}/MLModel-{suffix}'
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

r = GetRegressor(hyperparameters[:4], list(d.Values['Total'].columns), samples.columns, f'{MLFolder}/Regressor', d.Values['Total'], samples, training=False)

Logger.FinishTask('Training regressor')

Logger.StartTask('Determining parameters')

measured = consumption.T
measured.columns = list(d.Values['Total'].columns)
# print (measured.columns)
# print (d.Values['Total'])
dfs = r.Predict(measured,)

# print (dfs.shape)
for p in dfs.columns:
    print (p, np.min(dfs[p]), np.percentile(dfs[p], 2.5), np.percentile(dfs[p], 50), dfs[p].mean(), np.percentile(dfs[p], 97.5), np.max(dfs[p]))

dfs.T.to_csv(f'{MLFolder}/predictions.csv')
Logger.PrintSummary()