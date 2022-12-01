from IDFObject import IDFObject
    
class Controls(IDFObject.IDFObject):
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

    def Initialise(self):
        self.DaylightingReferencePoints = self.DaylightingReferencePoints.replace(';', ',')