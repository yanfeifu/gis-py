'''
Author: your name
Date: 2021-07-27 10:45:47
LastEditTime: 2021-08-03 11:54:42
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /undefinedd:/CodeBackEnd/MapServiceManager/Python/publishService.py
'''
# -*- encoding: utf-8 -*-
import arcpy
import sys


service_name = arcpy.GetParameterAsText(0);
workspace_path = arcpy.GetParameterAsText(1);
mxd_path = arcpy.GetParameterAsText(2);
service_url = arcpy.GetParameterAsText(3);
username = arcpy.GetParameterAsText(4);
password = arcpy.GetParameterAsText(5);
summary = 'summary'
tags = 'tags'

# 用Python解析器跑py时，碰到中文名称的需要加后面的转码 .decode('utf-8').encode('cp936')
# service_name = "service01"
# workspace_path = "D:/CodeBackEnd/dotnetewebapiservice/DigitalBaseWebApi/MxdService/"
# mxd_path = "D:/CodeBackEnd/dotnetewebapiservice/DigitalBaseWebApi/MxdService/service01.mxd"
# service_url = "http://10.190.192.150:6080/arcgis/admin"
# username = "admin"
# password = "admin"
# summary = 'summary'
# tags = 'tags'

# Provide path to connection file
out_folder_path = workspace_path
ags_filename = "connection.ags"
staging_folder_path = workspace_path

arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",  
                                            out_folder_path,  
                                            ags_filename,  
                                            service_url,  
                                            "ARCGIS_SERVER",  
                                            False,  
                                            staging_folder_path,  
                                            username,  
                                            password,  
                                            "SAVE_USERNAME")
# Provide other service details
sddraft = workspace_path + service_name + '.sddraft'
sd = workspace_path + service_name + '.sd'

# Create service definition draft
map_docment = arcpy.mapping.MapDocument(mxd_path);
arcpy.mapping.CreateMapSDDraft(map_docment, sddraft, service_name, 'ARCGIS_SERVER', ags_filename, True, None, summary, tags)

# Analyze the service definition draft
analysis = arcpy.mapping.AnalyzeForSD(sddraft)

# Print errors, warnings, and messages returned from the analysis
print "The following information was returned during analysis of the MXD:"
for key in ('messages', 'warnings', 'errors'):
  print '----' + key.upper() + '---'
  vars = analysis[key]
  for ((message, code), layerlist) in vars.iteritems():
    print '    ', message, ' (CODE %i)' % code
    print '       applies to:',
    for layer in layerlist:
        print layer.name,
    print

# Stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
    # Execute StageService. This creates the service definition.
    arcpy.StageService_server(sddraft, sd)

    # Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
    arcpy.UploadServiceDefinition_server(sd, ags_filename)
    print "Service successfully published"
else: 
    print "Service could not be published because errors were found during analysis."

print arcpy.GetMessages()