from IDFObject import IDFObject
    
class RunPeriod(IDFObject.IDFObject):
    __IDFName__ = 'RunPeriod'
    Properties = [
        'Name',
        'BeginMonth',
        'BeginDayofMonth',
        'BeginYear',
        'EndMonth',
        'EndDayofMonth',
        'EndYear',
        'DayofWeekforStartDay',
        'UseWeatherFileHolidaysandSpecialDays',
        'UseWeatherFileDaylightSavingPeriod',
        'ApplyWeekendHolidayRule',
        'UseWeatherFileRainIndicators',
        'UseWeatherFileSnowIndicators',
        'TreatWeatherasActual',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
