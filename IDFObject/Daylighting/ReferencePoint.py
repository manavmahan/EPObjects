from ...GeometryObject.XYZ import XYZ

class ReferencePoint:
    def __init__(self, name: str, zoneName: str, point: XYZ):
        self.Name = name
        self.ZoneName = zoneName
        self.Point = point

    def WriteToIDF(self):
        return "\n".join([
            f"DayLighting:{self.__name__},",
            f"{self.Name},",
            f"{self.ZoneName},",
            str(self.Point),
        ]) + ";"
