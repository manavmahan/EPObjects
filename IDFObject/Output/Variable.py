from IDFObject import IDFObject
    
class Variable(IDFObject.IDFObject):
    __IDFName__ = 'Output:Variable'
    Properties = [
        'KeyValue',
        'Name',
        'ReportingFrequency',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
    
    @classmethod
    def get_variable(cls, **kwargs):
        props = dict(Variable.Default)
        props.update(kwargs)
        return Variable(props)

Variable.Default = dict(
    KeyValue = '*',
    ReportingFrequency = "RunPeriod"
)
