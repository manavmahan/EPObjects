from idf_object import IDFObject
    
class RunPeriod(IDFObject):
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

    default = {
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
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)