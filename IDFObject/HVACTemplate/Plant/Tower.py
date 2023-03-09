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

Tower.Default = {
    "Name": "MainTower",
    "TowerType": "SingleSpeed", 
    "HighSpeedNominalCapacity": "autosize", 
    "HighSpeedFanPower": "autosize", 
    "LowSpeedNominalCapacity": "autosize", 
    "LowSpeedFanPower": "autosize", 
    "FreeConvectionCapacity": "autosize", 
    "Priority": 1, 
    "SizingFactor": 1.2
}