from IDFObject.IDFObject import IDFObject
    
class EquipmentConnections(IDFObject):
    __IDFName__ = 'ZoneHVAC:EquipmentConnections'
    Properties = [
        'ZoneName',
        'ListNameZoneEquipment',
        'ListNameZoneAirInletNodes',
        'ListNameZoneAirExhaustNodes',
        'ZoneAirNodeName',
        'ZoneReturnAirNodeorNodeListName',
        'ZoneReturnAirNode1FlowRateFractionScheduleName',
        'ZoneReturnAirNode1FlowRateBasisNodeorNodeListName',
    ]

    def __init__(self, propertiesDict: dict()):
        super().__init__(self.Properties, propertiesDict)

EquipmentConnections.Default = dict(
    ListNameZoneEquipment = '',
    ListNameZoneAirInletNodes = '',
    ListNameZoneAirExhaustNodes = ' ',
    ZoneReturnAirNode1FlowRateFractionScheduleName = '',
    ZoneReturnAirNode1FlowRateBasisNodeorNodeListName = '',
)
