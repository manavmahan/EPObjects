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

RunPeriod.Default = {
    "BeginMonth": 1, 
    "BeginDayofMonth": 1, 
    "BeginYear": 2017, 
    "EndMonth": 12, 
    "EndDayofMonth": 31, 
    "EndYear": 2017, 
    "DayofWeekforStartDay": " ", 
    "UseWeatherFileHolidaysandSpecialDays": "No", 
    "UseWeatherFileDaylightSavingPeriod": "Yes",
    "ApplyWeekendHolidayRule": "No", 
    "UseWeatherFileRainIndicators": "Yes", 
    "UseWeatherFileSnowIndicators": "Yes", 
    "TreatWeatherasActual": "No",
}