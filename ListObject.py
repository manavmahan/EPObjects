class ListObject:
    def __init__(self, values = list()):
        self.Values = values

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ','.join(str(x) for x in self.Values)

    def AddObject(self, other):
        self.Values += [other]
