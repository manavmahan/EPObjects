from IDFObject import IDFObject
    
class People(IDFObject.IDFObject):
    __IDFName__ = 'People'
    Properties = [
        'Name',
        'ZoneListName',
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
        'SurfaceNameAngleFactorListName',
        'WorkEfficiencyScheduleName',
        'ClothingInsulationCalculationMethod',
        'ClothingInsulationCalculationMethodScheduleName',
        'ClothingInsulationScheduleName',
        'AirVelocityScheduleName',
        'ThermalComfortModel1Type',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

People.Default = dict(
    NumberofPeopleScheduleName = 'Office.People',
    NumberofPeopleCalculationMethod = 'Area/Person',
    NumberofPeople = '',
    PeopleperZoneFloorArea = '',
    ZoneFloorAreaperPerson = 22,
    FractionRadiant = 0.1,
    SensibleHeatFraction = '',
    ActivityLevelScheduleName = 'Office.Activity',
    CarbonDioxideGenerationRate = 3.82E-08,
    EnableASHRAE55ComfortWarnings = '',
    MeanRadiantTemperatureCalculationType = 'ZoneAveraged',
    SurfaceNameAngleFactorListName = '',
    WorkEfficiencyScheduleName = 'Always1',
    ClothingInsulationCalculationMethod = 'DynamicClothingModelASHRAE55',
    ClothingInsulationCalculationMethodScheduleName = '',
    ClothingInsulationScheduleName = '',
    AirVelocityScheduleName = 'Always1',
    ThermalComfortModel1Type = 'Fanger',
)