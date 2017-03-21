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

# def open_projects_xml(fichier,project_name):
#     tree = etree.parse(fichier)
#     for project in tree.xpath("/projects/project/name"):
#         if name.text == project_name:
#             name.getparent().remove(name)

    #tree.findtext(path)

def project_language(fichier):
    configuration = open_xml(fichier)
    return configuration[language]

def compil_xml(fichier,value):
    write_xml(fichier,"compil",value)

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
                  "     <compil></compil>\n"
                  "</project>")
    fichier.close()

def add_projects_xml(project_name,project_lang,project_location,date,project_nb_files):
    tree = etree.parse("projects.xml")
    projects=tree.getroot()
    project = etree.SubElement(projects, "project")
    name = etree.SubElement(project, "name")
    name.text = project_name
    language = etree.SubElement(project, "language")
    language.text = project_lang
    location = etree.SubElement(project, "location")
    location.text = project_location
    creation_date = etree.SubElement(project, "creation_date")
    creation_date.text = date
    nb_files = etree.SubElement(project, "number_files")
    nb_files.text = project_nb_files
    compil = etree.SubElement(project, "compil")
    compil.text = ""
    tree.write('projects.xml', pretty_print=True)

try :
    configuration = open_xml("conf.xml")
except :
    new = open("conf.xml", "w")
    new.write("<configuration>\n"
              "     <theme>basic</theme>\n"
              "     <assistance_vocale>False</assistance_vocale>\n"
              "     <loading>False</loading>\n"
              "     <numerote_lines>True</numerote_lines>\n"
              "     <language>en</language>\n"
              "</configuration>")
    new.close()
    
try :
    open("projects.xml")
except :
    new = open("projects.xml", "w")
    new.write("<projects>\n"
              "</projects>")
    new.close()