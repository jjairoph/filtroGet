# -*- coding: utf-8 -*-
import os  # Mostrar la ruta al archivo
import re  # Expresiones regulares
import urllib
import urllib2

'#https://docs.python.org/2/howto/urllib2.html'
'#HOWTO Fetch Internet Resources Using urllib2'

class SeparaInfoFarmalisto:
    # como consultar farmalisto
    # http://www.farmalisto.com.co/buscar?search_query=loratadina&n=5000

    '#RegEx para identificar inicio de la lista de resultados medicamentos consultados'
    k_inicio_lista = '<ul class="product_grid" id="product_list">'

    '#Patron para separar cada item'
    '#<li class="grid_4 ajax_block_product first_item item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product alternate_item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product alternate_item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product last_item alternate_item clearfix omega alpha">'

    k_item = '<li class="grid_4 ajax_block_product [a-z_\s]{13,50}omega alpha">'

    '#DEtalle de las columnas de cada fila'
    k_product_img_link = '<a class="product_img_link"\shref="[a-z:/.0-9-]{1,180}"'
    k_namepro ='namepro="[A-Z\s\/0-9a-z-óáéíú]{1,170}"'
    k_alt = 'alt="[[A-Z\s0-9a-z]{1,150}"\s\/>'
    k_name_product_search = '<div class="name_product_search"><a href="[a-z:/.0-9-]{1,180}"'
    k_pricepro = '\spricepro="[0-9.]{1,10}"\s'
    k_id_product = '&id_product=[0-9]{1,7}&'
    k_linkrewrite = 'linkrewrite="[0-9a-z-]{1,100}"'


    url = 'http://www.farmalisto.com.co/buscar'



    '#Constructor'
    def __init__(self, medicamento, nombre_archivo):
        self.medicamentos = []  # creates a new empty list for each medicine
        self.medicamento = medicamento #Medicamento a consultar
        self.archivo = nombre_archivo + '_' + medicamento + '.txt'
        self.filas = []


    def get_medicamentos(self):
        self.get_items(self)
        '#En medicamentos quedan los 14 registros, falta filtrar mas '
        return self.medicamentos

    '#Hacer la petición GET y capturar resultado'
    def set_request(self, regs_mostrar):
        values = {'search_query': self.medicamento,
                  'n': regs_mostrar}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req)
        string_filtrar = response.read()
        self.filtrar_archivo(string_filtrar)




    def filtrar_archivo(self, filtrar):
        '#Ahora partir por cada linea'
        '#Obtener la info de los medicamentos'
        control = 0
        for i, part in enumerate(filtrar.split(self.k_inicio_lista)):
            control = control + 1
            if not part.strip(): continue  # make sure its not empty
            if control > 1:
                file_tmp = open(self.archivo, 'r')
                '# Escribe en el archivo la información'
                file_tmp.write(part)
                file_tmp.close()
                '#En el archivo queda la lista con los medicamentos'




    def get_items(self):
        '#Abre el archivo con todos los medicamentos'
        f = open(self.archivo, 'r')  # Toco modificar había un caracter de continuación raro
        filedata = f.read()
        f.close()

        '#Inicializar la lista de los medicamentos'
        self.filas = []

        '#Ahora partir por cada linea'
        p = re.compile(self.k_item)
        self.filas = p.split(filedata)
        return self.filas

    def separar_items(self):
        '#Hacer loop a la lista. No mirar el item 0 '
        for texto in self.filas:
            self.extraer_info(texto)


    def extraer_info(self, fila):
        item = []
        '#Aplicar el filtro id_producto'
        p = re.compile(self.k_id_product)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            id_producto = match.string[match.start(): match.end()]
            item.append(id_producto)

        '#Aplicar el filtro imagen link'
        p = re.compile(self.k_product_img_link)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            img_link = match.string[match.start(): match.end()]
            item.append(img_link)

        '#Aplicar el filtro nombre producto'
        p = re.compile(self.k_namepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            nombre_producto = match.string[match.start(): match.end()]
            item.append(nombre_producto)

        '#Aplicar el filtro precio'
        p = re.compile(self.k_pricepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            precio = match.string[match.start(): match.end()]
            item.append(precio)
        self.medicamentos.append(item)

    def escribir_archivo(self, filename):
        outfile = open(filename, 'r')
        outfile.write("\n".join(self.medicamentos))









