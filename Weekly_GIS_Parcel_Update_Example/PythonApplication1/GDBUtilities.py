from email import message
import arcpy, os
from arcpy import env

arcpy.env.workspace=r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb"
arcpy.env.overwriteOutput = True
class GDBUtilities:



    
    
    ##For testing
    #Cadastral_Update_gdb = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb"
    
    
    ##for production
    Cadastral_Update_gdb = r"C:\ArcMap\Databases\Cadastral_Update.gdb"
    
    
    HAM_PARCEL_POLY_GIS01 = "\\\\caggiswa01\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\HAM_PARCEL_POLY"
    HAM_PARCEL_POLY_GIS02 = "\\\\caggiswa02\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\HAM_PARCEL_POLY"

    #HAM_PARCEL_POLY_GIS01 = r"C:\workingScratchArea\ParcelUpdateClassTests\caggiswa01\CADASTRAL.gdb\HAM_PARCEL_POLY"
    #HAM_PARCEL_POLY_GIS02 = r"C:\workingScratchArea\ParcelUpdateClassTests\ca0138egis02\CADASTRAL.gdb\HAM_PARCEL_POLY"
    
    HAM_BK_GIS01 = "\\\\caggiswa01\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\Auditor_Book_Page"
    #HAM_BK_GIS01 = r"C:\workingScratchArea\ParcelUpdateClassTests\caggiswa01\CADASTRAL.gdb\Auditor_Book_Page"                                                                                                     
    
    HAM_BK_GIS02 = "\\\\caggiswa02\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\Auditor_Book_Page"

    #HAM_BK_GIS02 = r"C:\workingScratchArea\ParcelUpdateClassTests\ca0138egis02\CADASTRAL.gdb\Auditor_Book_Page"

    #cgdConnect = r"C:\Users\WKunkler\AppData\Roaming\ESRI\Desktop10.6\ArcCatalog\Cagis.sde"

    cgdConnect = r"\\mocha\c$\batch\DatabaseConnections\cagis@2ocgd132.sde"



    Parcpoly_Condo_Combo = Cadastral_Update_gdb + "\\Parcpoly_Condo_Combo"
    Parcpoly_FGDB_Dissolved = Cadastral_Update_gdb + "\\Parcpoly_FGDB_Dissolved"
    Parcpoly_Merged_Consolidation = Cadastral_Update_gdb + "\\Parcpoly_Merged_Consolidation"
    HAM_PARCEL_ATT = Cadastral_Update_gdb + "\\Ham_Parcel_Attributes_Merged"
    
    
    #Parcpoly_Condo_Combo = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Condo_Combo"
    #Parcpoly_FGDB_Dissolved = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_FGDB_Dissolved"
    #Parcpoly_Merged_Consolidation = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation"
    
    #HAM_PARCEL_ATT = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Ham_Parcel_Attributes_Merged"
    
    

    
    #c:\ArcMap\CagisGISProjects\Parcel_Update root for layers
    ##for prod

    #for lists of len == 4, 3rd is join table, 4 is tuple of (TargetField, Join Field)
    #layers_root = r"C:\ArcMap\CagisGISProjects\Parcel_Update"
    PredefinedLayers = {"Parcpoly_Condo_lyr": [Cadastral_Update_gdb + '\\Parcpoly_Condo', ""], "Parcpoly_Condo_for_Join_Related_lyr":[Cadastral_Update_gdb + "\\Parcpoly_Condo_for_Join","", Cadastral_Update_gdb + '\\Parcel_Attributes', ("NAME", "PARCELID") ],
                       "Parcpoly_Condo_FGDB_Clear_Selected_lyr":[Cadastral_Update_gdb + '\\Parcpoly_Condo',""], "Parcpoly_Condo_FGDB_Selected_lyr":[Cadastral_Update_gdb + '\\Parcpoly_Condo',""],
                        "Condo_Units_ParcelFabric_lyr":[cgdConnect + '\\HCE.ParcelEditing\\HCE.TaxParcel_Condo_Units', "SYSTEMENDDATE is NULL"], "Parcel_Polygons_ParcelFabric_lyr": [cgdConnect + "\\HCE.ParcelEditing\\HCE.ParcelFabric_Parcels","(SystemEndDate IS NULL) and TYPE = 7"],
                        "Condo_Parcel_Polygons_lyr": [Cadastral_Update_gdb + '\\Parcpoly_Condo_Combo', "GRPPCLID like '%CD%' AND PARCELID not like '%CD%'"], 
                        "Parcpoly_Merged_Consolidation_Joined":[Cadastral_Update_gdb + "\\Parcpoly_Merged_Consolidation",""], 
                        "SubDiv_ParcFabric_lyr":[cgdConnect + '\\HCE.ParcelEditing\\HCE.ParcelFabric_Parcels', "SYSTEMENDDATE IS NULL AND TYPE = 5 AND CONVEYANCETYPE = 'Subdivision'"], "Condo_Polygons_ParcelFabric_lyr":[cgdConnect + "\\HCE.ParcelEditing\\HCE.ParcelFabric_Parcels", "SYSTEMENDDATE IS NULL AND TYPE = 5 AND CONVEYANCETYPE = 'Condominium'"],
                        "Condo_Polygons_ParcelFabric_lyr_1":[cgdConnect + "\\HCE.ParcelEditing\\HCE.ParcelFabric_Parcels", "SYSTEMENDDATE IS NULL AND TYPE = 5 AND CONVEYANCETYPE = 'Condominium'"], "ROW_lyr": [cgdConnect + '\\HCE.ParcelEditing\\HCE.ParcelFabric_Lines', "(SystemEndDate IS NULL) AND CATEGORY = 5"],
                        "BK_lyr":[Cadastral_Update_gdb+'\\Auditor_Book_Page',""], "Sub_SDE_lyr":[cgdConnect + '\\HCE.ParcelEditing\\HCE.ParcelFabric_Parcels', "SYSTEMENDDATE IS NULL AND TYPE = 5 AND CONVEYANCETYPE = 'Subdivision'" ],
                        "Condo_Unit_Joined_Attributes_lyr": [Cadastral_Update_gdb + '\\Condo_FGDB', ""], "AudBookPage_ParcelFabricLyr":[cgdConnect + "\\HCE.ParcelEditing\\HCE.Auditor_Book_Page" ,"SYSTEMENDDATE IS NULL"] }
    
    #"Condo_FGDB_lyr":[Cadastral_Update_gdb + '\\Condo_Polygons',"" ]
    #"Condopoly_FGDB_lyr":[Cadastral_Update_gdb + '\\Condo_Polygons',"" ],

    #This one is created later
    #"Parcpoly_Condo_Combo_All_Selected":[Cadastral_Update_gdb + '\\Parcpoly_Condo_Combo', ""]
    #"Parcpoly_Condo_FGDB_Related_lyr":[Cadastral_Update_gdb + "\\Parcelpoly_FGDB",""],
    for key in PredefinedLayers.keys():
        print("making feature layers")
        arcpy.MakeFeatureLayer_management(PredefinedLayers[key][0], key, PredefinedLayers[key][1])
        if len(PredefinedLayers[key]) == 4:
            continue
            
    print("done making layers!")

    
    
    
    
   
    ##Maybe still need this? This one is missing
    #Condo_FGDB_lyr = layers_root + '\\Condo_FGDB.lyr'
    
    ##for testing
    #Parcpoly_Condo_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo.lyr"
    #Parcpoly_Condo_for_Join_Related_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo_for_Join_Related.lyr"
    #Parcpoly_Condo_FGDB_Clear_Selected_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo_FGDB_Clear_Selected.lyr"
    #Parcpoly_Condo_FGDB_Selected_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo_FGDB_Selected.lyr"
    #Condo_Units_ParcelFabric_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo Units (ParcelFabric).lyr"
    #Parcel_Polygons_ParcelFabric_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcel Polygons (ParcelFabric).lyr"
    #Condo_Parcel_Polygons_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo_Parcel_Polygons.lyr"
    #Parcpoly_Condo_FGDB_Related_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo_FGDB_Related.lyr"
    #Parcpoly_Merged_Consolidation_Joined = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Merged_Consolidation_Joined.lyr"
    #Condo_FGDB_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo_FGDB.lyr"
    #Condopoly_FGDB_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condopoly_FGDB.lyr"



    #cant find
    #Parcpoly_FGDB_lyr = "C:\\ArcMap\\CagisGISProjects\\Parcel_Update\\Parcpoly_FGDB.lyr"

    ##for testing
    #in_features="C:/ArcMap/CagisGISProjects/Parcel_Update/Subdivisions (ParcelFabric).lyr"
    #SubDiv_ParcFabric_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Subdivisions (ParcelFabric).lyr"
    #Condo_Polygons_ParcelFabric_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo Polygons (ParcelFabric).lyr"
    #Condo_Polygons_ParcelFabric_lyr_1 = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo Polygons (ParcelFabric).lyr"
    #ROW_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\ROW Lines (ParcelFabric).lyr"
    #BK_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Auditor Book and Page.lyr"
    #Sub_SDE_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Ham_ParcelFabric_Subdivisions.lyr"
    #Condo_Unit_Joined_Attributes_lyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Condo_Unit_Joined_Attributes.lyr"
    #Parcpoly_Condo_Combo_All_Selected = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Parcpoly_Condo_Combo_All_Selected.lyr"

    #for prod
    






    HAM_PARCEL_ATT_GIS01 = "\\\\caggiswa01\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\Ham_Parcel_Attributes_Merged"
    #HAM_PARCEL_ATT_GIS01 = r"C:\workingScratchArea\ParcelUpdateClassTests\caggiswa01\CADASTRAL.gdb\Ham_Parcel_Attributes_Merged"
    HAM_PARCEL_ATT_GIS02 = "\\\\caggiswa02\\GISFileDS\\arcgisserver\\Data\\CADASTRAL.gdb\\Ham_Parcel_Attributes_Merged"
    #HAM_PARCEL_ATT_GIS02 = r"C:\workingScratchArea\ParcelUpdateClassTests\ca0138egis02\CADASTRAL.gdb\Ham_Parcel_Attributes_Merged"
    
    
    Ham_Subdivision_boundaries = Cadastral_Update_gdb + "\\Ham_Subdivision_Boundaries"


    #AudBookPage_ParcelFabricLyr = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Parcel_Update\Auditor Book and Page (ParcelFabric).lyr"
    
    PARCEL_ATTRIBUTES_VIEW = cgdConnect + '\\CAGIS.PARCEL_ATTRIBUTES_VIEW2'
    
    #PARCEL_ATTRIBUTES_VIEW = "Database Connections\\cagis@2ocgd132.sde\\CAGIS.PARCEL_ATTRIBUTES_VIEW2"
    cgd132_Ham_ParcFabric_sub = cgdConnect + '\\CAGIS.Ham_Parcelfabric_Subdivisions' 
    #cgd132_Ham_ParcFabric_sub = "Database Connections/cagis@2ocgd132.sde/CAGIS.Ham_Parcelfabric_Subdivisions"

    cgd132_Ham_ParcFabric_CondoAtts = cgdConnect + '\\CAGIS.Ham_Parcelfabric_Condo_Atts'
    #cgd132_Ham_ParcFabric_CondoAtts="Database Connections/cagis@2ocgd132.sde/CAGIS.Ham_Parcelfabric_Condo_Atts"

    cgd132_Ham_ParcFabric_CondoPoly = cgdConnect + '\\CAGIS.Ham_Parcelfabric_Condopoly'
    #cgd132_Ham_ParcFabric_CondoPoly = "Database Connections/cagis@2ocgd132.sde/CAGIS.Ham_Parcelfabric_Condopoly"


    CondoPoly = Cadastral_Update_gdb + "\\Condopoy_FGDB"
    #CondoPoly = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Condopoy_FGDB"
  

    CondoUnitAttr = Cadastral_Update_gdb + "\\Condo_Unit_Attributes"




    def __init__(self, emailObj):
        self.emailObj = emailObj

    def __delete(self, featureClassPath):

       
        arcpy.Delete_management(featureClassPath)

    def __helperSelectFunc(self):
        #tmp_layer = arcpy.mp.LayerFile(self.Parcpoly_Condo_lyr)
        print("helper function 1")
        #"NAME like '%CD%' AND PARCELID IS NOT NULL"
        arcpy.env.workspace = self.Cadastral_Update_gdb
        arcpy.env.overwriteOutput = True
        arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + '\\Parcelpoly_FGDB' ,"tmp_lyr")
        arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + "\\Condo_FGDB", "CondoFGDB")
        arcpy.JoinField_management("tmp_lyr", "NAME", "Condo_FGDB", "GRPPCLID")
        
        
        #arcpy.SelectLayerByAttribute_management("tmp_lyr", selection_type="NEW_SELECTION", where_clause="Parcelpoly_FGDB_NAME like '%CD%' AND CONDO_FGDB_PARCELID IS NOT NULL")
        arcpy.SelectLayerByAttribute_management("tmp_lyr", selection_type="NEW_SELECTION", where_clause="NAME like '%CD%' AND PARCELID IS NOT NULL")
       
       
        #arcpy.CalculateField_management("tmp_lyr", "Parcelpoly_FGDB.NAME", "!Condo_FGDB.PARCELID!", expression_type="PYTHON3", code_block="")
       
        #fields = arcpy.ListFields("tmp_lyr")
        #[print(field.name) for field in fields] 
        arcpy.CalculateField_management("tmp_lyr", field="NAME", expression="!PARCELID!", expression_type="PYTHON3", code_block="")
        arcpy.SelectLayerByAttribute_management("tmp_lyr", selection_type="CLEAR_SELECTION", where_clause="")

        #arcpy.RemoveJoin("tmp_lyr")
    def __helperSelectFunc2(self):
        print("helper function 2")
        #arcpy.CalculateField_management(self.Cadastral_Update_gdb + "\\Parcpoly_Condo_Combo", field="Condo_FGDB.PARCELID", expression="!Parcelpoly_FGDB.NAME!", expression_type="PYTHON_9.3", code_block="")
        arcpy.CalculateField_management(self.Cadastral_Update_gdb + "\\Parcpoly_Condo_Combo", field="PARCELID", expression="!NAME!", expression_type="PYTHON3", code_block="")



    def __featureClassCreate(self, key, tupleVals):
        if len(tupleVals) == 5:
            print(tupleVals[4])
        if key == "Parcpoly_Condo_for_Join_Related_lyr":
            arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + "\\Parcpoly_Condo_for_Join", "Parcpoly_Condo_for_Join_Related_lyr")
            arcpy.MakeTableView_management(self.PredefinedLayers[key][2], self.PredefinedLayers[key][2].split("\\")[-1])
           
            arcpy.AddJoin_management(key, self.PredefinedLayers[key][3][0], self.PredefinedLayers[key][2].split("\\")[-1], self.PredefinedLayers[key][3][1])
            
        elif key == "Condo_Unit_Joined_Attributes_lyr":
            arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + "\\Condo_FGDB", "Condo_Unit_Joined_Attributes_lyr")
        arcpy.FeatureClassToFeatureClass_conversion(key, tupleVals[0], tupleVals[1], tupleVals[2])
        if tupleVals[3] == 1:
            self.__helperSelectFunc()
        elif tupleVals[3] == 2:
            self.__helperSelectFunc2()
        elif tupleVals[3] == 3:
            arcpy.FeatureClassToFeatureClass_conversion(key, tupleVals[0], tupleVals[1], tupleVals[2])
            arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + "\\Parcelpoly_FGDB", tupleVals[5])

    def createGDB(self, listOfServices):
        
        
        try:
            
            print("deleting services")
            [self.__delete(service) for service in listOfServices]
            
        


           
            #     "Parcpoly_Condo_FGDB_Clear_Selected_lyr"       
            listKeys = ["AudBookPage_ParcelFabricLyr", "Condo_Polygons_ParcelFabric_lyr_1", "Condo_Units_ParcelFabric_lyr", "Parcel_Polygons_ParcelFabric_lyr", "Parcpoly_Condo_FGDB_Related_lyr", self.Cadastral_Update_gdb + '\\Parcpoly_Condo', "Parcpoly_Condo_for_Join_Related_lyr", \
                        "SubDiv_ParcFabric_lyr", "Condo_Polygons_ParcelFabric_lyr", "Condo_Unit_Joined_Attributes_lyr"]

            listTups = [(self.Cadastral_Update_gdb, "Auditor_Book_Page", "SYSTEMENDDATE IS NULL","",0,"Exporting Parcel_Attributes from SDE..."), (self.Cadastral_Update_gdb, "Condopoy_FGDB","",0),(self.Cadastral_Update_gdb, "Condo_FGDB","",0, "Exporting Condo Units from parcelFabric..."),\
                (self.Cadastral_Update_gdb, "Parcelpoly_FGDB","",3,"Exporting tax parcels from parcelFabric...","Parcpoly_Condo_FGDB_Related_lyr"), (self.Cadastral_Update_gdb, "Parcpoly_Condo", "",1,"Combining tax parcels with condo units to create parcpoly_condos..."),\
                    ( self.Cadastral_Update_gdb, "Parcpoly_Condo_for_Join","",0,"Combining tax parcels with condo units to create parcpoly_condos_for join..."), (self.Cadastral_Update_gdb, "Parcpoly_Condo_Combo","",2,"Combining tax parcels with condo units to create the final parcpoly_condos_combo..."),\
                   (self.Cadastral_Update_gdb, "Ham_Subdivision_Boundaries","",0,"Copying subdivisions..."),(self.Cadastral_Update_gdb, "Condopoly_FGDB","",0,"Copying Condo_polygons..."),(self.Cadastral_Update_gdb, "Condo_Unit_Attributes","",0,"Copying Condo_Unit_Attributes...") ]
            

            dictFeatures = dict(zip(listKeys, listTups))




            print("Exporting Parcel_Attributes from SDE...")
            
            arcpy.TableToTable_conversion(self.cgdConnect + "\\CAGIS.PARCEL_ATTRIBUTES_VIEW2",self.Cadastral_Update_gdb, "Parcel_Attributes", "")
            
            
            [self.__featureClassCreate(key, dictFeatures[key]) for key in listKeys]


            print("Converting polygons to Ham_Parcel_Attributes_Merged points...")
            arcpy.MakeFeatureLayer_management(self.Cadastral_Update_gdb + '\\Parcpoly_Condo_Combo',"Parcpoly_Condo_Combo_All_Selected")
            arcpy.FeatureToPoint_management("Parcpoly_Condo_Combo_All_Selected", self.Cadastral_Update_gdb+"\\Ham_Parcel_Attributes_Merged", "INSIDE")

            Subject = "Parcel polygon creation succeeded!"
            Msg = ("Parcel polygon feature class has been created in file geodatabase!")
            print(Msg)
            self.emailObj.sendMessage(Subject, Msg)



        except Exception as e:
            Msg = (" An error occurred while trying to create parcel polygon feature class in file geodatabase!")
            Msg +=  "\n " + str(e)
            Subject = "ERROR: Parcel polygon creation failed!"
            print(e)
            #return (Subject, Msg)
            self.emailObj.sendMessage(Subject, Msg)
           
        
        
    def validateData(self, updateFrequency, processOutcome):

        ValidateData = 'SUCCESS'


        
        try:
          
            FGDB = 'CADASTRAL.gdb'
            if (updateFrequency == 'CagisOnline'):
                print('Cagis Online Data')
                validateFGDB = os.path.join(r'\\caggiswa01\GISFileDS\arcgisserver\Data',FGDB)
                #validateFGDB = os.path.join(r"C:\workingScratchArea\ParcelUpdateClassTests\caggiswa01", FGDB)
            else:
                print('Go Cagis Data')
                validateFGDB = os.path.join(r'\\caggiswa02\GISFileDS\arcgisserver\Data',FGDB)
                #validateFGDB = os.path.join(r"C:\workingScratchArea\ParcelUpdateClassTests\ca0138egis02", FGDB)
            arcpy.env.workspace = validateFGDB
            fcList = arcpy.ListFeatureClasses()
           
            messages = ""
            #may need to do something about these messages
            print('Weekly Parcel Extraction Validation Results (' + updateFrequency +'):')
            messages += 'Weekly Parcel Extraction Validation Results (' + updateFrequency +'):\n'
            print('---------------------------------------------')
            messages += '---------------------------------------------\n'
            dataDict={
            "HAM_PARCEL_POLY": (418000,425000), "HAM_PARCEL_POLY_MERGED_OWNERSHIP": (350000,360000), "CONDOMINIUM_UNITS":(21000, 23000), 'Condominium_Common_Areas': (1900,2200), 'Auditor_Book_Page': (2600,2800),
            'Condo_polygons': (20000, 25000), 'Ham_Parcel_Attributes_Merged': (410000,435500), 'Ham_Subdivision_Boundaries': (9500, 12500)
            }
            print(dataDict)
            FiltList = list(filter(lambda x: x in dataDict.keys(), fcList))
            
            for fc in FiltList:
                
                result = int(arcpy.GetCount_management(fc).getOutput(0))
                if result > dataDict[fc][0] and result < dataDict[fc][1]:
                    print("count(" + fc + ") = " + str(result))
                    messages += "count(" + fc + ") = " + str(result)
                else:
                    print("FAILED - count("+fc+") = "+str(result))
                    messages += "FAILED - count("+fc+") = "+str(result)
                    ValidateData = "FAILURE"

            if ValidateData == 'FAILURE':
                        processOutcome.append('Failure - ValidateFGDB Function')
                        print('Validation Failed! \n')
                        messages+='\n******At least one or more feature(s) failed on data validation!!!****** \r\n'
                        messages+='One or more data failed data validation - ValidateFGDB Function\r\n'
                        self.emailObj.sendMessage('Failure - ValidateFGDB Function', messages)
            else:
                        print('Data Validation Successfull! \n')
                        messages += '\n Validation Successfull! \r\n'
                        self.emailObj.sendMessage('Data Validation Successfull!', messages)

        except RuntimeError as e:
            #processOutcome.append('One or more data failed data validation - ValidateFGDB Function')
            #messages.append(e.message)
            Msg = (" One or more data failed data validation - ValidateFGDB Function")
            Msg +=  "\n " + e.message
            Subject = "ERROR: Parcel polygon Validation failed!"
            print(str(e))
            #return (Subject, Msg)
            self.emailObj.sendMessage(Subject, Msg)
        except Exception as e:
            Msg = (" One or more data failed data validation - ValidateFGDB Function")
            Msg +=  "\n " + str(e)
            Subject = "ERROR: Parcel polygon Validation failed!"
            print(str(e))
            self.emailObj.sendMessage(Subject, Msg)
            #return (Subject, Msg)
            
