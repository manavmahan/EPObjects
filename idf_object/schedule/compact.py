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

    no_cooling = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31, For: Alldays, Until: 24:00, 35'''
    )

    four_and_half_days = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31,
        For: Mondays Tuesdays Wednesday Thursdays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,
            Until: t1, v1, Until: t2, v2, Until: 24:00, v1,
        For: Fridays,
            Until: t1, v1, Until: t3, v3, Until: 24:00, v1,
        For: Weekends Holidays,
            Until: 24:00, v1'''
    )

    typical_house = dict(
        ScheduleTypeLimitsName = 'AnyNumber',
        Fields = '''Through 12/31,
        For: Mondays Tuesdays Wednesday Thursdays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,
            Until: t1, v1, Until: t2, v2, Until: t3, v3, Until: t4, v4, Until: 24:00, v1,
        For: Fridays,
            Until: t1, v1, Until: t2, v2, Until: t5, v5, Until: t4, v4, Until: 24:00, v1,
        For: Weekends Holidays,
            Until: t1, v1, Until: t6, v6, Until: t7, v7, Until: 24:00, v1'''
    )

    def __init__(self, **kwargs):
        props = dict(getattr(self, kwargs.get('default', 'default')))
        props.update(kwargs)
        super().__init__(self.Properties, props)
        self.assign_values(**kwargs)
        self.type = kwargs.get('default', 'default')

    def assign_values(self, **values):
        for key in values:
            self.Fields = self.Fields.replace(key, str(values[key]))

    def fill_default_times(self):
        if self.type == "four_and_half_days":
            keys = dict(
                t1='07:30', t2='17:00', t3='13:00',
            )
        elif self.type == "typical_house":
            keys = dict(
                t1='06:00', t2='08:00', t3='18:00', t4='22:00', t5="18:00", t6="16:00", t7="22:00",
            )
        else:
            return
        self.assign_values(**keys)

    def distribute_weekly_hours(self, hours):
        if self.type == "typical_house":
            key_combinations = [
                dict(
                    hours=100,
                    t1='05:00', t2='07:00', t3='21:00', t4='23:00', t5="18:00", t6="16:00", t7="22:00",
                ),
                dict(
                    hours=104,
                    t1='05:00', t2='07:00', t3='20:00', t4='23:00', t5="18:00", t6="16:00", t7="22:00",
                ),
                dict(
                    hours=108,
                    t1='05:00', t2='07:00', t3='19:00', t4='23:00', t5="18:00", t6="16:00", t7="22:00",
                ),
                dict(
                    hours=112,
                    t1='06:00', t2='08:00', t3='19:00', t4='23:00', t5="18:00", t6="16:00", t7="22:00",
                ),
                dict(
                    hours=116,
                    t1='06:00', t2='08:00', t3='18:00', t4='22:00', t5="18:00", t6="16:00", t7="22:00",
                ),
                dict(
                    hours=120,
                    t1='07:00', t2='09:00', t3='18:00', t4='22:00', t5="18:00", t6="16:00", t7="22:00",
                )
            ]
            min_diff = 10000
            selected = None
            for keys in key_combinations:
                if abs(keys['hours'] - hours) < min_diff:
                    min_diff = abs(keys['hours'] - hours)
                    selected = keys
            self.assign_values(**selected)

    def set_setpoints(self, value):
        setoff = 4 if 'Heating' in self.Name else -4
        if self.type == "default":
            self.assign_values(v1=value)
        elif self.type == "four_and_half_days":
            self.assign_values(v1=value-setoff, v2=value, v3=value-setoff)