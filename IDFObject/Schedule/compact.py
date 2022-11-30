class Compact():
    Lines = None

    def __init__(self, file: str):
        with(open(file)) as f:
            self.Lines = "\n".join([x for x in f.readlines() if x[0]!='#'])

    def WriteToIDF(self):
        return "\n".join([
            f"Schedule:{self.__class__.__name__},",
            f"{self.Name},",
            f"{self.ScheduleLimitName},",
            f"{self.Lines};",
        ])