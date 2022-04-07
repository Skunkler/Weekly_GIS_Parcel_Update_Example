import arcpy
from arcpy import env


class ParcPolyHelper:

	def __init__(self, sourceRootObj):
		self.sourceRootObj = sourceRootObj
	

	def __createParcAttributes(self):
		try:

			arcpy.TableToTable_conversion(self.sourceRootObj["ParcelAttributeViews2"], r"C:\ArcMap\Databases\Cadastral_Update.gdb", "PARCEL_ATTRIBUTES")
		except Exception as e:
			print(e)
			ouch = arcpy.GetMessages(2)
			return (e, Ouch)

	def __CalculateFieldParcpoly_Condo(self):

		try:
			tmp_layer = arcpy.mapping.Layer(self.sourceRootObj["ParcpolyCondoLyr"])
			arcpy.selectLayerByAttributes_management(tmp_layer, "NEW_SELECTION", "NAME like '%CD%' AND PARCELID IS NOT NULL")
			arcpy.CalculateField_management(tmp_layer, "NAME", expression = "!PARCELID!", "Python_9.3")
			arcpy.SelectLayerByAttribute_management(tmp_layer, "CLEAR_SELECTION")
		except Exception as e:
			print(e)
			ouch = arcpy.GetMessages(2)
			return (e, ouch)


	def __ParcFabricName(self):
		try:
			arcpy.CalculateField_management(self.sourceRootObj[ParcpolyCondoCombo], "PARCELID", "!NAME!", "Python_9.3")
		except Exception as e:
			print(e)
			ouch = arcpy.GetMessages(2)
			return (e, ouch)

	def __featureClassFeatureClass(self, key, outputPath, outputTarget, whereclause = None):
		try:
			if whereclause == None:
				arcpy.FeatureClassToFeatureClass_conversion(key, self.sourceRootObj[key], outputTarget)
			else:
				arcpy.FeatureClassToFeatureClass_conversion(key, self.sourceRootObj[key], outputTarget, whereclause)
		except Exception as e:
			print(e)
			ouch = arcpy.GetMessages(2)
			return (e, ouch)

	def mainCaller(self):

		processList = []
		self.__createParcAttributes()
		for key in self.sourceRootObj.keys():
			if key in ProcessList:
				outputLoc = self.sourceRootObj[key].split("/")[-1]
				outputPath = self.sourceRootObj[key].replace(outputLoc,"")
				if key == r"C:\ArcMap\CagisGISProjects\Parcel_Update\Auditor Book and Page (ParcelFabric).lyr":
				

					self.__featureClassFeatureClass(key, outputPath, outputLoc, "SYSTEMENDDATE IS NULL")
				elif key == r"C:\ArcMap\CagisGISProjects\Parcel_Update\Parcpoly_Condo_Combo_All_Selected.lyr":
					arcpy.FeatureToPoint_management(key, self.sourceRootObj[key], "INSIDE")
				else:
					self.__featureClassFeatureClass(key, outputPath, outputLoc)


class DataValidation:

	def __init__(self):
		pass
	
	def validateData(self, updateFreq):
		FGDB = "Cadastral.gdb"
		VALIDATEDATA = "SUCCESS"
		if updateFreq == "CagisOnline":
			validateFGDB = os.path.join(r"\\caggiswa01\GISFileDS\arcgisserver\Data", FGDB)
		else:
			validateData = os.path.join(r"\\CA0138EGIS02\c$\arcgisserver\Data",FGDB)
		
		env.workspace = validateData

		fcDict = {"HAM_PARCEL_POLY": (418000, 425000), 
			"HAM_PARCEL_POLY_MERGED_OWNSHP": (350000, 360000),
		    "CONDOMINIUM_UNITS": (21000, 23000), 
			"Condominium_Common_Areas": (1900, 2200),
			"Auditor_Book_Page": (2600, 2800),
			"Condo_polygons": (20000, 25000),
			"Ham_Parcel_Attributes_Merged": (410000, 435500),
			"Ham_Subdivision_Boundaries": (9500, 12500)}

		
		for key in fcDict.keys():
			result = int(arcpy.GetCount_management(key).getOutput(0))
			if result > fcDict[key][0] and result < fcDict[key][1]:
				msg=("count("+key+") = "+str(result))
				print(msg)
				messages.append(msg)
			else:
				msg = "FAILED - count(" + key + ") = "+str(result)
				print(msg)
				messages.append(msg)
				VALIDATEDATA = "FAILURE"
				messages.append("---------------------------------------------")
		if VALIDATEDATA == "FAILURE":
			processOutcome.append('Failure - ValidateFGDB Function')
			print('Validation Failed! \n')
			messages.append('\n******At least one or more feature(s) failed on data validation!!!****** \r\n')
			messages.append('One or more data failed data validation - ValidateFGDB Function\r\n')
		else:
			print('Data Validation Successfull! \n')
			messages.append('\n Validation Successfull! \r\n')
