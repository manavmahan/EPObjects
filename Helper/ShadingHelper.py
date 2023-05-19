from IDFObject.WindowShadingControl import WindowShadingControl
from IDFObject.FenestrationSurface.Detailed import Detailed as Fenestration
from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface

def AddShading(epObjects):
    epObjects += list(CreateShading(epObjects))

def CreateShading(epObjects):
    fenestrations = list(x for x in epObjects if isinstance(x, Fenestration))
    for f in fenestrations:
        buildingSurface = next(x for x in epObjects if isinstance(x, BuildingSurface) and x.Name==f.BuildingSurfaceName)
        wsc = WindowShadingControl(
            Name = f'{WindowShadingControl.default["ShadingControlType"]}.{f.Name}',
            ZoneName = buildingSurface.ZoneName,
            FenestrationSurfaceName = f.Name
        )
        yield wsc