from IDFObject import IDFObject
    
class SummaryReports(IDFObject.IDFObject):
    __IDFName__ = 'Output:Table:SummaryReports'
    Properties = [
        'ReportsName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
        self.Initialise()

    def Initialise(self):
        self.ReportsName = self.ReportsName.replace(';', ',')