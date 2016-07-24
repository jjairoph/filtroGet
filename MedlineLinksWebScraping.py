# -*- coding: utf-8 -*-

import re  # Expresiones regulares
import urllib
import urllib2
import json
import codecs
from bs4 import BeautifulSoup

'#Query para obtener informacion medicamento'
'#https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?&v:project=medlineplus-spanish&v:sources=medlineplus-spanish-bundle&query=acetaminofen&binning-state=group%3d%3dMedicinas%20y%20suplementos&'

'#https://docs.python.org/2/howto/urllib2.html'
'#HOWTO Fetch Internet Resources Using urllib2'

'#wEB sCRAPING'
'#http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html'

'''#Para probar on line regex
http://www.regextester.com/20
http://regexr.com/
'''


'#TODAS LAS CONSTANTES DEFINIDAS POR FUERA DE LA CLASE NO SE PUEDEN USAR'
'#Solo sirven en el programa principal'
archivoResultadoMedline = 'MedlineResultado.json'

'#Fake browser visit '
k_url_from = 'http://www.ichangtou.com/#company:data_000008.html'
k_headers_mozilla = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


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
'#k_link = ^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$'
k_link = 'http[s]?:\/?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)'

'#Separador columnas info drogueria'
k_sep_campo = '||'

'#Clase utilizada para obtener la información de MEDLINEPLUS'
class SeparaInfoMedline:

    '''#Patrones para separar cada item'
    https://www.nlm.nih.gov/.../spanish/druginfo/meds/a697038-es.html
    https://www.nlm.nih.gov/medlineplus/spanish/druginfo/meds/a697038-es.html
    https://www.nlm.nih.gov/.../spanish/druginfo/meds/a603031-es.html
    '''
    k_item = '(https:\/\/)(www.nlm.nih.gov\/\.\.\.\/)[A-Z\s0-9a-z\/-]{1,60}.htm.?'

    '#asi se obtiene la pagina con la info del medicamento EJ a611019-es.html'
    k_id_medicamento = 'a6\d\d\d\d\d-es\.html'

    k_url_detalle_med = 'https://www.nlm.nih.gov/medlineplus'

    k_resultadomedplus = 'resultadoMedplus.txt'

    k_patron_buscar = 'https://www.nlm.nih.gov/...'

    k_alt = 'alt="[[A-Z\s0-9a-z]{1,150}"\s\/>'
    k_namepro = 'namepro="' + k_nombre_largo + '"'
    k_desc_prod = 'html" title="' + k_nombre_largo + '">'
    k_pricepro = '\spricepro="' + k_precio_pto + '"\s'
    k_id_product = '&id_product=' + k_id_producto + '&'
    k_linkrewrite = 'linkrewrite="[0-9a-z-]{1,100}"'

    k_partir = 'project-medlineplus-spanish sources-medlineplus-spanish-bundle'


    '#URL que da inicio al query con GET'
    url = 'https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta'

    '#Query para obtener informacion medicamento'
    '#https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?&v:project=medlineplus-spanish&v:sources=medlineplus-spanish-bundle&query=acetaminofen&binning-state=group%3d%3dMedicinas%20y%20suplementos&'

    '#Constructor de la clase'
    def __init__(self, medicamento):
        self.medicamentos = []  # creates a new empty list for each medicine
        self.medicamento = medicamento #Medicamento a consultar
        self.archivoResultadoMedline = 'MedlineResultado.json'
        self.filas = []

    '#Hacer la petición GET y capturar resultado'
    'El resultado es un json con el resultado obtenido de la consulta, nombre y pagina con la informacion'
    '# Ibuprofeno a693050-es.html'
    def set_requestWebScraping(self, medicamento):
        # headers = {'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Referer': 'http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=293', 'Origin': 'http://www.transtats.bts.gov', 'Upgrade-Insecure-Requests': 1, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'Cookie': 'ASPSESSIONIDQADBBRTA=CMKGLHMDDJIECMNGLMDPOKHC', 'Accept-Language': 'en-US,en;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded'}
        values = {'v:project': 'medlineplus-spanish',
                  'v:sources': 'medlineplus-spanish-bundle',
                  'query': medicamento,
                  'binning-state': 'group==Medicinas y suplementos'}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req)
        string_filtrar = response.read()
        soup = BeautifulSoup(string_filtrar)
        '#Obtener todos los resultados que corresponden a medicinas y suplementos'
        divs = soup.find_all("li", class_="document source-drugs-spanish")
        resultados = {}
        for element in divs:
            resultados[element.a.get_text()] = self.getLinksWebCrawling(element.a["href"])
        return resultados



    '#Sacar el nombre de la pagina para el medicamento'
    def getLinksWebCrawling(self, filtrar):
        self.filas = []
        '#Ahora partir por cada linea'
        p = re.compile(self.k_id_medicamento)
        iteratorfile = p.finditer(filtrar)
        for match in iteratorfile:
            print(match.start())  # Donde comienza el string que concuerda
            print(match.end())  # Donde termina el string que concuerda"""
            cadena = match.string[match.start(): match.end()]
            self.filas.append(cadena)
            '# Escribe en el archivo la información'
        return cadena



'#Por aqui comienza la ejecución del programa'
if __name__ == "__main__":
    print ("Iniciando programa")

    '#De un archivo plano de una sola columna tomar los nombres de los medicamentos a consultar en medline'
    meds_file = open("MedicamentosNoRepetidosConsultar.txt", "r")
    lines_med = meds_file.readlines()
    meds_file.close()
    '#Diccionario que muestra el parametro medicamento a consultar y los resultados obtenidos'
    resultadoFinal = {}

    for medicamento in lines_med:
        medline = SeparaInfoMedline(medicamento.replace('\n', ''))
        resultadoFinal[medicamento] = medline.set_requestWebScraping(medicamento)

    '#Escribir el resultado en un archivo en formato JSON'
    with codecs.open(archivoResultadoMedline, 'w', 'utf8') as f:
        f.write(json.dumps(resultadoFinal, indent=4, sort_keys=True, ensure_ascii=False))

    print 'Programa finalizado resultado en ' + archivoResultadoMedline

