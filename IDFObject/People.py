from IDFObject import IDFObject
    
class People(IDFObject.IDFObject):
    __IDFName__ = 'People'
    Properties = [
        'Name',
        'ZoneorZoneListName',
        'NumberofPeopleScheduleName',
        'NumberofPeopleCalculationMethod',
        'NumberofPeople',
        'PeopleperZoneFloorArea',
        'ZoneFloorAreaperPerson',
        'FractionRadiant',
        'SensibleHeatFraction',
        'ActivityLevelScheduleName',
        'CarbonDioxideGenerationRate',
        'EnableASHRAE55ComfortWarnings',
        'MeanRadiantTemperatureCalculationType',
        'SurfaceName/AngleFactorListName',
        'WorkEfficiencyScheduleName',
        'ClothingInsulationCalculationMethod',
        'ClothingInsulationCalculationMethodScheduleName',
        'ClothingInsulationScheduleName',
        'AirVelocityScheduleName',
        'ThermalComfortModel1Type',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
