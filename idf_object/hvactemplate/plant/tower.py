from idf_object import IDFObject
    
class Tower(IDFObject):
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

    default = {
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

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)