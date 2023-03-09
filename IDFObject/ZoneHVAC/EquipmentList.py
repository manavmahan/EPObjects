from IDFObject.IDFObject import IDFObject
    
class EquipmentList(IDFObject):
    __IDFName__ = 'ZoneHVAC:EquipmentList'
    Properties = [
        'Name',
        'LoadDistributionScheme',
        'ZoneEquipment1ObjectType',
        'ZoneEquipment1Name',
        'ZoneEquipment1CoolingSequence',
        'ZoneEquipment1HeatingorNoLoadSequence',
        'ZoneEquipment1SequentialCoolingFractionScheduleName',
        'ZoneEquipment1SequentialHeatingFractionScheduleName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

EquipmentList.Default = dict(
    LoadDistributionScheme = 'SequentialLoad',
    ZoneEquipment1CoolingSequence = 1,
    ZoneEquipment1HeatingorNoLoadSequence = 1,
    ZoneEquipment1SequentialCoolingFractionScheduleName = '',
    ZoneEquipment1SequentialHeatingFractionScheduleName = ''
)
