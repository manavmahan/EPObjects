import unittest

from Initialiser import Initialise

class TestInialiser(unittest.TestCase):
    idfObjects = dict(Initialise('Data'))
    def testReadFileBuilding(self):
        self.assertEqual("Building,Building1,0.0,,0.01,0.01,FullExterior,10,6;", str(self.idfObjects['Building'][0]))

    def testReadFileBuildingSurfaceDetailed(self):
        self.assertEqual('BuildingSurface:Detailed,Floor0.Zone0,Floor,GroundFloorConstruction,Zone0,Ground,,NoSun,NoWind,0,4, 0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,0.0;', str(self.idfObjects['BuildingSurface:Detailed'][0]))

    def testReadFileConstruction(self):
        self.assertEqual("Construction,BrickWallWithInsulation,Brick,WallInsulation;",  str(self.idfObjects['Construction'][0]))
    
    def testReadFileConvergenceLimits(self):
        self.assertEqual("ConvergenceLimits,0,20,2,8;", str(self.idfObjects['ConvergenceLimits'][0]))

    def testReadFileDaylightingControls(self):
        self.assertEqual("Daylighting:Controls,DayLightControlForOffice:0:1,Office:0:1,SplitFlux,Office_OccupancySchedule,Continuous,0.3,0.3,3,1,DayLightReferencePoint5forOffice:0:1,180,22,2,DayLightReferencePoint1forOffice:0:1,0.2,500,DayLightReferencePoint2forOffice:0:1,0.2,500;", str(self.idfObjects['Daylighting:Controls'][0]))

    def testReadFileDaylightingReferencePoint(self):
        self.assertEqual("Daylighting:ReferencePoint,DayLightReferencePoint1forOffice:0:1,Office:0:1,13.815,7.15,0.9;", str(self.idfObjects['Daylighting:ReferencePoint'][0]))

    def testReadFileElectricEquipment(self):
        self.assertEqual("ElectricEquipment,Equipment_Office,Office,Office_EquipmentSchedule,Watts/area,,12,,,0.1,;", str(self.idfObjects['ElectricEquipment'][0]))

    def testReadFileHVACTemplatePlantBoiler(self):
        self.assertEqual("HVACTemplate:Plant:Boiler,Boiler1,HotWaterBoiler,autosize,0.95,Electric,1,1.2,0.1,1.1,0.9,99;",
        str(self.idfObjects['HVACTemplate:Plant:Boiler'][0]))

    def testReadFileHVACTemplatePlantMixedWaterLoop(self):
        self.assertEqual("HVACTemplate:Plant:MixedWaterLoop,OnlyWaterLoop,,Intermittent,Default,,,34,,20,ConstantFlow,179352,SinglePump,Yes,Yes,Water,6,SequentialLoad;", str(self.idfObjects['HVACTemplate:Plant:MixedWaterLoop'][0]))

    def testReadFileHVACTemplatePlantTower(self):
        self.assertEqual("HVACTemplate:Plant:Tower,MainTower,SingleSpeed,autosize,autosize,autosize,autosize,autosize,1,1.2;", str(self.idfObjects['HVACTemplate:Plant:Tower'][0]))

    def testReadFileHVACTemplateThermostat(self):
        self.assertEqual("HVACTemplate:Thermostat,Office_Thermostat,Office_HeatingSetPointSchedule,,Office_CoolingSetPointSchedule,;", str(self.idfObjects['HVACTemplate:Thermostat'][0]))

    def testReadFileHVACTemplateZoneWaterToAirHeatPump(self):
        self.assertEqual("HVACTemplate:Zone:WaterToAirHeatPump,Office:0:1,Office_Thermostat,autosize,autosize,,1.2,1.2,Flow/Person,0.00944,,,,,DrawThrough,0.7,75,0.9,Coil:Cooling:WaterToAirHeatPump:EquationFit,autosize,autosize,3.2,Coil:Heating:WaterToAirHeatPump:EquationFit,autosize,3.2,,autosize,2.5,60,0.01,60,,Electric,SupplyAirTemperature,12.5,,SupplyAirTemperature,50.0,,,,,,,;", str(self.idfObjects['HVACTemplate:Zone:WaterToAirHeatPump'][0]))

    def testReadFileInternalMass(self):
        self.assertEqual("InternalMass,Office:0:1:InternalMass:01,InternalMass,Office:0:1,7.499853;", str(self.idfObjects['InternalMass'][0]))

    def testReadFileLights(self):
        self.assertEqual("Lights,Light_Office,Office,Office_LightSchedule,Watts/area,,7,,0,0.1,0.18,;", str(self.idfObjects['Lights'][0]))

    def testReadFileMaterial(self):
        self.assertEqual("Material,Brick,0.2,0.5,100,100,0.9,0.6,0.1;",  str(self.idfObjects['Material'][0]))

    def testReadFileOutputControlTableStyle(self):
        self.assertEqual("OutputControl:Table:Style,XMLandHTML;", str(self.idfObjects['OutputControl:Table:Style'][0]))

    def testReadFileOutputDiagnostics(self):
        self.assertEqual("Output:Diagnostics,DisplayAdvancedReportVariables,DisplayExtraWarnings;", str(self.idfObjects['Output:Diagnostics'][0]))

    def testReadFileOutputPreprocessorMessage(self):
        self.assertEqual("Output:PreprocessorMessage,ExpandObjects,Warning,Preprocessorwarning;", str(self.idfObjects['Output:PreprocessorMessage'][0]))

    def testReadFileOutputSurfacesDrawing(self):
        self.assertEqual("Output:Surfaces:Drawing,dxf;", str(self.idfObjects['Output:Surfaces:Drawing'][0]))

    def testReadFileOutputTableSummaryReports(self):
        self.assertEqual("Output:Table:SummaryReports,ZoneComponentLoadSummary,ComponentSizingSummary,EquipmentSummary,HVACSizingSummary,ClimaticDataSummary,OutdoorAirSummary,EnvelopeSummary;", str(self.idfObjects['Output:Table:SummaryReports'][0]))

    def testReadFileOutputVariable(self):
        self.assertEqual("Output:Variable,*,ZoneAirSystemSensibleHeatingRate,Annual;", str(self.idfObjects['Output:Variable'][0]))

    def testReadFileOutputVariableDictionary(self):
        self.assertEqual("Output:VariableDictionary,idf;", str(self.idfObjects['Output:VariableDictionary'][0]))

    def testReadFilePeople(self):
        self.assertEqual("People,People_Office,Office,Office_OccupancySchedule,Area/Person,,,22,0.1,,Office_ActivitySchedule,3.82e-08,,ZoneAveraged,,WorkEffSch,DynamicClothingModelASHRAE55,,,AirVeloSch,Fanger;", str(self.idfObjects['People'][0]))

    def testReadFileRunPeriod(self):
        self.assertEqual("RunPeriod,RunPeriod1,1,1,,12,31,,,No,No,No,Yes,Yes,No;", str(self.idfObjects['RunPeriod'][0]))

    def testReadFileScheduleCompact(self):
        self.assertEqual("Schedule:Compact,OfficeHeatingSetPointSchedule,,Through: 12/31,For: WeekDays SummerDesignDay WinterDesignDay CustomDay1 CustomDay2,Until: 6:30,15,Until: 18:30,20,Until: 24:00,15,For: WeekendsHoliday,Until: 24:00,15;", str(self.idfObjects['Schedule:Compact'][0]))

    def testReadFileScheduleTypeLimits(self):
        self.assertEqual("ScheduleTypeLimits,activityLevel,0,,Continuous,activitylevel;", str(self.idfObjects['ScheduleTypeLimits'][0]))

    def testReadFileSimulationControl(self):
        self.assertEqual("SimulationControl,Yes,Yes,Yes,No,Yes;", str(self.idfObjects['SimulationControl'][0]))

    def testReadFileSiteGroundTemperatureBuildingSurface(self):
        self.assertEqual("Site:GroundTemperature:BuildingSurface,6.17,5.07,5.33,6.27,9.35,12.12,14.32,15.48,15.2,13.62,11.08,8.41;", str(self.idfObjects['Site:GroundTemperature:BuildingSurface'][0]))

    def testReadFileSiteLocation(self):
        self.assertEqual("Site:Location,MUNICH_DEU,48.13,11.7,1,529;", str(self.idfObjects['Site:Location'][0]))

    def testReadFileSizingPeriodWeatherFileDays(self):
        self.assertEqual("SizingPeriod:WeatherFileDays,Summer including Extreme Summer days,7,18,7,25,SummerDesignDay,Yes,Yes;", str(self.idfObjects['SizingPeriod:WeatherFileDays'][0]))

    def testReadFileTimestep(self):
        self.assertEqual("Timestep,6;", str(self.idfObjects['Timestep'][0]))

    def testReadFileVersion(self):
        self.assertEqual("Version,9.2.0;", str(self.idfObjects['Version'][0]))

    def testReadFileWindowMaterialShade(self):
        self.assertEqual("WindowMaterial:Shade,ROLLSHADE,0.3,0.5,0.3,0.5,0.9,0.05,0.003,0.1,0.05,0,0.5,0.5,0, ;", str(self.idfObjects['WindowMaterial:Shade'][0]))

    def testReadFileWindowMaterialShade(self):
        self.assertEqual("WindowMaterial:Shade,ROLLSHADE,0.3,0.5,0.3,0.5,0.9,0.05,0.003,0.1,0.05,0,0.5,0.5,0,;", str(self.idfObjects['WindowMaterial:Shade'][0]))

    def testReadFileWindowMaterialSimpleGlazingSystem(self):
        self.assertEqual("WindowMaterial:SimpleGlazingSystem,GlazingMaterial,0.72,0.6,0.1;", str(self.idfObjects['WindowMaterial:SimpleGlazingSystem'][0]))

    def testReadFileWindowShadingControl(self):
        self.assertEqual("WindowShadingControl,CONTROLONZONETEMPWindow_On_Office:0:1:East:Wall:2,Office:0:1,,InteriorShade,,OnIfHighZoneAirTemperature,,23,NO,NO,ROLLSHADE,,,,DayLightControlForOffice:0:1,,Window_On_Office:0:1:East:Wall:2;", str(self.idfObjects['WindowShadingControl'][0]))

    def testReadFileZone(self):
        self.assertEqual("Zone,Office:0:1;", str(self.idfObjects['Zone'][0]))

    def testReadFileZoneInfiltrationDesignFlowRate(self):
        self.assertEqual("ZoneInfiltration:DesignFlowRate,Infiltration_Office,Office,SpaceInfiltrationSchedule,AirChanges/Hour,,,,0.337,0.606,0.03636,0.1177165,0;", str(self.idfObjects['ZoneInfiltration:DesignFlowRate'][0]))

    def testReadFileZoneList(self):
        self.assertEqual("ZoneList,Office,Office:0:1,Office:0:2;", str(self.idfObjects['ZoneList'][0]))

if __name__ == '__main__':
    unittest.main()
