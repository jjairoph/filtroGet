# -*- coding: utf-8 -*-



import Classes

medicamento = 'levotiroxina'
farmacia = 'farmalisto'
resultado = []

'#De un archivo plano tomar los nombres de los medicamentos a consultar'
text_file = open("query_meds.txt", "r")
lines = text_file.readlines()
text_file.close()

for medicamento in lines:
    farmalisto = Classes.SeparaInfoFarmalisto(medicamento.replace('\n', ''), farmacia)
    farmalisto.set_request(1000)
    resultado = farmalisto.get_items()
    farmalisto.separar_items()
    farmalisto.escribir_archivo('resultado.txt')









