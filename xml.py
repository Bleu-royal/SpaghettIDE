#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

try :
    open("conf.xml")
    #tree = etree.parse("conf.xml")
except :
    new = open("conf.xml", "w")
    new.write("<configuration>\n"
              "     <theme>basic</theme>\n"
              "     <assistance_vocale>False</assistance_vocale>\n"
              "</configuration>")
    new.close()

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