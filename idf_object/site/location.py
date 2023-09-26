from idf_object import IDFObject
    
class Location(IDFObject):
    __IDFName__ = 'Site:Location'
    Properties = [
        'Name',
        'Latitude',
        'Longitude',
        'TimeZone',
        'Elevation',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
