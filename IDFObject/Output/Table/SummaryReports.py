from IDFObject import IDFObject
    
class SummaryReports(IDFObject.IDFObject):
    __IDFName__ = 'Output:Table:SummaryReports'
    Properties = [
        'ReportsName',
    ]

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.Initialise()

    def Initialise(self):
        self.ReportsName = self.ReportsName.replace(';', ',')