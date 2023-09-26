from idf_object import IDFObject

class Compact(IDFObject):
    __IDFName__ = 'Schedule:Compact'
    Properties = [
        'Name',
        'ScheduleTypeLimitsName',
        'Fields',
    ]

    default = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31, For: Alldays, Until: 24:00, v1'''
    )

    four_and_half_days = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31,
        For: Mondays Tuesdays Wednesday Thursdays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,
            Until: t1, v1, Until: t2, v2, Until: 24:00, v1,
        For: Fridays,
            Until: t1, v1, Until: t3, v2, Until: 24:00, v1,
        For: Weekends Holidays,
            Until: 24:00, v1'''
    )

    typical_house = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31,
        For: Mondays Tuesdays Wednesday Thursdays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,
            Until: t1, v1, Until: t2, v2, Until: t3, v3, Until: 24:00, v1,
        For: Fridays,
            Until: t1, v1, Until: t2, v2, Until: t4, v4, Until: 24:00, v1,
        For: Weekends Holidays,
            Until: t1, v1, Until: t5, v5, Until: t3, v3, Until: 24:00, v1,'''
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.assign_values(**kwargs)

    def assign_values(self, **values):
        for key in values:
            self.Fields = self.Fields.replace(key, str(values[key]))