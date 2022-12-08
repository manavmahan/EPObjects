from IDFObject.IDFObject import IDFObject
    
class GlobalGeometryRules(IDFObject):
    __IDFName__ = 'GlobalGeometryRules'
    Properties = [
        'StartingVertexPosition',
        'VertexEntryDirection',
        'CoordinateSystem',
        'DaylightingReferencePointCoordinateSystem',
        'RectangularSurfaceCoordinateSystem',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
