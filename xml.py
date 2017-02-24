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
              "     <loading>False</loading>\n"
              "</configuration>")
    new.close()

try :
    open("projets.xml")
    #tree = etree.parse("conf.xml")
except :
    new = open("projets.xml", "w")
    new.write("<projets>\n"
              "</projets>")
    new.close()

def open_xml(fichier):
	configuration = {}
	tree = etree.parse(fichier)
	root = tree.getroot()
	for child in root.getchildren():
		configuration[child.tag] = child.text
	return configuration


def write_xml(fichier,config,value):
	tree = etree.parse(fichier)
	root = tree.getroot()
	for child in root.getchildren():
		if child.tag == config:
			mode = root.find(config)
	mode.text = value
	tree.write(fichier)