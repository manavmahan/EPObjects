from IDFObject import IDFObject
    
class InternalMass(IDFObject.IDFObject):
    __IDFName__ = 'InternalMass'
    Properties = [
        'Name',
        'ConstructionName',
        'ZoneName',
        'SpaceName',
        'SurfaceArea',
    ]

    default = dict(
        ConstructionName = "Mass",
        SpaceName = '',
    )
    
    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)