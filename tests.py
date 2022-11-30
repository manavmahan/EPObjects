import unittest

from Initialiser import Initialise

class TestInialiser(unittest.TestCase):
    idfObjects = dict(Initialise('Data'))
    def testReadFileBuilding(self):
        self.assertEqual("Building,Building1,0.0,,0.01,0.01,FullExterior,10,6;", 
        str(self.idfObjects['Building'][0]))

    def testReadFileBuildingSurfaceDetailed(self):
        self.assertEqual('BuildingSurface:Detailed,Floor0.Zone0,Floor,GroundFloorConstruction,Zone0,Ground,,NoSun,NoWind,0,4, 0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,0.0;', 
        str(self.idfObjects['BuildingSurface:Detailed'][0]))

    def testReadFileConstruction(self):
        self.assertEqual("Construction,BrickWallWithInsulation,Brick,WallInsulation;",  str(self.idfObjects['Construction'][0]))
    
    def testReadFileHVACTemplatePlantBoiler(self):
        self.assertEqual("HVACTemplate:Plant:Boiler,Boiler1,HotWaterBoiler,autosize,0.95,Electric,1,1.2,0.1,1.1,0.9,99;",
        str(self.idfObjects['HVACTemplate:Plant:Boiler'][0]))

    def testReadFileMaterial(self):
        self.assertEqual("Material,Brick,0.2,0.5,100,100,0.9,0.6,0.1;",  str(self.idfObjects['Material'][0]))

if __name__ == '__main__':
    unittest.main()
