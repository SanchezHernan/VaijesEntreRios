# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:05:33 2018

@author: Hornyt0x
"""

# -*- coding: utf-8 -*-

import shelve

class regArchivo():
   def __init__(self):
       self._info = None
       self._activo = True
   
   def setInfo(self, info):
       self._info = info
      
   def getInfo(self):
       return self._info
   
   def eliminado(self):
       self._activo = False
      
   def recuperado(self):
       self._activo = True
      
   def activo(self):
       return self._activo

def abrir(ruta):
    return shelve.open(ruta)

def cerrar(archivo):
    archivo.close()

def guardar(archivo, reg):
    archivo[str(len(archivo))] = reg

def modificar(archivo, reg, pos):
    try:
        archivo[str(pos)] = reg
        return True
    except:
        return False

def leer(archivo, pos):
    try:
        return archivo[str(pos)]
    except:
        return None