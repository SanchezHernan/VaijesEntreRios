
class ciudad():
    def __init__(self, nombre, cp, lat = None, long = None, idCiudad = None):
        self.nombre = nombre
        self.cp = cp
        self.idCiudad = idCiudad
        self.lat = lat
        self.long = long
        
    def getNombre(self):
        return self.nombre
    
    def setNombre(self, nombre):
        self.nombre = nombre
    
    def getCP(self):
        return self.cp
    
    def setCP(self, cp):
        self.cp = cp
    
    def setIdCiudad(self, idCiudad):
        self.idCiudad = idCiudad
        
    def getIdCiudad(self):
        return self.idCiudad
        
        
class viaje():
    def __init__(self, origen, destino, importe, distancia):
        self.origen = origen
        self.destino = destino
        self.importe = importe
        self.distancia = distancia
        self.idViaje = None
        
    def getOrigen(self):
        return self.origen
    
    def setOrigen(self, origen):
        self.origen = origen
        
    def getDestino(self):
        return self.destino
    
    def setDestino(self, ciudad):
        self.ciudad = ciudad
    
    def getImporte(self):
        return self.importe
    
    def setImporte(self, importe):
        self.importe = importe
        
    def getDistancia(self):
        return self.distancia
    
    def setDistancia(self, distancia):
        self.distancia = distancia
        
    def getIdViaje(self):
        return self.idViaje

    def setIdViaje(self, idViaje):
        self.idViaje = idViaje
        

class nodoVertice():
    def __init__(self):
        self.ciud = None
        self.cab = None
        self.sig = None
    
    def insertar(self, nodo):
        if((self.cab==None) or (nodo.info.getDestino().getNombre() < self.cab.info.getDestino().getNombre())):
            nodo.sig = self.cab
            self.cab = nodo
        else:
            ant = self.cab
            act = self.cab.sig
            while (act != None and (act.info.getDestino().getNombre() < nodo.info.getDestino().getNombre())):
                ant=act
                act=act.sig
            nodo.sig=act
            ant.sig=nodo
        
    def buscar(self, busk):
        act = self.cab
        while ((act!=None) and (act.info.getDestino().getNombre() != busk)):
            act=act.sig
        return act
    
    
class nodoArista():
    def __init__(self):
        self.info = None
        self.sig = None
    
    
