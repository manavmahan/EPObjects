from IDFObject import IDFObject

class Boiler(IDFObject.IDFObject):
    __IDFName__ = "HVACTemplate:Plant:Boiler"
    Properties = [
        'Name',
        'BoilerType',
        'Capacity',
        'Efficiency',
        'FuelType',
        'Priority',
        'SizingFactor',
        'MinimumPartLoadRatio',
        'MaximumPartLoadRatio',
        'OptimumPartLoadRatio',
        'WaterOutletUpperTemperatureLimit',
    ]
    
    default = {
        "Name": "Boiler",
        "BoilerType": "HotWaterBoiler", 
        "Capacity": "autosize", 
        "Efficiency": 0.95, 
        "FuelType": "Electricity", 
        "Priority": 1, 
        "SizingFactor": 1.2, 
        "MinimumPartLoadRatio": 0.1, 
        "MaximumPartLoadRatio": 1.1, 
        "OptimumPartLoadRatio": 0.9, 
        "WaterOutletUpperTemperatureLimit": 99
    }

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)