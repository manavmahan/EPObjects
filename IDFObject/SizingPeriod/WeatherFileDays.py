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

    default = dict()
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        props = dict(getattr(self, default if default else 'default'))
        props.update(kwargs)
        super().__init__(self.Properties, props)
