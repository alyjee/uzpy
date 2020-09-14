from os import path
import os
import json
from shutil import copyfile

def findAndReplaceText(filePath, replaceText):
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
			findAndReplaceText(json_data["appConfig"]["uat"], _newMsAppUuid)
			findAndReplaceFile(json_data["appLogo"], "destination/assets/logo.png")

main()