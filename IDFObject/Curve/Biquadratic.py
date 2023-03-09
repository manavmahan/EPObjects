from IDFObject.IDFObject import IDFObject
    
class Biquadratic(IDFObject):
    __IDFName__ = 'Curve:Biquadratic'
    Properties = [
        'Name',
        'Coefficient1Constant',
        'Coefficient2x',
        'Coefficient3x2',
        'Coefficient4y',
        'Coefficient5y2',
        'Coefficient6xy',
        'MinimumValueofx',
        'MaximumValueofx',
        'MinimumValueofy',
        'MaximumValueofy',
        'MinimumCurveOutput',
        'MaximumCurveOutput',
        'InputUnitTypeforX',
        'InputUnitTypeforY',
        'OutputUnitType',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

Biquadratic.HPHeatingCAPFTemp = dict(
    Name = 'HPHeatingCAPFTemp',
    Coefficient1Constant = '0.876825',
    Coefficient2x = '-0.002955',
    Coefficient3x2 = '-5.8e-05',
    Coefficient4y = '0.025335',
    Coefficient5y2 = '0.000196',
    Coefficient6xy = '-4.3e-05',
    MinimumValueofx = '0',
    MaximumValueofx = '50',
    MinimumValueofy = '0',
    MaximumValueofy = '50',
    MinimumCurveOutput = '0',
    MaximumCurveOutput = '5',
    InputUnitTypeforX = 'Temperature',
    InputUnitTypeforY = 'Temperature',
    OutputUnitType = 'Dimensionless'
)

Biquadratic.HPHeatingEIRFTemp = dict(
    Name = 'HPHeatingEIRFTemp',
    Coefficient1Constant =  0.704658,
    Coefficient2x = 0.008767,
    Coefficient3x2 = 0.000625,
    Coefficient4y = -0.009037,
    Coefficient5y2 = 0.000738,
    Coefficient6xy = -0.001025,
    MinimumValueofx = 0,
    MaximumValueofx = 50,
    MinimumValueofy = 0,
    MaximumValueofy = 50,
    MinimumCurveOutput = 0,
    MaximumCurveOutput = 5,
    InputUnitTypeforX = 'Temperature',
    InputUnitTypeforY = 'Temperature',
    OutputUnitType = 'Dimensionless',
)