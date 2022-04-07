import arcpy, smtplib, string, sys, datetime, time, os, urllib, json, getpass, arcview
import subprocess
from arcpy import env
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText




class UpdateGDBs:

    def __init__(self,emailObj):
        self.emailObj = emailObj

    
    def callIndexAndField(self, featureName, index):
        dictContainer = dict()
        
        for i in index.fields:
            if "shape" in index.name.lower():
                try:
                    print("adjusting spatial indexes for " + featureName)
                    arcpy.AddSpatialIndex_management(featureName)
                except Exception as err:
                    Msg = (" Parcel_Update_Class: An error occurred while trying to recreate spatial indexes in FGDB")
                    Msg += "\n " + err.message
                    Subject = "ERROR: Parcel Index Update Failure"
                    self.emailObj.sendMessage(Subject, Msg)
                    #return (Subject, Msg)

            elif "OBJECTID" not in index.name.upper():
                try:
                    print("adjusting attribute indexes for " + featureName)
                    dictContainer[featureName] = (index.name, i.name)
                    arcpy.RemoveIndex_management(featureName, str(dictContainer[featureName][0]))
                    arcpy.AddIndex_management(featureName, dictContainer[featureName][1], dictContainer[featureName][0])
                except Exception as err:
                    Msg = (" Parcel_Update_Class: An error occurred while trying to recreate indexes in FGDB")
                    Msg +=  "\n " + err.message
                    Subject = "ERROR: Parcel Index Update Failure!"
                    self.emailObj.sendMessage(Subject, Msg)
                    #return (Subject, Msg)
        
                    
    def rebuildIndexSDE(self, sdeConnect, filename):
        try:
            arcpy.RebuildIndexes_management(sdeConnect, "NO_SYSTEM", filename, "ALL")
        except Exception as err:
            Msg = (" Parcel_Update_Class: An error occured while trying to rebuild SDE indexes")
            Msg += "\n " + err.message
            Subject = "ERROR: Parcel Index Update Failure!"
            self.emailObj.sendMessage(Subject, Msg)
            #return (Subject, Msg)

    def truncateAppendFGDB(self, inputFeature, OtherSrcFeature, sdeFile = None):

        print("Truncating features from existing features {0}".format(inputFeature))
        try:
            arcpy.TruncateTable_management(inputFeature)
            arcpy.Append_management(OtherSrcFeature, inputFeature, "NO_TEST")
            if sdeFile == None:
                indexes = arcpy.ListIndexes(inputFeature)
                for index in indexes:
                    self.callIndexAndField(inputFeature, index)
            else:
                self.rebuildIndexSDE(sdeFile, inputFeature)
        except Exception as e:
            print(str(e))

            Msg = (" There was an error with the update process for " + inputFeature)
            Msg += "\n " + str(e)
            Subject = "Error! Truncate and Append failed"
            self.emailObj.sendMessage(Subject, Msg)
            #return (Subject, Msg)
            


    def create_merged_parcpoly1(self,inFc, outPath, outFc, whereClause):
        try:
            fullOutFc = os.path.join(outPath, outFc)
            print("Deleting condo parcels polygons...")
            arcpy.Delete_management(fullOutFc)

            print("Creating updated condo parcel polygons")
            arcpy.FeatureClassToFeatureClass_conversion(inFc,outPath, outFc, whereClause)

            
            
        except Exception as e:
            Msg = (" There was an error with the update process for " + inFc)
            Msg += "\n " + str(e)
            Subject = "ERROR: creating merged consolidation file failed in create_merged_parcpoly1!"
            self.emailObj.sendMessage(Subject, Msg)
            #return (Subject, Msg)


    def create_merged_parcpoly2(self, tempLyr, outPath, outFc, whereClause, fieldName, expression, originFeature, dissolveBool = False, NeedsFeature = False ):

        try:
            

            DissolvedLayer=os.path.join(outPath, outFc)
            arcpy.Delete_management(DissolvedLayer)
            ##for dev
            #cadastral_update_gdb = r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb"
            cadastral_update_gdb = r"C:\ArcMap\Databases\Cadastral_Update.gdb"
            if NeedsFeature == True and originFeature == cadastral_update_gdb + "\\Condo_Parcel_Polygons":
                arcpy.MakeFeatureLayer_management(cadastral_update_gdb + '\\Parcpoly_FGDB_Dissolved', "Parcpoly_FGDB_Dissolved_Joined_Attributes")
                arcpy.AddJoin_management("Parcpoly_FGDB_Dissolved_Joined_Attributes", "GRPPCLID", cadastral_update_gdb + '\\Parcel_Attributes', "GRPPCLID")
                arcpy.FeatureClassToFeatureClass_conversion("Parcpoly_FGDB_Dissolved_Joined_Attributes", outPath, outFc)


            




            
            
            temp_layer = tempLyr.split('\\')[-1][:-4]
            arcpy.MakeFeatureLayer_management(tempLyr, temp_layer)
            
            arcpy.SelectLayerByAttribute_management(temp_layer,"NEW_SELECTION", whereClause)
            arcpy.CalculateField_management(temp_layer, fieldName, expression, expression_type="PYTHON3", code_block="")
            arcpy.SelectLayerByAttribute_management(temp_layer, selection_type="CLEAR_SELECTION", where_clause="")    
            if dissolveBool == True:
                
                arcpy.Dissolve_management(originFeature, DissolvedLayer, "GRPPCLID", "", "MULTI_PART", "DISSOLVE_LINES")
            else:
                arcpy.DeleteField_management(in_table=DissolvedLayer, drop_field="UNIT")
                arcpy.AddField_management(in_table=DissolvedLayer, field_name="UNIT", field_type="TEXT", field_precision="", field_scale="", field_length="30", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

                arcpy.Append_management(inputs=cadastral_update_gdb+"\\Condo_Parcel_Polygons", target=DissolvedLayer, schema_type="NO_TEST")

                indexes = arcpy.ListIndexes(DissolvedLayer)
                for index in indexes:
                    self.callIndexAndField( DissolvedLayer, index)
        except Exception as e:
            
            Subject = "ERROR: creating merged consolidation file failed ub create_merged_parcpoly2!"
            Msg = ("An error occurred while trying to create parcel polygon feature class on PUB1!")
            Msg += "\n "+ str(e)
            self.emailObj.sendMessage(Subject, Msg)
           
