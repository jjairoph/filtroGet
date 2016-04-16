# -*- coding: utf-8 -*-



import Classes

medicamento = 'levotiroxina'
farmacia = 'farmalisto'
resultado = []

'#De un archivo plano de una sola columna tomar los nombres de los medicamentos a consultar'
meds_file = open("query_meds.txt", "r")
lines_med = meds_file.readlines()
meds_file.close()

'#De un archivo plano de una sola columna tomar los nombres de las farmacias'
farmacias_file = open("farmacias.txt", "r")
farmacias = farmacias_file.readlines()
farmacias_file.close()


'#Despues incluir la iteracion de las farmacias'
for medicamento in lines_med:
    # farmalisto = Classes.SeparaInfoFarmalisto(medicamento.replace('\n', ''), farmacia)
    # farmalisto.set_request(1000)
    # resultado = farmalisto.get_items()
    # farmalisto.separar_items()
    # farmalisto.escribir_archivo('resultadoFarmalisto.txt')

    farmacia = 'sfarma'
    sfarma = Classes.SeparaSFarma(medicamento.replace('\n', ''), farmacia)
    sfarma.set_request(1000)
    resultado = sfarma.get_items()
    sfarma.separar_items()
    sfarma.escribir_archivo('resultadoSFarma.txt')









