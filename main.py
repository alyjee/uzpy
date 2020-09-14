from os import path
import os
import json
from shutil import copyfile
import xml.etree.ElementTree as ET

def replaceAppName(appName, targetFile):
	print("asda")
	allowed_file_types = ('.xml')
	if path.exists(targetFile) and targetFile.lower().endswith(allowed_file_types):
		print("File {0} exists and has .xml file".format(targetFile))
		tree = ET.parse(targetFile)
		# print(tree.findall("string"))
		for ele in tree.findall("string"):
			if ele.attrib["name"] == "app_name":
				print("Old App Name: {0} New App Name: {1}".format(ele.text, appName))
				ele.text = appName
		tree.write(targetFile)

def findAndReplaceInJson(filePath, replaceText):
	allowed_file_types = ('.txt', '.json')
	if path.exists(filePath) and filePath.lower().endswith(allowed_file_types):
		with open(filePath, 'r') as file :
			text = file.read()
			try:
				json_data = json.loads(text)
			except json.decoder.JSONDecodeError:
				return False
		
		text_to_find = json_data["msAppUUID"]

		text = text.replace(text_to_find, replaceText)
		
		# Write the file out again
		with open(filePath, 'w') as file:
		  file.write(text)

def findAndReplaceFile(newFile, oldFile):
	if path.exists(oldFile):
		os.replace(oldFile, newFile)
	else:
		copyfile(newFile, oldFile)


def main():
	source_json_file = "configurations.json"
	allowed_file_types = ('.txt', '.json')
	
	if path.exists(source_json_file) and source_json_file.lower().endswith(allowed_file_types):
		print("File exists and it has .json extension")
		with open(source_json_file, encoding='utf-8-sig') as json_file:
			text = json_file.read()
			try:
				json_data = json.loads(text)
				print("File holds valid JSON data")
			except json.decoder.JSONDecodeError:
				print("Invalid JSON file")
				return False
			
			_newMsAppUuid = json_data["msAppUUID"]
			print("Replacing msAppUuid in following JSON files:")
			print("files/uat-config.json")
			findAndReplaceInJson(json_data["appConfig"]["uat"], _newMsAppUuid)
			
			findAndReplaceFile(json_data["appLogo"], "destination/assets/logo.png")
			replaceAppName(json_data["appName"], "destination/strings.xml")

main()
