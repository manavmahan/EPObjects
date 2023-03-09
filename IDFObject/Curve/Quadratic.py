from IDFObject.IDFObject import IDFObject
    
class Quadratic(IDFObject):
    __IDFName__ = 'Curve:Quadratic'
    Properties = [
        'Name',
        'Coefficient1Constant',
        'Coefficient2x',
        'Coefficient3x2',
        'MinimumValueofx',
        'MaximumValueofx',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

Quadratic.HPHeatPLFFPLR = dict(
    Name = 'HPHeatPLFFPLR',
    Coefficient1Constant = 0.9,
    Coefficient2x = 0.1,
    Coefficient3x2 = 0.0,
    MinimumValueofx = 0.0,
    MaximumValueofx = 1.0,
)
