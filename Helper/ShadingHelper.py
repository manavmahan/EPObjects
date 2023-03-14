from IDFObject.WindowShadingControl import WindowShadingControl
from IDFObject.FenestrationSurface.Detailed import Detailed as Fenestration
from IDFObject.BuildingSurface.Detailed import Detailed as BuildingSurface

def AddShading(epObjects):
    epObjects += list(CreateShading(epObjects))

def CreateShading(epObjects):
    fenestrations = list(x for x in epObjects if isinstance(x, Fenestration))
    for f in fenestrations:
        wsc = WindowShadingControl(WindowShadingControl.OnIfHighHorizontalSolar)
        wsc.Name = f'{wsc.ShadingControlType}.{f.Name}'
        buildingSurface = next(x for x in epObjects if isinstance(x, BuildingSurface) and x.Name==f.BuildingSurfaceName)
        wsc.ZoneName = buildingSurface.ZoneName
        wsc.FenestrationSurfaceName = f.Name
        yield wsc