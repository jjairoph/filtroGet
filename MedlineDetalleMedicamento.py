# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import json
import codecs
import MySQLdb
import sys

from pprint import pprint

#http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
'#Recibir el URL como parametro'
link = 'https://medlineplus.gov/spanish/druginfo/meds/a682571-es.html'


'''###################################################################################################################'
<div class="section-body" id="section-warning"><p> Queda la adverncia  </p>
<div class="section-body" id="section-1"><p> descripcion </p>
<div class="section-body" id="section-2"><p> ... </p>
<div class="section-body" id="section-precautions">
<div class="section-body" id="section-5">
<div class="section-body" id="section-6">
<div class="section-body" id="section-side-effects">
<div class="section-body" id="section-8">
<div class="section-body" id="section-9">
<div class="section-body" id="section-10">
<div class="section-body" id="section-brandname-1">
#why">¿Para cuáles condiciones o enfermedades se prescribe este medicamento?
#how">¿Cómo se debe usar este medicamento?
#precautions">¿Cuáles son las precauciones especiales que debo seguir?
#if-i-forget">¿Qué tengo que hacer si me olvido de tomar una dosis?
#side-effects">¿Cuáles son los efectos secundarios que podría provocar este medicamento?
#storage-conditions">¿Cómo debo almacenar o desechar este medicamento?
#other-information">¿Qué otra información de importancia debería saber?
'''

'#Clase utilizada para obtener la información detallada de medicamento en MEDLINEPLUS'
class InfoMedicamentoMedline:

    PASSWD_LOCAL = "elpdhsqep"
    LOCALSQL_INSTANCE = 'pharmallium'
    #TABLA_CARACTERISTICAS = 'pharmallium.medlinemedicamentos'
    TABLA_CARACTERISTICAS = 'pharmallium.medlinemedsunicos'

    INSERT_SIN_DUPLICADOS = 'INSERT into ' + TABLA_CARACTERISTICAS + ' (NombreMedicamento, LinkHtml, StringConsulta, why, how, otherUses, precautions, specialDietary, ifIForget, sideEffects, storageConditions, overdose, otherInformation, brandName, id_atc) ' \
                            ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    '#Recibir el URL base como parametro'
    linkInicial = 'https://medlineplus.gov/spanish/druginfo/meds/'

    '#Constructor de la clase'

    def __init__(self, urlMed):
        self.urlMedicamento = urlMed  # Pagina informacion Medicamento


    '#se puede hacer otro para los <li>'
    def getText(self, tag, id, idtexto, soup):
        divs = soup.find_all(tag, id=id)
        texto = 'vacio'
        for element in divs:
            texto = element.find(class_=idtexto).get_text()
            '#print len(texto)'
        return texto


    def getPropiedadesMedicamento(self, soup):
        propiedades = {}
        propiedades['why'] = self.getText("div", "why", "section-body", soup)
        propiedades['how'] = self.getText("div", "how", "section-body", soup)
        propiedades['other-uses'] = self.getText("div", "other-uses", "section-body", soup)
        propiedades['precautions'] = self.getText("div", "precautions", "section-body", soup)
        propiedades['special-dietary'] = self.getText("div", "special-dietary", "section-body", soup)
        propiedades['if-i-forget'] = self.getText("div", "if-i-forget", "section-body", soup)
        propiedades['side-effects'] = self.getText("div", "side-effects", "section-body", soup)
        propiedades['storage-conditions'] = self.getText("div", "storage-conditions", "section-body", soup)
        propiedades['overdose'] = self.getText("div", "overdose", "section-body", soup)
        propiedades['other-information'] = self.getText("div", "other-information", "section-body", soup)
        propiedades['brand-name'] = self.getText("div", "brand-name-1", "section-body", soup)
        return propiedades




    def getSoup(self, link):
        linkCompleto = self.linkInicial + link
        try:
            r = urllib.urlopen(linkCompleto).read()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1} link medicamento".format(errno, strerror)
        except:
            print "Unexpected error: Link medicamento", sys.exc_info()[0]

            raise

        return BeautifulSoup(r)

    '#Inserta en la tabla correspondientye la longitud de cada campo para todos los medicamentos'
    def insertarMysqlLongitud(self, fila, consulta, med, finlink, id_atc):

        record = [med, finlink, consulta, fila['why'], fila['how'], fila['other-uses'],fila['precautions'], fila['special-dietary'], fila['if-i-forget'], fila['side-effects'], fila['storage-conditions'], fila['overdose'], fila['other-information'],fila['brand-name'], id_atc]
        db = MySQLdb.connect(host='localhost', user='root', passwd=self.PASSWD_LOCAL, db=self.LOCALSQL_INSTANCE)
        '# prepare a cursor object using cursor() method'
        cursor = db.cursor()
        # SQL query to INSERT a record into the table FACTRESTTBL.
        cursor.execute(self.INSERT_SIN_DUPLICADOS, record)

        # Commit your changes in the database
        db.commit()

        # disconnect from server
        #db.close()

    '#Ingresar las caracteristicas a la tabla'
    def insertarMysqlMedicamento(self, fila, consulta, med, finlink, idatc):
        record = [med, finlink, consulta, fila['why'], fila['how'], fila['other-uses'], fila['precautions'],
                  fila['special-dietary'], fila['if-i-forget'], fila['side-effects'], fila['storage-conditions'],
                  fila['overdose'], fila['other-information'], fila['brand-name'], idatc]
        db = MySQLdb.connect(host='localhost', user='root', passwd=self.PASSWD_LOCAL, db=self.LOCALSQL_INSTANCE)
        '# prepare a cursor object using cursor() method'
        cursor = db.cursor()

        try:
            '# SQL query to INSERT a record into the table '
            cursor.execute(self.INSERT_SIN_DUPLICADOS, record)
            # Commit your changes in the database
            db.commit()
        except MySQLdb.IntegrityError, e:
            '# handle a specific error condition'
            print record
            print str(e)
        except MySQLdb.Error, e:
            '# handle a generic error condition'
            print record
            print str(e)
        except MySQLdb.Warning, e:
            '# handle warnings, if the cursor youre using raises them'
        except :
            '# catch *all* exceptions'
            e = sys.exc_info()[0]
            print record
            print '###########################################'
            print str(e)
            print str(sys.exc_info())

        # disconnect from server
        # db.close()





