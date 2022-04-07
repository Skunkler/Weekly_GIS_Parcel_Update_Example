import email
from site import execsitecustomize
import arcpy, smtplib, string, sys, datetime, time, os #, httplib, urllib, json, getpasss
import subprocess
from arcpy import env
from datetime import datetime, date, timedelta
#from email.mime.text import MIMEText
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText
#from email import Encoders
from startStopServicesClass import StartStopServices
from EmailUtilities import EmailUtil
from GDBUtilities import GDBUtilities
from parcel_update_class import UpdateGDBs






passWord = ""
userName = ""
startStop_SRV03 = StartStopServices(userName, passWord, 6080, "caggissrv03")
startStop_SRV04 = StartStopServices(userName, passWord, 6080, "caggissrv04")
emailUtil = EmailUtil("GIS Manager <gis_data_update_process@someplace.com>", ['Warren.Kunkler@someplace.com'])

gdbUtil = GDBUtilities(emailUtil)
updateGDB = UpdateGDBs(emailUtil)

mesages = []
processOutcome = []

todayList = []
todayDate = date.today()

todayList.append(todayDate)
updateFrequency = ""

ListServ=["Condo_FGDB", "Condopoy_FGDB", "Parcpoly_FGDB", "Parcpoly_Condo", "Parcpoly_Condo_for_Join", "Parcpoly_Condo_Combo", "Parcel_Attributes","Auditor_Book_Page","Condo_Unit_Attributes","Condopoly_FGDB", "Ham_Subdivision_Boundaries","Ham_Parcel_Attributes_Merged"]



#gdbUtil.createGDB(ListServ)
def updateGIS01():
    try:
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_PARCEL_POLY_GIS01, gdbUtil.Parcpoly_Condo_Combo)
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_PARCEL_ATT_GIS01, gdbUtil.HAM_PARCEL_ATT)
        #updateGDB.truncateAppendFGDB(gdbUtil.HAM_BK_GIS01, r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\HCE.ParcelEditing\HCE.Auditor_Book_Page")
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_BK_GIS01, gdbUtil.cgdConnect + '\\HCE.ParcelEditing\\HCE.Auditor_Book_Page')
    except Exception as e:
        print(e)
        emailUtil.sendMessage("Error", str(e))


def updateGIS02():
    try:
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_PARCEL_POLY_GIS02, gdbUtil.Parcpoly_Condo_Combo)
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_PARCEL_ATT_GIS02, gdbUtil.HAM_PARCEL_ATT)
        #updateGDB.truncateAppendFGDB(gdbUtil.HAM_BK_GIS02, r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\HCE.ParcelEditing\HCE.Auditor_Book_Page")
        updateGDB.truncateAppendFGDB(gdbUtil.HAM_BK_GIS02, gdbUtil.cgdConnect + '\\HCE.ParcelEditing\\HCE.Auditor_Book_Page')
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error", str(e))



def updatePUB1():
    try:
        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2opub132.sde\CAGIS.Ham_Parcel_Poly", gdbUtil.Parcpoly_Condo_Combo, True)
        updateGDB.truncateAppendFGDB("C:\workingScratchArea\parcel_update_process_data\pub1_Data.gdb\Ham_Parcel_Poly", gdbUtil.Parcpoly_Condo_Combo)
        
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error", str(e))


def updateCGD1():
    try:
        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.Ham_Parcelfabric_Parcels", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Parcpoly_Condo_Combo", True)
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\CAGIS_HAM_Parcelfabric_Parcels", gdbUtil.Parcpoly_Condo_Combo)

        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.CADASTRA\CAGIS.Ham_Parcel_Poly", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Parcpoly_Condo_Combo", True)
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\CAGIS_HAM_Parcel_Poly", gdbUtil.Parcpoly_Condo_Combo)
    
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error", str(e))


def updateRest():
    try:
        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.Ham_Parcelfabric_Subdivisions", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Ham_Subdivision_Boundaries", True)
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\HAM_Parcelfabric_Subdivisions", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Ham_Subdivision_Boundaries")

        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.Ham_Parcelfabric_Condo_Atts", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Condo_Unit_Attributes", True)
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\Ham_Parcelfabric_Condo_Atts", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Condo_Unit_Attributes")

        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.Ham_Parcelfabric_Condopoly", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Condopoy_FGDB", True )
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\Ham_Parcelfabric_Condopoly", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Condopoy_FGDB")
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error with Rest", str(e))

