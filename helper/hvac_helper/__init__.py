def is_zonelist_with_thermostat(zonelist, thermostats):
    thermostat_name = f'Thermostat.{zonelist.Name}'
    return any(x for x in thermostats if x.Name==thermostat_name)

def get_zonelists_with_thermostat(zonelists, thermostats):
    return filter(lambda zl: is_zonelist_with_thermostat(zl, thermostats), zonelists)