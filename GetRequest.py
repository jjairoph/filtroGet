# -*- coding: utf-8 -*-

'#https://docs.python.org/2/howto/urllib2.html'
'#HOWTO Fetch Internet Resources Using urllib2'

import urllib
import urllib2
import os  # Mostrar la ruta al archivo
import re  # Expresiones regulares


'#RegEx para identificar inicio de la lista de resultados HAY QUE BUSCAR ESTE PATRON'
k_inicio_lista = '<ul class="product_grid" id="product_list">'
#k_inicio_lista = '\n\d{1,2}\n'

'#Patron para cada item'
k_item = '<li class="grid_4 ajax_block_product first_item item clearfix omega alpha">'






#como consultar farmalisto
#http://www.farmalisto.com.co/buscar?search_query=loratadina&n=500

buscar = 'levotiroxina'

url = 'http://www.farmalisto.com.co/buscar'
values = {'search_query' : buscar,
          'n' : '1000' }

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
resultado = response.read()


for i, part in enumerate(resultado.split(k_inicio_lista)):
    if not part.strip(): continue  # make sure its not empty
    na = 'res.txt'
    file_tmp = open(na, 'w')
    '# Escribe en el archivo la información separada por unidades(week_unit1.txt, week_unit2.txt ...)'
    file_tmp.write(part)
    file_tmp.close()
'#En el archivo queda la lista con los medicamentos'


'#Abre el archivo con todos los medicamentos'
f = open(na, 'r')  # Toco modificar había un caracter de continuación raro
filedata = f.read()
f.close()


'#Inicializar la lista de los medicamentos'
medicamentos = []

'#Ahora partir por cada linea'
'#'
pf = re.compile(k_item)
iteratorfile = pf.finditer(filedata)


for i, part in enumerate(filedata.split(k_item)):
    if not part.strip(): continue  # make sure its not empty
    #na = 'res.txt'
    #file_tmp = open(na, 'w')
    '# Escribe en el archivo la información separada por unidades(week_unit1.txt, week_unit2.txt ...)'
    medicamentos.append(part)

'#En el archivo queda la lista con los medicamentos'



