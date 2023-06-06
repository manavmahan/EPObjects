from idf_object import IDFObject

class AirGap(IDFObject):
    __IDFName__ = 'Material:AirGap'
    Properties = [
        "Name",
        "Resistance",
    ]

    default = dict(
        Name = 'AirGap',
        Resistance = 0.12, # corresponding to 30 mm air cavity
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
