# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 19:19:03 2018

@author: Hornyt0x
"""

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
#import Browser
from PyQt4 import uic
from Grafo import *
import Geocoder as gc
import Hervaisen

from Archivo import *
import os
rutaVert = os.path.realpath('Archivos/Vertices.dat')
rutaArist = os.path.realpath('Archivos/Aristas.dat')


class VentanaVert(QtGui.QDialog):
    def __init__(self, gra):
        QtGui.QDialog.__init__(self)
        uic.loadUi("Interfases/VentanaVert.ui", self)
        self.btnAgCiud.clicked.connect(lambda: self.agregarCiudad(gra))
        self.btnSalir.clicked.connect(self.cerrar)
        
        
    def validar(self):
        return (len(self.leCiudad.text())>0) and (len(self.leCp.text())>0)
        
    def agregarCiudad(self, gra):
        
        if self.validar():
            geopos = gc.geocoder(self.leCiudad.text()+ " entre rios")
            city = ciudad(self.leCiudad.text(), self.leCp.text(), geopos['lat'], geopos['lng'])
            if (gra.altaVertice(city)):
                self.lblResult.setText('Ciudad cargada con exito')
            else:
                self.lblResult.setText('La ciudad no se ha podido cargar')
            self.leCiudad.setText('')
            self.leCp.setText('')
    
    def cerrar(self):
        self.close()
        
                

class VentanaArist(QtGui.QDialog):
    def __init__(self, gra):
        QtGui.QDialog.__init__(self)
        uic.loadUi("Interfases/ventanaArist.ui", self)
        self.distanciaActual = 0
        self.grafo = None
        self.modo = 0
        
        self.cargarComboBox(self.cbOrigen, gra)  
        self.cargarComboBox(self.cbDestino, gra)
        self.cargarListWidget(gra)
        self.btnCargViaje.clicked.connect(lambda: self.agregarViaje(gra))      
        self.cbOrigen.currentIndexChanged.connect(lambda: self.calcularDistancia(gra))
        self.cbDestino.currentIndexChanged.connect(lambda: self.calcularDistancia(gra))
        self.btnEliminar.clicked.connect(lambda: self.eliminar(gra))
        self.btnModo.clicked.connect(lambda: self.cambiarModo(gra))        
        self.btnSalir.clicked.connect(self.cerrar)
        
    def validar(self):
        return (len(self.leImporte.text()) > 0)
        
    def cargarComboBox(self, comboBox, gra): 
        ciudades = gra.tomarCiud()  
        for c in ciudades:
            comboBox.addItem(c.getNombre())  
            
    def mostrarDistanciaEstimada(self):
        self.lblDistancia.setText("Distancia estimada: %.2fkm" % (self.distanciaActual))
    
    def agregarViaje(self, gra):
        if self.validar():
            origen = gra.buscar(self.cbOrigen.currentText())
            destino = gra.buscar(self.cbDestino.currentText())
            if origen.ciud.getNombre() != destino.ciud.getNombre():
                importe = self.leImporte.text()
                v = viaje(origen.ciud, destino.ciud, importe, self.lblDistancia.text())
                if gra.generarArco(v):
                    self.lblSucces.setText('Viaje cargado con exito')
                    if self.modo == 0:
                        item = (origen.ciud.getNombre() + ' a ' + destino.ciud.getNombre() + ', Importe: ' + str(importe))
                        self.listWidget.addItem(item)
                else:
                    self.lblSucces.setText('El viaje ya existe')
            else:
                self.lblSucces.setText('Las ciudades destino y origen son las mismas')
        else:
            self.lblSucces.setText('Informacion incorrecta')
        self.leImporte.setText('')
           
    def calcularDistancia(self, gra):
        if self.modo == 1:
            self.listWidget.clear()
        origen = self.cbOrigen.itemText(self.cbOrigen.currentIndex())
        destino = self.cbDestino.itemText(self.cbDestino.currentIndex())
        nodo = gra.buscar(origen)
        nodo2 = gra.buscar(destino)
        if nodo2 != None and nodo != None:
            self.distanciaActual = Hervaisen.geo_distance(
                nodo.ciud.long,
                nodo.ciud.lat,
                nodo2.ciud.long,
                nodo2.ciud.lat)
            self.mostrarDistanciaEstimada()
            if self.modo == 1:
                self.mostrarViajesSegun()
    
    def cargarListWidget(self, gra):
        if self.modo == 0:
            viajes = gra.tomarAristas()
            for v in viajes:    
                item = (v.getOrigen().getNombre() + ' a ' + v.getDestino().getNombre() + ', Importe: ' + str(v.getImporte()))
                self.listWidget.addItem(item)
        else:  
            self.grafo = gra.transformar()
            self.mostrarViajesSegun()
    
    def eliminar(self, gra):
        reply=QtGui.QMessageBox.question(self, 'Advertencia',
            "Seguro que desea eliminar este viaje?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QtGui.QMessageBox.Yes:
            ciudades = str(self.listWidget.currentItem().text())
            self.listWidget.takeItem(self.listWidget.currentRow())
            pos = ciudades.find(" a ")
            origen=ciudades[:pos]
            pos2=ciudades.find(", Importe")
            pos+=3
            destino=ciudades[pos:pos2]
            v=gra.buscarArista(origen, destino)
            aristas=abrir(rutaArist)
            reg=regArchivo()
            reg.setInfo(v.info)
            reg.eliminado()
            modificar(aristas, reg, str(v.info.getIdViaje()))
            cerrar(aristas)
            gra.eliminarArista(origen, destino)
            
            
    def mostrarViajesSegun(self):
        origen = self.cbOrigen.itemText(self.cbOrigen.currentIndex())
        destino = self.cbDestino.itemText(self.cbDestino.currentIndex())
        if destino != origen:
            item = []
            separador = ' | '      
            generator = todosLosCaminos(self.grafo, origen, destino)
            for j in generator:
                for i in j:
                    item.append(i)
                self.listWidget.addItem(separador.join(item))
                item.clear()
    
    def cambiarModo(self, gra):
        if self.modo == 1:
            self.modo = 0
            self.btnModo.setText('Origen - Destino')
        else:
            self.modo = 1
            self.btnModo.setText('Todos los viajes')
        self.listWidget.clear()
        self.cargarListWidget(gra)
        

                
    def transformarGrafo(self, gra):
        self.grafo = transformar(gra)
        
    def cerrar(self):
        self.close()
        
        
class MenuPrinc(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("Interfases/Menu.ui", self)
        self.graph = grafo()
        self.ciudadesEliminadas = []
        self.viajesEliminados = []
        
        self.cargarGrafo()
        self.ventanaV = VentanaVert(self.graph)
        self.ventanaA = VentanaArist(self.graph)
        self.cargarListView()
        
        self.btnVertice.clicked.connect(self.abrirVentanaVert)
        self.btnArista.clicked.connect(self.abrirVentanaArist)
        self.btnActualizar.clicked.connect(self.actualizar)
        self.cargarMapa()
        #self.statusBar().showMessage('cargando')
        
    def abrirVentanaVert(self):   
        self.ventanaV.exec_()    
    
    def abrirVentanaArist(self):
        self.ventanaA.cbOrigen.clear()
        self.ventanaA.cbDestino.clear()
        self.ventanaA.cargarComboBox(self.ventanaA.cbOrigen, self.graph)
        self.ventanaA.cargarComboBox(self.ventanaA.cbDestino, self.graph)
        self.ventanaA.exec_()
        
    def cargarListView(self): 
        self.listView.clear()
        ciudades = self.graph.tomarCiud()
        for ciud in ciudades:
            self.listView.addItem(ciud.getNombre())         
        
    def cargarGrafo(self):
        vertices = abrir(rutaVert)
        aristas = abrir(rutaArist)
        vk = list(vertices.keys())
        for i in vk:
            reg = leer(vertices,i)
            if reg.activo():
                 self.graph.altaVertice(reg.getInfo())
        ak = list(aristas.keys())
        for i in ak:
            reg = leer(aristas,i)
            if reg.activo():
                self.graph.generarArco(reg.getInfo())
        cerrar(vertices)
        cerrar(aristas)
    
    def actualizar(self):
        self.cargarListView()
        self.cargarMapa()
        
    def closeEvent(self, event):
        regArch = regArchivo()
        vertices = abrir(rutaVert)
        aristas = abrir(rutaArist)
        ciudades = self.graph.tomarCiud()
        viajes = self.graph.tomarCam()
        if ciudades != None:  
            for c in ciudades:
                if c.getIdCiudad() == None:
                    c.setIdCiudad(len(vertices))
                    regArch.setInfo(c)
                    guardar(vertices, regArch)
        if viajes != None:
            for v in viajes:
                if v.getIdViaje() == None:
                    v.setIdViaje(len(aristas))
                    regArch.setInfo(v)
                    guardar(aristas, regArch)
        cerrar(vertices)
        cerrar(aristas)
                 
    def cargarMapa(self):
        center ="center=paso de la laguna entre rios"
        zoom = "&zoom=7.50"
        size = "&size=600x700"
        #lista_Ciud = ["concepcion del uruguay", "villaguay","colon,entre rios","parana,entre rios"]
        ciudades = self.graph.tomarCiud()
        cities = []
        for c in ciudades:
            cities.append(c.getNombre() + ' Entre Rios')
        if ciudades != None:
            marcas = "|"
            marcas = marcas.join(cities)
            markers = "&markers=" + "color:red|"+ marcas
            maptype="&maptype=roadmap"
            #path = "&path=concepcion del uruguay|villaguay,colon|parana entre rios"
            key = "&key=AIzaSyCXQfkDrWHjpnG-0DvUcgtFkGdsKm2esG0"
            self.webView.load(QtCore.QUrl("https://maps.googleapis.com/maps/api/staticmap?"+center+zoom+size+maptype+markers+key))

  

        
        
        
if(__name__=="__main__"):

    app = QtGui.QApplication(sys.argv)
    principal = MenuPrinc()
    principal.show()
    app.exec_()
    print('')
    
    '''
    vertices = abrir(rutaArist)
    for i in range(0, len(vertices)):
        reg = leer(vertices, i)
        print(reg.getInfo().getOrigen().getNombre())
    cerrar(vertices)
    '''
    #g.listarGrafo()
    #principal.grafo.listarGrafo()
    #mostrar el precio de las combinaciones