from enum import Enum

class Direction(Enum):
    N = "North"
    E = "East"
    W = "West"
    S = "South"
    def __str__(self):
        return str(self.value)

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
    Occupants = "Occupants"
    Occupancy = "Occupancy"
    StartTime = "Start Time"
    EndTime = "End Time"
    LightHeatGain = "Light Heat Gain"
    EquipmentHeatGain = "Equipment Heat Gain"

    # Envelope Properties
    Permeability = "Permeability"
    GValue = "g-value"
    UValue = "u-value"

    # Internal Mass
    InternalMass = "Internal Mass"

    # Internal Heat Gains
    People = "People"

    # System Efficiency
    BoilerEfficiency = "Boiler Efficiency"

    # Zone Conditions
    HeatingSetpoint = "HeatingSetpoint"

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
    Roof = "Roof"
    Wall = "Wall"
    Window = "Window"

    def __str__(self):
        return str(self.value)