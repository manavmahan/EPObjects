class StringList(list):
    def __init__(self, iterable):
        if (isinstance(iterable, str)):
            iterable = iterable.split(',')
        super().__init__(str(item) for item in iterable)

    def __setitem__(self, index, item):
        super().__setitem__(index, str(item))

    def insert(self, index, item):
        super().insert(index, str(item))

    def append(self, item):
        super().append(str(item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(str(item) for item in other)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ','.join(self)
