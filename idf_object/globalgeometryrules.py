from idf_object import IDFObject
    
class GlobalGeometryRules(IDFObject):
    __IDFName__ = 'GlobalGeometryRules'
    Properties = [
        'StartingVertexPosition',
        'VertexEntryDirection',
        'CoordinateSystem',
        'DaylightingReferencePointCoordinateSystem',
        'RectangularSurfaceCoordinateSystem',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
