from idf_object import IDFObject
    
class People(IDFObject):
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

    default = dict(
        NumberofPeopleCalculationMethod = 'Area/Person',
        NumberofPeople = '',
        PeopleperZoneFloorArea = '',
        ZoneFloorAreaperPerson = 20,
        FractionRadiant = 0.1,
        SensibleHeatFraction = '',
        CarbonDioxideGenerationRate = 3.82E-08,
        EnableASHRAE55ComfortWarnings = '',
        MeanRadiantTemperatureCalculationType = 'ZoneAveraged',
        SurfaceNameAngleFactorListName = '',
        WorkEfficiencyScheduleName = 'Generic.Always01',
        ClothingInsulationCalculationMethod = 'DynamicClothingModelASHRAE55',
        ClothingInsulationCalculationMethodScheduleName = '',
        ClothingInsulationScheduleName = '',
        AirVelocityScheduleName = 'Generic.Always01',
        ThermalComfortModel1Type = 'Fanger',
    )

    zone = dict(
        NumberofPeopleCalculationMethod = 'People',
        NumberofPeople = '',
        PeopleperZoneFloorArea = '',
        ZoneFloorAreaperPerson = '',
        FractionRadiant = 0.1,
        SensibleHeatFraction = '',
        CarbonDioxideGenerationRate = 3.82E-08,
        EnableASHRAE55ComfortWarnings = '',
        MeanRadiantTemperatureCalculationType = 'ZoneAveraged',
        SurfaceNameAngleFactorListName = '',
        WorkEfficiencyScheduleName = 'Generic.Always01',
        ClothingInsulationCalculationMethod = 'DynamicClothingModelASHRAE55',
        ClothingInsulationCalculationMethodScheduleName = '',
        ClothingInsulationScheduleName = '',
        AirVelocityScheduleName = 'Generic.Always01',
        ThermalComfortModel1Type = 'Fanger',
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)