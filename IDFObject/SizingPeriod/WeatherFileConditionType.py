from IDFObject.IDFObject import IDFObject

'''
SizingPeriod:WeatherFileConditionType,
  Extreme Winter Weather Period for Design,  !- Name
  WinterExtreme,                             !- Period Selection
  WinterDesignDay,                           !- Day Type
  No,                          !- Use Weather File Daylight Saving Period
  No;                          !- Use Weather File Rain and Snow Indicators
'''
    
class WeatherFileConditionType(IDFObject):
    __IDFName__ = 'SizingPeriod:WeatherFileConditionType'
    Properties = [
        'Name',
        'PeriodSelection',
        'DayType',
        'UseWeatherFileDaylightSavingPeriod',
        'UseWeatherFileRainandSnowIndicators',
    ]

    default = dict(
        UseWeatherFileDaylightSavingPeriod = 'No',
        UseWeatherFileRainandSnowIndicators = 'No',
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
