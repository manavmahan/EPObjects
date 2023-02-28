from IDFObject.IDFObject import IDFObject
    
class File(IDFObject):
    __IDFName__ = 'Schedule:File'
    Properties = [
        'Name',
        'ScheduleTypeLimit',
        'NameofFile',
        'ColumnNumber',
        'RowstoSkipatTop',
        'NumberofHoursofData',
        'ColumnSeparator',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

File.Default = dict(
    ScheduleTypeLimit = '',
    RowstoSkipatTop = 1,
    NumberofHoursofData = 8760,
    ColumnSeparator = ',',
)