from IDFObject import IDFObject
    
class Tower(IDFObject.IDFObject):
    __IDFName__ = 'HVACTemplate:Plant:Tower'
    Properties = [
        'Name',
        'TowerType',
        'HighSpeedNominalCapacity',
        'HighSpeedFanPower',
        'LowSpeedNominalCapacity',
        'LowSpeedFanPower',
        'FreeConvectionCapacity',
        'Priority',
        'SizingFactor',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
