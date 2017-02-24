#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

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

try :
    configuration = open_xml("conf.xml")
except :
    new = open("conf.xml", "w")
    new.write("<configuration>\n"
              "     <theme>basic</theme>\n"
              "     <assistance_vocale>False</assistance_vocale>\n"
              "     <loading>False</loading>\n"
              "     <numerote_lines>True</numerote_lines>\n"
              "     <language>Fran&#231;ais</language>\n"
              "</configuration>")
    new.close()
    
try :
    open("projets.xml")
except :
    new = open("projets.xml", "w")
    new.write("<projets>\n"
              "</projets>")
    new.close()