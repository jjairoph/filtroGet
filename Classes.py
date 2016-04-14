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
    k_item = '<li class="grid_4 ajax_block_product [a-z_\s]{13,25}omega alpha">'

    url = 'http://www.farmalisto.com.co/buscar'

    archivo = 'farmalisto'


    def __init__(self, medicamento):
        self.medicamentos = []  # creates a new empty list for each medicine
        self.medicamento = medicamento #Medicamento a consultar

    def get_medicamentos(self):
        return self.medicamentos

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

        for i, part in enumerate(filtrar.split(self.k_item)):
            if not part.strip(): continue  # make sure its not empty
            self.medicamentos.append(part)




