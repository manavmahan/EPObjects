import json
from IDFObject.IDFObject import IDFObject
    
class Version(IDFObject):
    __IDFName__ = 'Version'
    Properties = [
        'VersionIdentifier',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)