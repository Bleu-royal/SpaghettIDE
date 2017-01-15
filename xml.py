#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

# import xml.etree.ElementTree
# from xml.dom import minidom

# file_xml = '/themes/current_theme.xml'

# def get(file_xml):

#     doc = minidom.parse(file_xml)

#     e = xml.etree.ElementTree.parse(file_xml).getroot()

#     print(doc)
#     print(e)

def open_theme(file_xml):

    tree = etree.parse(file_xml)
    root = tree.getroot()
    mode = root.find('nom')
    return str(mode.text)


    
