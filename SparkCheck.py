#!/usr/bin/python
# -*- coding: utf-8 -*- 
from Logger import Log
import ConfigParser
import re, os
from utils import ConfParse


class SparkCheck(object):

	def __init__(self,path,security_file):
		self._path = path
		self._security_file = security_file
 	
 	def check(self):
 		security_conf = ConfigParser.SafeConfigParser(allow_no_value=True)
	 	security_conf.read(self._security_file)

	 	check_conf = ConfParse.ConfParser()
	 	check_conf.read("%s/spark-defaults.conf" % self._path)
	 	check_conf_options = check_conf.get_options()

	 	has_warn = False
	 	sections = security_conf.sections()
	 	for section in sections:
	 		items = security_conf.items(section)
	 		for item in items:
	 			#print section, re.compile("\s+").split(item[0])
	 			key_val = re.compile("\s+").split(item[0])

	 			try:
	 				check_val = check_conf_options[key_val[0]]

	 				if(key_val[1] != '*' and check_val != key_val[1]):
	 					Log.log_warn("Suggest to set option %s = %s" %(key_val[0], key_val[1]))
	 					has_warn = True
	 			except KeyError, e:
	 				has_warn = True
	 				if key_val[1] == "*":
	 					if(key_val[0] == 'spark.authenticate.secret'):
	 						Log.log_warn("Suggest to add option %s if your spark runs on yarn mode"%key_val[0])
	 					else:
	 						Log.log_warn("Suggest to add option %s"%key_val[0])
	 				else:
	 					if(key_val[0] == 'spark.authenticate'):
	 						Log.log_warn("Suggest to add option %s = %s if your spark runs on standalone mode"% (key_val[0], key_val[1]))
	 					else:
	 					    Log.log_warn("Suggest to set option %s = %s"% (key_val[0], key_val[1]))

	 	if has_warn == False:
	 		Log.log_pass("Your configuration is safe!")

def run(check_folder):
	if not os.path.exists(check_folder):
		Log.log_error("The folder doest not exists!")
		sys.exit(0)
	Log.log_info("Start to check the security of spark...")
	test = SparkCheck(check_folder, "spark/security.ini")
	test.check()

if __name__ == '__main__':
	run("./spark")