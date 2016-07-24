# -*- coding: utf-8 -*-
import WebPages
import MedlineLinksWebScraping

consultaPrecios = 'PRECIOS'
consultaMedPlus = 'MEDPLUS'

medicamento = 'levotiroxina'
resultado = []

'#Selecciones si consulta precios(PRECIOS) o' \
'informacion general medicamento(MEDPLUS)  '
paginaConsultar = 'PRECIOS'

'#De un archivo plano de una sola columna tomar los nombres de los medicamentos a consultar'
#meds_file = open("query_meds.txt", "r")
meds_file = open("MedicamentosNorepetidosConsultar.txt", "r")
lines_med = meds_file.readlines()
meds_file.close()

'#De un archivo plano de una sola columna tomar los nombres de las farmacias'
farmacias_file = open("farmacias.txt", "r")
farmacias = farmacias_file.readlines()
farmacias_file.close()

contador = 0

'#Consultar precios'
if paginaConsultar == consultaPrecios:
    '#Despues incluir la iteracion de las farmacias'
    for medicamento in lines_med:
        farmacia = 'farmalisto'
        farmalisto = WebPages.SeparaInfoFarmalisto(medicamento.replace('\n', ''), farmacia, contador)
        farmalisto.set_request(1000)
        resultado = farmalisto.get_items()
        farmalisto.separar_items()
        farmalisto.escribir_archivo('resultadoFarmalisto.txt')

        farmacia = 'sfarma'
        sfarma = WebPages.SeparaSFarma(medicamento.replace('\n', ''), farmacia, contador)
        sfarma.set_request(1000)
        resultado = sfarma.get_items()
        sfarma.separar_items()
        sfarma.escribir_archivo('resultadoSFarma.txt')

        contador = contador + 1

        print contador