class grafo():
    def __init__(self):
        self.cab = None
        
    def insertar(self, nodo):
        if ((self.cab == None) or (nodo.ciud.getNombre() < self.cab.ciud.getNombre())):
            nodo.sig=self.cab
            self.cab=nodo
        else:
            ant=self.cab
            act=self.cab.sig
            while (act != None) and (act.ciud.getNombre() < nodo.ciud.getNombre()):
                ant=act
                act=act.sig
            nodo.sig=act
            ant.sig=nodo
              
    def altaVertice(self, ciudad):
        pos=self.buscar(ciudad.getNombre())
        if pos==None:
            nodo=nodoVertice()
            nodo.cab=None
            nodo.ciud=ciudad
            self.insertar(nodo)
            return True
        else:
            return False
            
    def generarArco(self, viaje):        
        pos = self.buscar(viaje.getOrigen().getNombre())
        if (pos != None):
            pos2 = self.buscar(viaje.getDestino().getNombre())
            if (pos2 != None):
                i = pos.buscar(viaje.getDestino().getNombre())
                if i == None:
                    nodo=nodoArista()
                    nodo.info=viaje
                    pos.insertar(nodo)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def generarArco2(self, viaje):        
        pos = self.buscar(viaje.getOrigen().getNombre())
        i = pos.buscar(viaje.getDestino().getNombre())
        if i == None:
            nodo=nodoArista()
            nodo.info = viaje
            pos.insertar(nodo)
            return True
        else:
            return False
        
    def eliminarArista(self, origen, destino):        
        pos = self.buscar(origen)
        o=pos
        if pos.cab.info.destino.nombre == destino:
            pos.cab = pos.cab.sig
        else:
            ant=pos.cab
            act=pos.cab.sig
            while act.info.destino.nombre != destino:
                ant=act
                act=act.sig
            ant.sig = act.sig
    
    def eliminarVertice(self, vertice):
        res = None
        viajes = self.tomarCam()
        for v in viajes:
            if v.destino.getNombre() == vertice or v.origen.getNombre() == vertice:
                return res
        if self.cab.ciud.nombre == vertice:
            res = self.cab.ciud
            self.cab = self.cab.sig
            return res
        else:
            ant = self.cab
            act = self.cab.sig
            while act.ciud.nombre != vertice:
                ant=act
                act=act.sig
            if act!=None:
                res=act.ciud
                ant.sig = act.sig
                return res
            else:
                return res
            
    def buscar(self, busk):
        act = self.cab
        while ((act!=None) and (act.ciud.getNombre() != busk)):
            act=act.sig
        return act
    
    def buscarArista(self, origen, destino):
        o=self.buscar(origen)
        v=o.buscar(destino)
        return v
        
                    
    def listarGrafo(self):
        if (self.cab!= None): 
            act=self.cab
            while act != None:                
                print("Ciudad: "+act.ciud.getNombre() + " ")
                if (act.cab!=None):
                    print("Puede viajar a: ")
                    aux=act.cab
                    while aux != None:
                        print(aux.info.getDestino().getNombre() + ", distancia: " + str(aux.info.getDistancia()))
                        aux=aux.sig
                    print()
                act=act.sig 
        else: print("grafo vacio")
    
    def tomarCiud(self):
        lista_Ciud =[]
        act=self.cab
        while(act!=None):
            lista_Ciud.append(act.ciud)
            act = act.sig
        return lista_Ciud

    def tomarCam(self):
        if self.cab != None:    
            caminos=[]
            v=self.cab
            while v!=None:
                if v.cab!=None:
                    cam=v.cab
                    while cam != None:
                        caminos.append(cam.info)
                        cam=cam.sig
                v=v.sig
            return caminos
        else:
            return None
            
    def tomarAristas(self):
        aristas = []
        vert = self.cab
        while vert != None:
            v = vert.cab
            while v != None:
                aristas.append(v.info)
                v=v.sig
            vert=vert.sig
        return aristas
            
                        
    def transformar(self):
        graph = {}
        act = self.cab
        while act != None:
            if (act.cab != None):
                aux=act.cab
                dic=[]
                while aux != None:
                    dic.append(aux.info.destino.nombre)
                    aux=aux.sig
                graph[act.ciud.nombre] = set(dic)
            else:
                graph[act.ciud.nombre] = set({})
            act=act.sig
        return graph
                    
        
def todosLosCaminos(grafo, origen, destino):
        stack = [[origen]]
        while stack:
            path = stack.pop()
            node = path[-1]
            for next in grafo[node] - set(path):
                if next == destino:
                    yield path + [next]
                else:
                    stack.append(path + [next])  
        
        
    
'''
g=grafo()
rdt = ciudad('Rosario del Tala', 3174)
cdu = ciudad('Concepcion del Uruguay', 3260)
ny = ciudad('Nogoya', 3150)
bs = ciudad('Basavilbaso', 3170)
mc = ciudad('Macia', 3177)
g.altaVertice(rdt)
g.altaVertice(cdu)
g.altaVertice(ny)
g.altaVertice(bs)
g.altaVertice(mc)

g.generarArco(viaje(rdt, bs, 80, 50))
g.generarArco(viaje(rdt, cdu, 130, 90))
g.generarArco(viaje(mc, ny, 160, 110))
g.generarArco(viaje(ny, cdu, 84, 99))
g.generarArco(viaje(mc, bs, 99, 20))
g.generarArco(viaje(bs, rdt, 77, 98))
g.generarArco(viaje(bs, ny, 55, 55))
g.generarArco(viaje(cdu, rdt, 88, 88))
g.listarGrafo()






grapho = g.transformar()
generator = todosLosCaminos(grapho, 'Basavilbaso', 'Concepcion del Uruguay')
print(generator)
for j in generator:
    print('Camino: ')
    for i in j:
        print(str(i) + ', ')
'''

