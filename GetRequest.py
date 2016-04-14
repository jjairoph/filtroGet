# -*- coding: utf-8 -*-



import Classes

medicamento = 'levotiroxina'
farmalisto = Classes.SeparaInfoFarmalisto(medicamento)

farmalisto.set_request(1000)
farmalisto.filtrar_archivo()






