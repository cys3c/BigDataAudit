#!/usr/bin/python
# -*- coding: utf-8 -*- 
import argparse
import os
from Logger import Log
import sys

def CheckHadoop(args):
	path = args.confFolder
	if not os.path.exists(path):
	    Log.log_error("'%s' is not a dir!" % path)
	    sys.exit(0)
	abs_path = os.path.abspath(path)
	# print abs_path
	import HadoopCheck
	HadoopCheck.run(abs_path)

def CheckSpark(args):
	path = args.confFolder
	if not os.path.exists(path):
	    Log.log_error("'%s' is not a dir!" % path)
	    sys.exit(0)
	abs_path = os.path.abspath(path)
	import SparkCheck
	SparkCheck.run(abs_path)

def main():
	parser = argparse.ArgumentParser(description="This is a tool for detectiong the security problem of spark and hadoop!")

	subparsers = parser.add_subparsers(help='commands')

	# A ConfigCheck command
	conf_check_parser = subparsers.add_parser('hadoop', help='check security of hadoop')
	conf_check_parser.add_argument('confFolder', action='store', help='the dir of hadoop configuration files')
	conf_check_parser.set_defaults(func=CheckHadoop)
	# A SettingCheck command
	setting_check_parser = subparsers.add_parser('spark', help='check security of spark')
	setting_check_parser.add_argument('confFolder', action='store', help='the dir of spark configuration files')
	setting_check_parser.set_defaults(func=CheckSpark)

	args = parser.parse_args()
	args.func(args)

if __name__ == '__main__':
	main()