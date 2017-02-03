#!/usr/bin/python
# -*- coding: utf-8 -*- 
import json, sys, os
from Logger import Log
import xml.etree.ElementTree as ET

class HadoopCheck(object):
	
	def __init__(self, path, security_file):
		self._path = path
		self._security_file = security_file

	"""
	load json
	"""
	def load_json(self):
		try:
			fp = open(self._security_file)
			content = fp.read()
			security_conf_json = json.loads(content)
		except Exception, e:
			Log.log_error(str(e))
			sys.exit(0)
		finally:
			if fp is not None:
				fp.close()
		return security_conf_json
	

	def check(self):
		security_conf_json = self.load_json()
		for key, val in security_conf_json.items():
			Log.log_info("Begining to check security: %s" % key)
			has_threat = False
			for file, attrs in val.items():
				Log.log_info(">> Check file: %s.xml"%file)
				setting = self.parse_xml("%s/%s.xml"%(self._path, file))
				for prop in attrs:
					reason = prop['reason']
					del prop['reason']
					for key, val in prop.items():
						if key not in setting.keys():
							Log.log_warn("%s Set: %s=%s"%(reason, key, val))
							has_threat = True
						else:
							if val != "*" and val != setting[key]:
								Log.log_warn("Suggest to set %s=%s"%(key, val))
								has_threat = True
			if has_threat == False:
				Log.log_pass("Your %s setting is safe!" % key)


	def parse_xml(self, file):
		res = dict()
		try:
			root = ET.parse(file).getroot()
			properties = root.findall(".//property")
			for item in properties:
				name = item.find(".//name").text
				value = item.find(".//value").text
				res[name] = value
		except Exception, e:
			Log.log_error(str(e))
			sys.exit(0)
		return res

def run(confFolder):
	if not os.path.exists(confFolder):
		Log.log_error("The folder doest not exists!")
		sys.exit(0)
	test = HadoopCheck(confFolder, "hadoop/hadoop.json")
	test.check()
	
if __name__ == "__main__":
	test = HadoopCheck()("hadoop", "hadoop.json")
	test.check()
	
	