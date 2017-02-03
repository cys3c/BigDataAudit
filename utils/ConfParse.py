#!/usr/bin/python
# -*- coding:utf-8 -*- 
import os, sys
import re

class ConfParser(object):

	def __init__(self, conf_type=0):
		self._conf_type = 0
		self._kv_map = dict()

	def read(self,file):
		if not os.path.exists(file):
			print "The file does not exists!"
			sys.exit(0)
		if self._conf_type == 0:
			self.read_sp_conf(file)
		else:
			print "developing!"

	def read_sp_conf(self, file):
		fp = open(file)
		for line in fp:
			content = line.strip()
			
			if content == '' or content[0] == '#' or content[0] == ';':
				continue
			k_v = re.compile("\s+").split(content)
			self._kv_map[k_v[0]] = k_v[1]

		fp.close()

	def get_options(self):
		return self._kv_map


if __name__ == '__main__':
	test = ConfParser()
	test.read("../spark/spark-defaults.conf")
	print test.get_options()