def create_merged_parcpoly():
    try:
        #updateGDB.create_merged_parcpoly1("C:/ArcMap/Databases/Cadastral_Update.gdb/Parcpoly_Condo_Combo","C:/ArcMap/Databases/Cadastral_Update.gdb","Condo_parcel_polygons", "GRPPCLID like '%CD%' AND PARCELID not like '%CD%'")
        
        
        updateGDB.create_merged_parcpoly1(r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Condo_Combo", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb", "Condo_parcel_polygons", "GRPPCLID like '%CD%' AND PARCELID not like '%CD%'")
        
        

        #updateGDB.create_merged_parcpoly2(r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Condo_Combo", "C:/ArcMap/Databases/Cadastral_Update.gdb","Parcpoly_FGDB_Dissolved", "GRPPCLID IS NULL","GRPPCLID","[PARCELID]", gdbUtil.Parcpoly_Condo_Combo, True, True)
        
        
        
        updateGDB.create_merged_parcpoly2(r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Condo_Combo",  r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb","Parcpoly_FGDB_Dissolved", "GRPPCLID IS NULL","GRPPCLID","!PARCELID!", gdbUtil.Parcpoly_Condo_Combo, True, True)
        
        
        
        #updateGDB.create_merged_parcpoly2(r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation", "C:/ArcMap/Databases/Cadastral_Update.gdb", "Parcpoly_Merged_Consolidation","PARCELID IS NULL", "PARCELID", "[GRPPCLID]", "C:\ArcMap\Databases\Cadastral_Update.gdb\Condo_Parcel_Polygons")
        #uncomment below
        updateGDB.create_merged_parcpoly2(r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb", "Parcpoly_Merged_Consolidation","PARCELID IS NULL", "PARCELID", "!GRPPCLID!", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Condo_Parcel_Polygons", False, True)



        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2ocgd132.sde\CAGIS.Ham_Parcelfabric_Merged_Parcel",r"C:\ArcMap\Databases\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation", True )
        
        #uncomment
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\cgd132_data.gdb\CAGIS_Ham_Parcelfabric_Merged_Parcel", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation")


        #updateGDB.truncateAppendFGDB(r"C:\batch\DatabaseConnections\cagis@2opub132.sde\CAGIS.Ham_Parcelfabric_Merged_Parcel", r"C:\ArcMap\Databases\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation", True)
        
        #uncomment
        updateGDB.truncateAppendFGDB(r"C:\workingScratchArea\parcel_update_process_data\pub1_Data.gdb\CAGIS_Ham_Parcelfabric_Merged_Parcel", r"C:\workingScratchArea\ParcelUpdateClassTests\Mocha\Cadastral_Update.gdb\Parcpoly_Merged_Consolidation")
       
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error with Create Merged ParcPoly", str(e))
def validateData(updateFrequency):
    try:
        gdbUtil.validateData(updateFrequency, [])
    except Exception as e:
        print(str(e))
        emailUtil.sendMessage("Error with validateData", e)

def restartServices():
    try:
        Services = {"HCE": "Cadastral", "Hamilton":"HCE_Parcels_With_Auditor_Data", "GIS_Framework": "AA_Apps"}
        for key in Services.keys():
            startStop_SRV03.restartService(key, Services[key])
            startStop_SRV04.restartService(key, Services[key])
            
    except Exception as e:
        Message = str(e)
        emailUtil.sendMessage("Failure to Start or Stop Services",str(e))


try:
    gdbUtil.createGDB(ListServ)
    updateGIS01()
    updateGIS02()

    updatePUB1()
    updateCGD1()
    create_merged_parcpoly()
    updateRest()
    #validateData('CagisOnline')
    #validateData('GoCAGIS')
    #restartServices()
    print("process complete")
    emailUtil.sendMessage("Parcel Update process success!", "Parcel update process from the Parcel Update Class ran successfully!")
except Exception as e:
    print(e)
    emailUtil.sendMessage("Parcel Update Process Failure!", "The parcel update process failed\n{0}".format(str(e)))
