#!/usr/bin/python
# -*- coding:utf-8 -*-

class Log(object):

	WARRING_COLOR = '\033[1;37m'  # yellow
	ERROR_COLOR   = '\033[1;31m'  # red
	INFO_COLOR    = '\033[1;34m'  # blue
	PASS_COLOR    = '\033[1;32m'  # green
	END_COLOR = '\033[0m'

	@staticmethod
	def log_error(msg):
		print "[Error]: %s%s%s"%(Log.ERROR_COLOR, msg, Log.END_COLOR)
	
	@staticmethod
	def log_warn(msg):
		print "[Warning]: %s%s%s"%(Log.WARRING_COLOR, msg, Log.END_COLOR)

	@staticmethod
	def log_info(msg):
		print "[Info]: %s%s%s"%(Log.INFO_COLOR, msg, Log.END_COLOR)

	@staticmethod
	def log_pass(msg):
		print "[Pass]: %s%s%s"%(Log.PASS_COLOR, msg, Log.END_COLOR)

if __name__ == '__main__':
	Log.log_pass("msg")