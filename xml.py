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

def create_xml(path):
	fichier = open(path, "w")
	fichier.write("<project>\n"
	              "     <name></name>\n"
	              "     <creation_date></creation_date>\n"
	              "     <language></language>\n"
	              "     <location></location>\n"
	              "     <number_files></number_files>\n"
	              "</project>")
	fichier.close()

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
    new = open("projects.xml", "w")
    new.write("<projets>\n"
              "</projects>")
    new.close()