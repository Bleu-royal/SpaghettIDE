#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

def open_xml():
	configuration = {}
	tree = etree.parse("conf.xml")
	root = tree.getroot()
	for child in root.getchildren():
		configuration[child.tag] = child.text
	return configuration


def write_xml(config, value):
	tree = etree.parse("conf.xml")
	root = tree.getroot()
	for child in root.getchildren():
		if child.tag == config:
			mode = root.find(config)
	mode.text = value
	tree.write("conf.xml")