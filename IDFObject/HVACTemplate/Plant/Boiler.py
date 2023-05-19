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
    
    Efficiency = None

    def __init__(self, properties: dict()) -> None:
        super().__init__(self.Properties, properties)
        self.Initialise()

    def Initialise(self):
        pass

    @classmethod
    def get_default(cls, **kwargs):
        props = dict(Boiler.Default)
        props.update(kwargs)
        return Boiler(props)

Boiler.Default = {
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