'#Por aqui comienza la ejecución del programa'
if __name__ == "__main__":
    print ("Iniciando programa detalle medicamento")

    '#De un archivo plano en formato JSON tomar los nombres y las paginas que contiene la info de medicamentos a consultar'
    jsonlinks_file = "MedlineResultado.json"

    json_data = open(jsonlinks_file)
    data = json.load(json_data)
    json_data.close()

    '#Diccionario que muestra la longitud de cada campo'
    resultadoFinal = {}
    for k in data:
        medicamentoLink = data[k]
        for medl in medicamentoLink:
            finLink = medicamentoLink[medl]
            #print medl
            #print (finLink)
            detalleMedicamento = InfoMedicamentoMedline(finLink)
            resultadoFinal[medl] = detalleMedicamento.getPropiedadesMedicamento(detalleMedicamento.getSoup(finLink))
            detalleMedicamento.insertarMysqlMedicamento(detalleMedicamento.getPropiedadesMedicamento(detalleMedicamento.getSoup(finLink)), k, medl, finLink)


    '#Escribir el resultado en un archivo en formato JSON'
    with codecs.open('archivoResultadoMedlineLongitud.json', 'w', 'utf8') as f:
        f.write(json.dumps(resultadoFinal, indent=4, sort_keys=True, ensure_ascii=False))

    print 'Programa finalizado resultado en '

'''
print 'why'
textomostrar = getText("div", "why", "section-1", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'how'
textomostrar = getText("div", "how", "section-2", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'other-uses'
textomostrar = getText("div", "other-uses", "section-3", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'precautions'
textomostrar = getText("div", "precautions", "section-precautions", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'special-dietary'
textomostrar = getText("div", "special-dietary", "section-5", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'if-i-forget'
textomostrar = getText("div", "if-i-forget", "section-6", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'


print 'side-effects'
textomostrar = getText("div", "side-effects", "section-side-effects", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'overdose'
textomostrar = getText("div", "overdose", "section-9", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'

print 'other-information'
textomostrar = getText("div", "other-information", "section-10", soup)
print str(len(textomostrar))
print textomostrar
print '***************************************************************'


print 'brand-name-1'
textomostrar = getText("div", "brand-name-1", "section-brandname-1", soup)
print str(len(textomostrar))
print textomostrar


'''