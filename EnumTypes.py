from enum import Enum

class Distribution(Enum):
    Normal = 'Normal'
    Triangular = 'Triangular'
    Uniform = 'Uniform'

    def __str__(self):
        return str(self.value)

class Frequency(Enum):
    Annual = 'Annual'
    Hourly = 'Hourly'
    Monthly = 'Monthly'

class ParameterType(Enum):
    # Building Operation

    # Thermal Properties
    GValue = "g-value"
    UValue = "u-value"

    def __str__(self):
        return str(self.value)

def ParameterUnit(Enum):
    UValue = "W/m\u00b2K"
    HeatCapacity = 'kW/kg'
    def __str__(self):
        return str(self.value)

class SamplingScheme(Enum):
    LHS = "Latin Hypercube Sampling"
    Sobol = "Sobol Sampling"
    MonteCarlo = "Monte Carlo Sampling"

class SurfaceType(Enum):
    Ceiling = "Ceiling"
    Floor = "Floor"
    Wall = "Wall"
    Roof = "Roof"

    def __str__(self):
        return str(self.value)