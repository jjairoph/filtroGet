# -*- coding: utf-8 -*-
import os  # Mostrar la ruta al archivo
import re  # Expresiones regulares
import urllib
import urllib2
import json
import string

'#https://docs.python.org/2/howto/urllib2.html'
'#HOWTO Fetch Internet Resources Using urllib2'

'#Para probar on line regex'
'#http://www.regextester.com/20'

'#RegExp para usar en las farmacias'
k_nombre_largo = '[A-Z\s\/0-9\%a-z-óáéíú.,&;]{10,180}'

k_nombre_corto = '[A-Z\s\/0-9\%a-z-óáéíú.,&;]{1,50}'

'#número con separador decimal .'
k_precio_pto = '[0-9.]{1,10}'
'#número con separador decimal ,'
k_precio_coma_espacios = '[\$0-9,\s]{1,30}'
'#Id de producto'
k_id_producto = '[0-9]{1,7}'

'#url valido'
'#No funcionó'
#k_link = '^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$'
k_link = 'http[s]?:\/?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)'

'#Separador columnas info drogueria'
k_sep_campo = '||'

class SeparaInfoFarmalisto:
    # como consultar farmalisto
    # http://www.farmalisto.com.co/buscar?search_query=loratadina&n=5000

    '#RegEx para identificar inicio de la lista de resultados medicamentos consultados'
    k_inicio_lista = '<ul class="product_grid" id="product_list">'

    '#Patrones para separar cada item'
    '#<li class="grid_4 ajax_block_product first_item item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product alternate_item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product alternate_item clearfix omega alpha">'
    '#<li class="grid_4 ajax_block_product last_item alternate_item clearfix omega alpha">'
    k_item = '<li class="grid_4 ajax_block_product [a-z_\s]{13,50}omega alpha">'

    '#Detalle del patron de las columnas de cada fila'


    k_product_img_link = '<a class="product_img_link"\shref="' + k_link + '"'

    k_alt = 'alt="[[A-Z\s0-9a-z]{1,150}"\s\/>'
    k_namepro = 'namepro="' + k_nombre_largo + '"'
    k_desc_prod = 'html" title="' + k_nombre_largo + '">'
    k_pricepro = '\spricepro="' + k_precio_pto + '"\s'
    k_id_product = '&id_product=' + k_id_producto + '&'
    k_linkrewrite = 'linkrewrite="[0-9a-z-]{1,100}"'



    url = 'http://www.farmalisto.com.co/buscar'



    '#Constructor'
    def __init__(self, medicamento, farmacia, contador):
        self.medicamentos = []  # creates a new empty list for each medicine
        self.medicamento = medicamento #Medicamento a consultar
        self.farmacia = farmacia
        self.archivo = farmacia + '_' + str(contador) + '.txt'
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
                file_tmp = open(self.archivo, 'w')
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

        '#Revisar que el primer item no este vacio'
        if len(self.filas[0]) == 0:
            del self.filas[0]
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
            id_producto = match.string[match.start()+12: match.end()-1]
            id_producto = 'id_producto' + k_sep_campo + id_producto
            item.append(id_producto)

        '#Aplicar el filtro imagen link'
        p = re.compile(self.k_product_img_link)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            link_detalle = match.string[match.start()+34: match.end()-1]
            link_detalle = 'link_detalle' + k_sep_campo + link_detalle
            item.append(link_detalle)

        '#Aplicar el filtro nombre producto CONTIENE LA MARCA'
        p = re.compile(self.k_namepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            nombre_producto = match.string[match.start()+9: match.end()-1]
            nombre_producto = 'nombre_producto' + k_sep_campo + nombre_producto
            item.append(nombre_producto)

        '#Aplicar el filtro nombre desc producto'
        p = re.compile(self.k_desc_prod)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            desc_prod = match.string[match.start()+13: match.end()-2]
            desc_prod = 'desc_prod' + k_sep_campo + desc_prod
            item.append(desc_prod)

        '#Aplicar el filtro precio'
        p = re.compile(self.k_pricepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            precio = match.string[match.start()+11: match.end()-2]
            precio = 'precio' + k_sep_campo + precio
            item.append(precio)

        '#No se almacena si esta vacio'
        if len(item) > 1:
            self.medicamentos.append(item)



    def escribir_archivo(self, filename):
        outfile = open(filename, 'a')
        for linea in self.medicamentos:
            json.dump(linea, outfile)
            outfile.write('\n')
            '#outfile.write("\n".join(linea))'

        outfile.close()

'''
**********************************************************************************************************************
Clase para sfarmadroguerias
**********************************************************************************************************************
'''

class SeparaSFarma:
    '# como consultar sfarma'
    '# http://www.sfarmadroguerias.com/buscar?controller=search&orderby=position&orderway=desc&search_query=acetaminofen&submit_search=&n=300'
    '#Consulta minima'
    '#http://www.sfarmadroguerias.com/buscar?search_query=levotiroxina&n=300'

    '#RegEx para identificar inicio de la lista de resultados medicamentos consultados'
    '#SE ENCONTRARON DOS DIFERENTES'
    '<ul class="list-unstyled product_list products-block row  default nopadding list">'
    '<ul class="list-unstyled product_list products-block grid row  default nopadding">'
    '#Para garantizar que lo encuentre se toma lo comun a ambos'
    k_inicio_lista = '<ul class="list-unstyled product_list products-block[a-z_\s-]{13,50}">'

    '#Patrones para separar cada item'
    '#<li class="ajax_block_product  col-xs-12 first-in-line first-item-of-tablet-line first-item-of-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12 last-item-of-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12 last-item-of-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12 last-item-of-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12 first-in-line first-item-of-tablet-line first-item-of-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#<li class="ajax_block_product  col-xs-12 last-line last-item-of-mobile-line last-mobile-line" data-col-lg="3" data-col-md="3" data-col-sm="4">'
    '#Para cada item'
    k_item = '<li class="ajax_block_product  col-xs-12["=0-9a-z_\s-]{13,270}data-col-sm="4">'

    '#Detalle del patron de las columnas de cada fila'
    k_id_product = 'data-id-product="' + k_id_producto + '" title="Comparar ">'
    k_namepro = 'title="' + k_nombre_largo + '" itemprop="url">'
    #k_alt = 'alt="[[A-Z\s0-9a-z]{1,150}"\s\/>'
    k_disponibilidad = '<link itemprop="availability" href="http:\/\/schema.org\/' + k_nombre_corto + '" \/>' + k_nombre_corto + '<\/span>'
    k_pricepro = '<span itemprop="price" class="product-price new-price">' + k_precio_coma_espacios
    #k_linkrewrite = 'linkrewrite="[0-9a-z-]{1,100}"'
    k_product_img_link = '<a class="img product_img_link"\shref="' + k_link


    url = 'http://www.sfarmadroguerias.com/buscar'


    '#Constructor podria venir de clase padre'
    def __init__(self, medicamento, farmacia, contador):
        self.medicamentos = []  # creates a new empty list for each medicine
        self.farmacia = farmacia
        self.medicamento = medicamento  # Medicamento a consultar
        self.archivo = farmacia + '_' + str(contador) + '.txt'
        self.filas = []


    '#deberia estar clase padre'
    def get_medicamentos(self):
        self.get_items(self)
        '#En medicamentos quedan los 14 registros, falta filtrar mas '
        return self.medicamentos


    '#Hacer la petición GET y capturar resultado'


    '#esto podria variar y hacer uno aparte para get y post'
    def set_request(self, regs_mostrar):
        values = {'search_query': self.medicamento,
                  'n': regs_mostrar}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req)
        string_filtrar = response.read()
        self.filtrar_archivo(string_filtrar)


    '#Para sfarma NO es igual la logica NO EN PADRE'
    def filtrar_archivo(self, filtrar):
        '#Ahora partir por cada linea'
        '#Obtener la info de los medicamentos'
        #control = 0
        for i, part in enumerate(filtrar.split(self.k_inicio_lista)):
            #control = control + 1
            if not part.strip(): continue  # make sure its not empty
            #if control > 1:
            file_tmp = open(self.archivo, 'w')
            '# Escribe en el archivo la información'
            file_tmp.write(part)
            file_tmp.close()
            '#En el archivo queda la lista con los medicamentos'

    '#Este metodo puede estar en la clase padre'
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

        '#Revisar que el primer item no este vacio'
        if len(self.filas[0]) == 0:
            del self.filas[0]

        return self.filas


    def separar_items(self):
        '#Hacer loop a la lista. No mirar el item 0 '
        for texto in self.filas:
            self.extraer_info(texto)


    '#Extraer datos SFARMA Este es especifico para cada farmacia'
    def extraer_info(self, fila):
        item = []
        '#Aplicar el filtro id_producto'
        p = re.compile(self.k_id_product)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            id_producto = match.string[match.start() + 17: match.end() - 20]
            id_producto = 'id_producto' + k_sep_campo + id_producto
            item.append(id_producto)

        '#Aplicar el filtro imagen link'
        p = re.compile(self.k_product_img_link)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            img_link = match.string[match.start() + 38: match.end() - 1]
            img_link = 'img_link' + k_sep_campo + img_link
            item.append(img_link)

        '#Aplicar el filtro nombre producto CONTIENE LA MARCA'
        p = re.compile(self.k_namepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            nombre_producto = match.string[match.start() + 7: match.end() - 17]
            nombre_producto = 'nombre_producto' + k_sep_campo + nombre_producto
            item.append(nombre_producto)

        '#Aplicar el filtro nombre desc producto'
        p = re.compile(self.k_disponibilidad)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            disponibilidad = match.string[match.start() + 54: match.end() - 7]
            disponibilidad = string.replace(disponibilidad, '\t', '')
            disponibilidad = 'disponibilidad' + k_sep_campo + disponibilidad
            item.append(disponibilidad)

        '#Aplicar el filtro precio'
        p = re.compile(self.k_pricepro)
        iteratorfile = p.finditer(fila)
        for match in iteratorfile:
            """print(match.span())#Punto en donde se encuentra la coincidencia
            print( match.start())#Donde comienza el string que concuerda
            print( match.end())#Donde termina el string que concuerda"""
            precio = match.string[match.start() + 55: match.end() - 2]
            precio = string.replace(precio, '\t', '')
            precio = string.replace(precio, '\n', '')
            precio = 'precio' + k_sep_campo + precio
            item.append(precio)

        '#No se almacena si esta vacio'
        if len(item) > 1:
            self.medicamentos.append(item)

    '#Puede estar clase padre'
    def escribir_archivo(self, filename):
        outfile = open(filename, 'a')
        for linea in self.medicamentos:
            json.dump(linea, outfile)
            outfile.write('\n')
            '#outfile.write("\n".join(linea))'

        outfile.close()





