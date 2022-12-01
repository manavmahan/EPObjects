from IDFObject import IDFObject
    
class WeatherFileDays(IDFObject.IDFObject):
    __IDFName__ = 'SizingPeriod:WeatherFileDays'
    Properties = [
        'Name',
        'BeginMonth',
        'BeginDayofMonth',
        'EndMonth',
        'EndDayofMonth',
        'DayofWeekforStartDay',
        'UseWeatherFileDaylightSavingPeriod',
        'UseWeatherFileRainandSnowIndicators',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)
