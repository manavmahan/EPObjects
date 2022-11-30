import pandas as pd

class SimpleGlazingSystem:
    Properties = {
        'UValue': None,
        'GValue': None,
        'Visible Transmittance': None,
    }

    def __init__(self, name: str, properties: dict()) -> None:
        self.Name = name
        for property in self.Properties.keys():
            if property in properties: self.Properties[property] = properties[property]

    def WriteToIDF(self):
        return f"WindowMaterial:{self.__class__.__name__}, {self.Name}, {','.join(str(x) for x in self.Properties.values())};"

def InitialiseMaterial(file):
    data = pd.read_csv(file, index_col=0)
    for name in data.index:
        yield SimpleGlazingSystem(name, data.loc[name].to_dict())