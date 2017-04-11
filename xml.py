#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide.QtCore import *

from lxml import etree

def open_xml(fichier):
  """
  Permet l'ouverture d'une fichier xml et le stockage de ses informations dans un dico.
  """
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
    """
    Permet de récupérer le langage d'un fichier xml d'un projet.
    """
    configuration = open_xml(fichier)
    return configuration["language"].lower()

def project_compil(fichier):
    """
    Permet de récupérer la balise compil d'un fichier xml d'un projet.
    """
    configuration = open_xml(fichier)
    return configuration["compil"] if configuration["compil"] != " " else ""

def project_compil_json(fichier):
    """
    Permet de récupérer la balise compil_json d'un fichier xml d'un projet.
    """
    configuration = open_xml(fichier)
    return configuration["compil_json"] if configuration["compil_json"] != " " else ""

def compil_xml(fichier, value):
  """
  Permet d'écrire la valeur de la balise compil dans un fichier xml d'un projet.
  """
    write_xml(fichier,"compil",value)

def compil_json_xml(fichier, value):
  """
  Permet d'écrire la valeur de la balise compil_json dans un fichier xml d'un projet.
  """
    write_xml(fichier,"compil_json",value)

def write_xml(fichier, config, value):
  """
  Permet d'écrire la valeur d'une balise dans un fichier xml.
  """
    tree = etree.parse(fichier)
    root = tree.getroot()
    for child in root.getchildren():
        if child.tag == config:
            mode = root.find(config)
    mode.text = value
    tree.write(fichier)

def create_xml(path):
  """
  Permet de créér un fichier xml avec l'initialisation de ses balises.
  """
    fichier = open(path, "w")
    fichier.write("<project>\n"
                  "     <name></name>\n"
                  "     <creation_date></creation_date>\n"
                  "     <language></language>\n"
                  "     <location></location>\n"
                  "     <number_files></number_files>\n"
                  "     <compil></compil>\n"
                  "     <compil_json></compil_json>\n"
                  "</project>")
    fichier.close()

def add_projects_xml(project_name, project_lang, project_location, date, project_nb_files):
  """
  Permet d'ajouter les différentes balises composant un projet qui est ajouté à la liste des projets.
  """
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
    compil_json = etree.SubElement(project, "compil_json")
    compil_json.text = ""
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
              "     <current_workplace>%s</current_workplace>\n"
              "</configuration>"%(QDir.homePath() + "/workplace/"))
    new.close()
    
try :
    open("projects.xml")
except :
    new = open("projects.xml", "w")
    new.write("<projects>\n"
              "</projects>")
    new.close()