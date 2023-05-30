from idf_object.windowshadingcontrol import WindowShadingControl
from idf_object.fenestrationsurface.detailed import Detailed as Fenestration
from idf_object.buildingsurface.detailed import Detailed as BuildingSurface

def AddShading(epObjects):
    epObjects += list(CreateShading(epObjects))

def CreateShading(epObjects):
    fenestrations = list(x for x in epObjects if isinstance(x, Fenestration))
    for f in fenestrations:
        buildingSurface = next(x for x in epObjects if isinstance(x, BuildingSurface) and x.Name==f.BuildingSurfaceName)
        if buildingSurface.OutsideBoundaryCondition == 'Outdoors':
            wsc = WindowShadingControl(
                Name = f'{WindowShadingControl.default["ShadingControlType"]}.{f.Name}',
                ZoneName = buildingSurface.ZoneName,
                FenestrationSurfaceName = f.Name
            )
            yield wsc