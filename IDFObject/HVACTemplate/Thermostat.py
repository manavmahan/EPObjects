from IDFObject import IDFObject
    
class Thermostat(IDFObject.IDFObject):
    __IDFName__ = 'HVACTemplate:Thermostat'
    Properties = [
        'Name',
        'HeatingSetpointScheduleName',
        'ConstantHeatingSetpoint',
        'CoolingSetpointScheduleName',
        'ConstantCoolingSetpoint',
    ]

    default = dict(
        HeatingSetpointScheduleName = '',
        CoolingSetpointScheduleName = '',
        ConstantHeatingSetpoint = '',
        ConstantCoolingSetpoint = '',
    )   

    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)