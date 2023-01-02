from ListObject import ListObject
from IDFObject.IDFObject import IDFObject

class ReferencePoint:
    Properties = [
        'Name',
        'PartControlled',
        'IlluminanceSetpoint'
    ]

    def __init__(self, propertiesDict: dict()):
        for property in self.Properties:
            if property in propertiesDict: setattr(self, property, propertiesDict[property])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return ','.join(str(getattr(self, x)).rstrip() for x in self.Properties)

class Controls(IDFObject):
    __IDFName__ = 'Daylighting:Controls'
    Properties = [
        'Name',
        'ZoneName',
        'DaylightingMethod',
        'AvailabilityScheduleName',
        'LightingControlType',
        'MinimumInputPowerFractionforContinuousorContinuousOffDimmingControl',
        'MinimumLightOutputFractionforContinuousorContinuousOffDimmingControl',
        'NumberofSteppedControlSteps',
        'ProbabilityLightingwillbeResetWhenNeededinManualSteppedControl',
        'GlareCalculationDaylightingReferencePointName',
        'GlareCalculationAzimuthAngleofViewDirection',
        'MaximumAllowableDiscomfortGlareIndex',
        'DElightGriddingResolution',
        'DaylightingReferencePoints',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self,):
        if  not hasattr(self, 'DaylightingReferencePoints'):
            return
        
        dlpArray = self.DaylightingReferencePoints.split(',')
        n = int (len(dlpArray) // 3)
        dlPoints = []
        for i, point in enumerate(dlpArray[0::3]):
            dlPoints += [
                ReferencePoint(
                    dict(
                        Name = point,
                        PartControlled = dlpArray[i*3 + 1],
                        IlluminanceSetpoint = dlpArray[i*3 + 2],
                    )
                )
            ]
        self.DaylightingReferencePoints = ListObject(dlPoints)

    def AddDLPoints(self, points, illuminance):
        dlPoints = []
        n = len(points)
        for i, point in enumerate(points):
            dlPoints += [
                ReferencePoint(
                    dict(
                        Name = point,
                        PartControlled = round(1/n, 5) if i < n-1 else round(1 - round((n-1) / n, 5), 5),
                        IlluminanceSetpoint = illuminance,
                    )
                )
            ]
        self.DaylightingReferencePoints = ListObject(dlPoints)

Controls.Default = dict(
    DaylightingMethod = "SplitFlux",
    LightingControlType = "Continuous",
    MinimumInputPowerFractionforContinuousorContinuousOffDimmingControl = 0.3,
    MinimumLightOutputFractionforContinuousorContinuousOffDimmingControl = 0.3,
    NumberofSteppedControlSteps = 1,
    ProbabilityLightingwillbeResetWhenNeededinManualSteppedControl = 1,
    GlareCalculationAzimuthAngleofViewDirection = 180,
    MaximumAllowableDiscomfortGlareIndex = 22,
    DElightGriddingResolution = 2,
)